from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
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


class OwnedActionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("owner")
        cls.other_user = get_user_model().objects.create_user("other_owner")
        cls.game = Game.objects.create(title="Orbit Adventures")

    def setUp(self):
        self.url = reverse("gameshelf:add_to_owned", args=[self.game.pk])

    def test_anonymous_post_requires_login_without_writing(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("gameshelf:login")))
        self.assertFalse(UserGame.objects.exists())

    def test_authenticated_get_does_not_write(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.assertFalse(UserGame.objects.exists())

    def test_repeated_posts_create_one_owned_entry_for_current_user(self):
        self.client.force_login(self.user)
        for _ in range(2):
            response = self.client.post(self.url, {"user": self.other_user.pk}, follow=True)
            self.assertContains(response, "is now in your owned games.")
            self.assertContains(response, "In your library:")
        entry = UserGame.objects.get()
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.list_type, "owned")

    def test_wishlist_moves_to_owned_and_preserves_other_users_entry(self):
        entry = UserGame.objects.create(user=self.user, game=self.game, list_type="wishlist")
        other = UserGame.objects.create(user=self.other_user, game=self.game, list_type="wishlist")
        self.client.force_login(self.user)
        self.client.post(self.url)
        entry.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(entry.list_type, "owned")
        self.assertEqual(other.list_type, "wishlist")
        self.assertEqual(UserGame.objects.count(), 2)

    def test_missing_game_returns_404_without_writing(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("gameshelf:add_to_owned", args=[999999]))
        self.assertEqual(response.status_code, 404)
        self.assertFalse(UserGame.objects.exists())

    def test_post_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(self.url).status_code, 403)
        self.assertFalse(UserGame.objects.exists())
        client.get(reverse("gameshelf:game_detail", args=[self.game.pk]))
        response = client.post(self.url, {"csrfmiddlewaretoken": client.cookies["csrftoken"].value})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserGame.objects.get().list_type, "owned")
