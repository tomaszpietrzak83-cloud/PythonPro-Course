from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Game, Genre, Tag, UserGame


class CatalogAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_user_model().objects
        cls.owner = users.create_user("api_owner")
        cls.other = users.create_user("api_other")
        cls.game = Game.objects.create(title="Nebula Orbit")
        cls.game.genres.add(Genre.objects.get(slug="action"))
        cls.game.tags.add(Tag.objects.get(slug="singleplayer"))
        cls.other_game = Game.objects.create(title="Nebula Drift")
        UserGame.objects.create(user=cls.owner, game=cls.game, note="Private API note")
        UserGame.objects.create(user=cls.other, game=cls.other_game)

    def test_public_catalog_does_not_expose_private_data(self):
        for name in ("game-list", "genre-list", "tag-list"):
            response = self.client.get(reverse(f"gameshelf_api:{name}"))
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json(), list)
        detail = self.client.get(reverse("gameshelf_api:game-detail", args=[self.game.pk]))
        self.assertEqual(detail.json()["title"], self.game.title)
        self.assertTrue(detail.json()["cover_url"].endswith("cover-placeholder.svg"))
        self.assertNotIn("note", detail.json())
        self.assertNotContains(detail, "Private API note")

    def test_public_filters_combine_and_validate(self):
        url = reverse("gameshelf_api:game-list")
        result = self.client.get(url, {"q": "NEBULA", "genre": "action", "tag": "singleplayer"})
        self.assertEqual([game["id"] for game in result.json()], [self.game.pk])
        result = self.client.get(url, {"genre": "unknown"})
        self.assertEqual(result.status_code, 400)
        self.assertIn("genre", result.json())

    def test_missing_game_returns_404(self):
        self.assertEqual(
            self.client.get(reverse("gameshelf_api:game-detail", args=[999999])).status_code, 404
        )

    def test_library_requires_session_and_returns_only_current_users_entries(self):
        url = reverse("gameshelf_api:library-list")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.force_login(self.owner)
        result = self.client.get(url, {"user": self.other.pk})
        self.assertEqual(result.status_code, 200)
        self.assertEqual([entry["game"] for entry in result.json()], [self.game.pk])
        self.assertEqual(result.json()[0]["note"], "Private API note")
