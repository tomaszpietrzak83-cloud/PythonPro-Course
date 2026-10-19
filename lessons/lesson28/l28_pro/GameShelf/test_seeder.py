from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from .models import Game


class SeederTests(TestCase):
    def seed(self, **options):
        output = StringIO()
        call_command("seed_db", stdout=output, **options)
        return output.getvalue()

    def test_default_seeder_is_repeatable_and_preserves_manual_games(self):
        manual = Game.objects.create(title="My real game", description="Keep me")
        self.assertIn("Created 100", self.seed())
        seeded = Game.objects.filter(seed_key__isnull=False)
        self.assertEqual(seeded.count(), 100)
        self.assertEqual(seeded.filter(genres__slug="fake", tags__slug="fake").count(), 100)
        game = seeded.first()
        game.title = "My edited seeded title"
        game.save()
        self.assertIn("reused 100", self.seed())
        self.assertEqual(Game.objects.count(), 101)
        game.refresh_from_db()
        manual.refresh_from_db()
        self.assertEqual(game.title, "My edited seeded title")
        self.assertEqual(manual.description, "Keep me")
        self.assertFalse(manual.genres.exists())

    def test_seed_is_reproducible_and_count_can_grow(self):
        self.seed(games=2, seed=42)
        fields = ("seed_key", "title", "description", "release_date", "studio__name")
        first = list(Game.objects.order_by("seed_key").values_list(*fields))
        Game.objects.all().delete()
        self.seed(games=2, seed=42)
        self.assertEqual(first, list(Game.objects.order_by("seed_key").values_list(*fields)))
        self.seed(games=3, seed=42)
        self.assertEqual(Game.objects.count(), 3)

    def test_invalid_count_does_not_write_games(self):
        for count in (0, -1):
            with self.subTest(count=count), self.assertRaises(CommandError):
                self.seed(games=count)
        self.assertFalse(Game.objects.exists())
