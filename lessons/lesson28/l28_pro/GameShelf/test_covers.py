from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType

from django.conf.urls.static import static as media_patterns
from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import SimpleUploadedFile
from django.templatetags.static import static
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Game, UserGame


def uploaded_cover(name="test-cover.png"):
    image = BytesIO()
    Image.new("RGB", (240, 360), color="#635bff").save(image, format="PNG")
    return SimpleUploadedFile(name, image.getvalue(), content_type="image/png")


class CoverUploadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser(
            "cover_admin", "cover@example.invalid", password=None
        )

    def setUp(self):
        self.media = TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        settings = override_settings(
            MEDIA_ROOT=self.media.name, MEDIA_URL="/media/"
        )
        settings.enable()
        self.addCleanup(settings.disable)
        self.client.force_login(self.admin)

    def admin_data(self, **overrides):
        return {
            "title": "Uploaded cover game",
            "description": "An upload test",
            "library_entries-TOTAL_FORMS": "0",
            "library_entries-INITIAL_FORMS": "0",
            "library_entries-MIN_NUM_FORMS": "0",
            "library_entries-MAX_NUM_FORMS": "1000",
            "_save": "Save",
            **overrides,
        }

    def test_admin_upload_stores_file_path_and_displays_cover(self):
        response = self.client.post(
            reverse("admin:GameShelf_game_add"),
            self.admin_data(cover=uploaded_cover()),
        )
        self.assertEqual(response.status_code, 302)
        game = Game.objects.get(title="Uploaded cover game")
        self.assertTrue(game.cover.name.startswith("covers/"))
        self.assertTrue(Path(game.cover.path).is_file())
        with Image.open(game.cover.path) as image:
            self.assertEqual(image.size, (240, 360))
        for url in (
            reverse("gameshelf:game_list"),
            reverse("gameshelf:game_detail", args=[game.pk]),
        ):
            self.assertContains(self.client.get(url), game.cover.url)

    def test_admin_rejects_non_image_upload_without_creating_game(self):
        fake_image = SimpleUploadedFile(
            "invalid.png", b"This is not a PNG", content_type="image/png"
        )
        response = self.client.post(
            reverse("admin:GameShelf_game_add"),
            self.admin_data(cover=fake_image),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("cover", response.context["adminform"].form.errors)
        self.assertFalse(Game.objects.exists())
        self.assertEqual(list(Path(self.media.name).rglob("*.png")), [])

    def test_cover_is_optional_and_pages_without_image_still_work(self):
        game = Game.objects.create(
            title="No cover yet", description="A game without art"
        )
        self.assertFalse(game.cover)
        for url in (
            reverse("gameshelf:game_list"),
            reverse("gameshelf:game_detail", args=[game.pk]),
        ):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, game.title)

    def test_same_upload_name_does_not_overwrite_another_games_cover(self):
        first = Game.objects.create(title="First cover", cover=uploaded_cover())
        second = Game.objects.create(
            title="Second cover", cover=uploaded_cover()
        )
        self.assertNotEqual(first.cover.name, second.cover.name)
        self.assertTrue(first.cover.storage.exists(first.cover.name))
        self.assertTrue(second.cover.storage.exists(second.cover.name))

    def test_cover_can_be_cleared_in_admin_without_removing_game(self):
        game = Game.objects.create(
            title="Uploaded cover game", cover=uploaded_cover()
        )
        response = self.client.post(
            reverse("admin:GameShelf_game_change", args=[game.pk]),
            self.admin_data(**{"cover-clear": "on"}),
        )
        self.assertEqual(response.status_code, 302)
        game.refresh_from_db()
        self.assertFalse(game.cover)

    def test_placeholder_asset_exists_and_empty_cover_uses_it(self):
        game = Game.objects.create(title="Empty image")
        self.assertIsNotNone(finders.find("GameShelf/cover-placeholder.svg"))
        self.assertEqual(
            game.cover_url, static("GameShelf/cover-placeholder.svg")
        )

    def test_missing_file_uses_placeholder_and_keeps_stored_reference(self):
        game = Game.objects.create(
            title="Deleted image", cover=uploaded_cover()
        )
        stored_name = game.cover.name
        game.cover.storage.delete(stored_name)
        game.refresh_from_db()
        self.assertEqual(game.cover.name, stored_name)
        self.assertEqual(
            game.cover_url, static("GameShelf/cover-placeholder.svg")
        )
        response = self.client.get(
            reverse("gameshelf:game_detail", args=[game.pk])
        )
        self.assertContains(response, game.cover_url)
        self.assertNotContains(response, "/media/" + stored_name)

    def test_existing_image_is_preferred_to_placeholder(self):
        game = Game.objects.create(
            title="Image present", cover=uploaded_cover()
        )
        self.assertEqual(game.cover_url, game.cover.url)

    def test_catalog_detail_and_library_show_uploaded_cover_and_placeholder(
        self,
    ):
        with_cover = Game.objects.create(
            title="Has image", cover=uploaded_cover()
        )
        without_cover = Game.objects.create(title="Needs placeholder")
        for game in (with_cover, without_cover):
            UserGame.objects.create(user=self.admin, game=game)
        for name in ("game_list", "my_library"):
            response = self.client.get(reverse(f"gameshelf:{name}"))
            self.assertContains(response, with_cover.cover_url)
            self.assertContains(response, without_cover.cover_url)
        for game in (with_cover, without_cover):
            response = self.client.get(
                reverse("gameshelf:game_detail", args=[game.pk])
            )
            self.assertContains(response, game.cover_url)

    def test_development_media_route_serves_actual_uploaded_bytes(self):
        game = Game.objects.create(title="Served image", cover=uploaded_cover())
        urls = ModuleType("cover_test_media_urls")
        with override_settings(DEBUG=True, ROOT_URLCONF=urls):
            urls.urlpatterns = media_patterns(
                "/media/", document_root=self.media.name
            )
            response = self.client.get(game.cover.url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response["Content-Type"], "image/png")
            with Image.open(
                BytesIO(b"".join(response.streaming_content))
            ) as image:
                self.assertEqual(image.size, (240, 360))
