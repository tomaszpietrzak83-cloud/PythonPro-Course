from io import BytesIO, StringIO
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import requests
from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings
from PIL import Image

from .models import Game

REQUEST = "GameShelf.management.commands.import_games.requests.get"


def response(status=200, payload=None, content=b""):
    result = Mock(status_code=status)
    result.json.return_value = payload
    result.iter_content.return_value = iter([content])
    context = Mock()
    context.__enter__ = Mock(return_value=result)
    context.__exit__ = Mock(return_value=False)
    return context


@override_settings(RAWG_API_KEY="test-key")
class ImportGamesTests(TestCase):
    @patch(REQUEST)
    def test_import_stores_image_and_reuses_existing_game(self, get):
        image = BytesIO()
        Image.new("RGB", (20, 30)).save(image, format="PNG")
        cover_url = "https://media.rawg.io/media/demo.png"
        row = {
            "id": 123,
            "name": "Orbit",
            "released": "2020-01-03",
            "background_image": cover_url,
        }
        listing = {"results": [row]}
        get.side_effect = [
            response(payload=listing),
            response(payload={"description": "<p>Orbit game</p>"}),
            response(content=image.getvalue()),
            response(payload=listing),
        ]
        manual = Game.objects.create(title="Orbit")
        with (
            TemporaryDirectory() as folder,
            override_settings(MEDIA_ROOT=folder),
        ):
            call_command("import_games", stdout=StringIO())
            game = Game.objects.get(rawg_id=123)
            self.assertTrue(game.cover.storage.exists(game.cover.name))
            self.assertEqual(game.description, "Orbit game")
            self.assertTrue(game.genres.filter(slug="action").exists())
            game.title = "Edited"
            game.save()
            call_command("import_games", stdout=StringIO())
            game.refresh_from_db()
            self.assertEqual(game.title, "Edited")
            self.assertEqual(Game.objects.count(), 2)
            self.assertIsNone(manual.rawg_id)
            self.assertEqual(get.call_args_list[2].args, (cover_url,))
            self.assertNotIn("params", get.call_args_list[2].kwargs)

    @patch(REQUEST)
    def test_cover_on_unknown_host_is_not_requested(self, get):
        get.side_effect = [
            response(
                payload={
                    "results": [
                        {
                            "id": 123,
                            "name": "Orbit",
                            "background_image": "https://example.invalid/a.png",
                        }
                    ]
                }
            ),
            response(payload={}),
        ]
        errors = StringIO()
        call_command("import_games", stdout=StringIO(), stderr=errors)
        self.assertIn("placeholder", errors.getvalue())
        self.assertEqual(get.call_count, 2)
        self.assertFalse(Game.objects.get(rawg_id=123).cover)

    @patch(REQUEST, side_effect=requests.ConnectionError("URL?key=test-key"))
    def test_connection_error_does_not_expose_key(self, get):
        with self.assertRaises(CommandError) as error:
            call_command("import_games")
        self.assertNotIn("test-key", str(error.exception))
        self.assertFalse(Game.objects.exists())

    @override_settings(RAWG_API_KEY="")
    def test_missing_key_is_reported(self):
        with self.assertRaisesMessage(CommandError, "Set RAWG_API_KEY"):
            call_command("import_games")
