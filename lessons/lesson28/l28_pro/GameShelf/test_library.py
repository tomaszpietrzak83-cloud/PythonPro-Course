from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .models import Game, UserGame


class UserGameModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("collector")
        cls.other_user = get_user_model().objects.create_user("other_collector")
        cls.game = Game.objects.create(title="Shared game")

    def test_same_game_cannot_be_on_two_lists_for_one_user(self):
        UserGame.objects.create(user=self.user, game=self.game, list_type="owned")
        with self.assertRaises(IntegrityError), transaction.atomic():
            UserGame.objects.create(user=self.user, game=self.game, list_type="wishlist")
        self.assertEqual(UserGame.objects.count(), 1)

    def test_users_can_save_same_game_and_one_user_can_save_multiple_games(self):
        other_game = Game.objects.create(title="Another game")
        UserGame.objects.create(user=self.user, game=self.game)
        UserGame.objects.create(user=self.other_user, game=self.game, list_type="wishlist")
        UserGame.objects.create(user=self.user, game=other_game)
        self.assertEqual(self.user.game_entries.count(), 2)
        self.assertEqual(self.game.library_entries.count(), 2)

    def test_database_rejects_invalid_list_type(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            UserGame.objects.create(user=self.user, game=self.game, list_type="unknown")

    def test_deleting_user_removes_only_their_entries_and_preserves_games(self):
        UserGame.objects.create(user=self.user, game=self.game)
        other = UserGame.objects.create(user=self.other_user, game=self.game)
        self.user.delete()
        self.assertEqual(list(UserGame.objects.all()), [other])
        self.assertTrue(Game.objects.filter(pk=self.game.pk).exists())

    def test_deleting_game_removes_its_library_entries(self):
        UserGame.objects.create(user=self.user, game=self.game)
        self.game.delete()
        self.assertFalse(UserGame.objects.exists())
        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())

    def test_admin_lists_library_entries(self):
        admin = get_user_model().objects.create_superuser(
            "test_admin", email="test@example.com", password=None
        )
        UserGame.objects.create(user=self.user, game=self.game, list_type="wishlist")
        self.client.force_login(admin)
        response = self.client.get(reverse("admin:GameShelf_usergame_changelist"))
        self.assertContains(response, "Shared game")
        self.assertContains(response, "collector")
        self.assertContains(response, "Wishlist")
