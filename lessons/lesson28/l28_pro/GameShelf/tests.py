from django.test import TestCase
from django.urls import reverse

from .models import Game, Studio


class GameShelfViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(
            title="Celestial Roads",
            description="A relaxed exploration game about distant worlds.",
        )

    def test_homepage_returns_200_and_links_to_catalog(self):
        response = self.client.get(reverse("gameshelf:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Keep your game collection in one place.")
        self.assertContains(response, reverse("gameshelf:game_list"))

    def test_game_list_returns_200_and_shows_game(self):
        response = self.client.get(reverse("gameshelf:game_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.game.title)
        self.assertContains(
            response,
            reverse("gameshelf:game_detail", args=[self.game.pk]),
        )

    def test_game_detail_returns_200_and_shows_game_information(self):
        response = self.client.get(
            reverse("gameshelf:game_detail", args=[self.game.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.game.title)
        self.assertContains(response, self.game.description)

    def test_missing_game_detail_returns_404(self):
        response = self.client.get(reverse("gameshelf:game_detail", args=[9999]))

        self.assertEqual(response.status_code, 404)


class StudioTests(TestCase):
    def test_studio_is_visible_and_deleting_it_preserves_game(self):
        studio = Studio.objects.create(name="Test Studio")
        game = Game.objects.create(title="Test Game", studio=studio)
        for url in (
            reverse("gameshelf:game_list"),
            reverse("gameshelf:game_detail", args=[game.pk]),
        ):
            self.assertContains(self.client.get(url), studio.name)
        studio.delete()
        game.refresh_from_db()
        self.assertIsNone(game.studio)
