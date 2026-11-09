from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from .management.commands.seed_db import SEED_USER_GROUP
from .models import Game, Genre, Tag, UserGame


class SeederTests(TestCase):
    def seed(self, **options):
        output = StringIO()
        call_command("seed_db", stdout=output, **options)
        return output.getvalue()

    def test_default_seeder_is_repeatable_and_preserves_manual_games(self):
        manual = Game.objects.create(
            title="My real game", description="Keep me"
        )
        self.assertIn("Created 100", self.seed())
        seeded = Game.objects.filter(seed_key__isnull=False)
        self.assertEqual(seeded.count(), 100)
        self.assertEqual(
            seeded.filter(genres__slug="fake", tags__slug="fake").count(), 100
        )
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
        fields = (
            "seed_key",
            "title",
            "description",
            "release_date",
            "studio__name",
        )
        first = list(Game.objects.order_by("seed_key").values_list(*fields))
        Game.objects.all().delete()
        self.seed(games=2, seed=42)
        self.assertEqual(
            first, list(Game.objects.order_by("seed_key").values_list(*fields))
        )
        self.seed(games=3, seed=42)
        self.assertEqual(Game.objects.count(), 3)

    def test_invalid_count_does_not_write_games(self):
        for count in (0, -1):
            with self.subTest(count=count), self.assertRaises(CommandError):
                self.seed(games=count)
        self.assertFalse(Game.objects.exists())

    def test_default_seed_adds_fictional_taxonomy_without_creating_users(self):
        self.seed(games=8)
        self.assertEqual(
            Genre.objects.filter(slug__startswith="fake-theme-").count(), 4
        )
        self.assertEqual(
            Tag.objects.filter(slug__startswith="fake-feature-").count(), 6
        )
        self.assertTrue(Genre.objects.filter(slug="action").exists())
        for game in Game.objects.all():
            self.assertEqual(game.genres.count(), 2)
            self.assertEqual(game.tags.count(), 2)
            self.assertIsNotNone(game.studio)
        self.assertFalse(get_user_model().objects.exists())

    def test_users_and_libraries_repeat_safely_and_preserve_manual_edits(self):
        manual_user = get_user_model().objects.create_user("manual_collector")
        manual_game = Game.objects.create(title="Real game")
        manual_entry = UserGame.objects.create(
            user=manual_user, game=manual_game, note="Keep this"
        )
        options = {"games": 6, "users": 2, "entries_per_user": 4}
        self.seed(**options)
        self.assertEqual(UserGame.objects.count(), 9)
        seeded_users = get_user_model().objects.filter(
            groups__name=SEED_USER_GROUP
        )
        self.assertEqual(seeded_users.count(), 2)
        for user in seeded_users:
            self.assertFalse(user.has_usable_password())
            self.assertFalse(user.is_staff or user.is_superuser)
            self.assertEqual(user.game_entries.count(), 4)
            self.assertEqual(
                set(user.game_entries.values_list("list_type", flat=True)),
                {"owned", "wishlist"},
            )
        entry = UserGame.objects.exclude(pk=manual_entry.pk).first()
        entry.note, entry.rating, entry.play_status = (
            "My edited seed note",
            10,
            "completed",
        )
        entry.save()
        self.assertIn(
            "Library entries: created 0; reused 8", self.seed(**options)
        )
        entry.refresh_from_db()
        manual_entry.refresh_from_db()
        self.assertEqual(
            (entry.note, entry.rating, entry.play_status),
            ("My edited seed note", 10, "completed"),
        )
        self.assertEqual(manual_entry.note, "Keep this")
        self.assertEqual(UserGame.objects.count(), 9)

    def test_optional_password_only_applies_to_new_users(self):
        password = "Seed-Only-Nebula!82945"
        options = {
            "games": 2,
            "users": 1,
            "user_password_env": "GAMESHELF_TEST_PASSWORD",
        }
        with patch.dict("os.environ", {"GAMESHELF_TEST_PASSWORD": password}):
            self.seed(**options)
        user = get_user_model().objects.get(username="gameshelf_fake_001")
        self.assertTrue(user.check_password(password))
        with patch.dict(
            "os.environ",
            {"GAMESHELF_TEST_PASSWORD": "Different-Seed-Only!82945"},
        ):
            self.seed(**options)
        user.refresh_from_db()
        self.assertTrue(user.check_password(password))

    def test_invalid_library_options_write_nothing(self):
        cases = (
            {"users": -1},
            {"entries_per_user": -1},
            {"entries_per_user": 1},
            {"users": 1, "games": 2, "entries_per_user": 3},
            {"users": 1, "user_password_env": "GAMESHELF_MISSING_PASSWORD"},
        )
        with patch.dict("os.environ", {}, clear=True):
            for options in cases:
                with (
                    self.subTest(options=options),
                    self.assertRaises(CommandError),
                ):
                    self.seed(**options)
        self.assertFalse(Game.objects.exists())
        self.assertFalse(get_user_model().objects.exists())

    def test_manual_username_collision_rolls_back_the_whole_command(self):
        manual = get_user_model().objects.create_user(
            "gameshelf_fake_002", first_name="Keep me"
        )
        with self.assertRaises(CommandError):
            self.seed(games=2, users=2, entries_per_user=1)
        self.assertFalse(Game.objects.exists())
        self.assertEqual(get_user_model().objects.count(), 1)
        manual.refresh_from_db()
        self.assertEqual(manual.first_name, "Keep me")

    def test_marker_group_cannot_grant_seeded_users_permissions(self):
        group = Group.objects.create(name=SEED_USER_GROUP)
        group.permissions.add(Permission.objects.first())
        with self.assertRaises(CommandError):
            self.seed(games=2, users=1)
        self.assertFalse(get_user_model().objects.exists())
        self.assertFalse(Game.objects.exists())

    def test_library_targets_can_grow_without_duplicates(self):
        self.seed(games=4, users=1, entries_per_user=2)
        self.seed(games=4, users=2, entries_per_user=4)
        self.assertEqual(UserGame.objects.count(), 8)
        self.seed(games=4, users=2, entries_per_user=4)
        self.assertEqual(UserGame.objects.count(), 8)
