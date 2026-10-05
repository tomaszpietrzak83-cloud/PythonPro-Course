from django.test import TestCase
from django.urls import reverse

from .models import Game, Genre, Studio, Tag


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


class GenreTests(TestCase):
    def test_rawg_genres_are_seeded(self):
        self.assertEqual(Genre.objects.count(), 19)
        self.assertEqual(Genre.objects.get(slug="role-playing-games-rpg").name, "RPG")

    def test_genre_filter_and_detail(self):
        action = Genre.objects.get(slug="action")
        game = Game.objects.create(title="Action Example")
        game.genres.add(action, Genre.objects.get(slug="adventure"))
        other = Game.objects.create(title="Other Example")
        response = self.client.get(reverse("gameshelf:game_list"), {"genre": "action"})
        self.assertEqual(list(response.context["games"]), [game])
        self.assertNotContains(response, other.title)
        detail = self.client.get(reverse("gameshelf:game_detail", args=[game.pk]))
        self.assertContains(detail, "Action")
        self.assertContains(detail, "Adventure")

    def test_unknown_genre_returns_form_error(self):
        response = self.client.get(reverse("gameshelf:game_list"), {"genre": "unknown"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["filter_form"].errors)
        self.assertFalse(response.context["games"].exists())


class TagTests(TestCase):
    def test_rawg_starter_tags_are_seeded(self):
        self.assertEqual(Tag.objects.count(), 12)
        self.assertEqual(Tag.objects.get(slug="singleplayer").name, "Singleplayer")

    def test_tag_filter_combines_with_genre_and_shows_detail(self):
        tag = Tag.objects.get(slug="co-op")
        action = Genre.objects.get(slug="action")
        game = Game.objects.create(title="Co-op Action")
        game.tags.add(tag, Tag.objects.get(slug="open-world"))
        game.genres.add(action)
        other = Game.objects.create(title="Co-op Puzzle")
        other.tags.add(tag)
        other.genres.add(Genre.objects.get(slug="puzzle"))
        url = reverse("gameshelf:game_list")
        response = self.client.get(url, {"tag": "co-op"})
        self.assertEqual(list(response.context["games"]), [game, other])
        response = self.client.get(url, {"tag": "co-op", "genre": "action"})
        self.assertEqual(list(response.context["games"]), [game])
        detail = self.client.get(reverse("gameshelf:game_detail", args=[game.pk]))
        self.assertContains(detail, "Co-op")
        self.assertContains(detail, "Open World")

    def test_unknown_tag_returns_form_error(self):
        response = self.client.get(reverse("gameshelf:game_list"), {"tag": "unknown"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["filter_form"].errors)
        self.assertFalse(response.context["games"].exists())
