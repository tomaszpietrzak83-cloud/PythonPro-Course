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


class WishlistActionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("wish_collector")
        cls.other_user = get_user_model().objects.create_user("other_wish_collector")
        cls.game = Game.objects.create(title="Future Worlds")

    def setUp(self):
        self.url = reverse("gameshelf:add_to_wishlist", args=[self.game.pk])

    def test_anonymous_post_requires_login_without_writing(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("gameshelf:login")))
        self.assertFalse(UserGame.objects.exists())

    def test_authenticated_get_does_not_write(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.assertFalse(UserGame.objects.exists())

    def test_repeated_posts_save_current_users_wishlist_and_preserve_other_user(self):
        other = UserGame.objects.create(user=self.other_user, game=self.game, list_type="owned")
        self.client.force_login(self.user)
        for _ in range(2):
            response = self.client.post(self.url, {"user": self.other_user.pk}, follow=True)
            self.assertContains(response, "is now on your wishlist.")
        entry = UserGame.objects.get(user=self.user, game=self.game)
        other.refresh_from_db()
        self.assertEqual(entry.list_type, "wishlist")
        self.assertEqual(other.list_type, "owned")
        self.assertEqual(UserGame.objects.count(), 2)

    def test_owned_game_is_not_moved_to_wishlist(self):
        entry = UserGame.objects.create(user=self.user, game=self.game, list_type="owned")
        self.client.force_login(self.user)
        response = self.client.post(self.url, follow=True)
        entry.refresh_from_db()
        self.assertEqual(entry.list_type, "owned")
        self.assertEqual(UserGame.objects.count(), 1)
        self.assertContains(response, "already owned")
        self.assertNotContains(response, '>Add to wishlist</button>')

    def test_missing_game_returns_404_without_writing(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("gameshelf:add_to_wishlist", args=[999999]))
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
        self.assertEqual(UserGame.objects.get().list_type, "wishlist")


class MyLibraryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("reader")
        cls.other_user = get_user_model().objects.create_user("other_reader")
        cls.owned_game = Game.objects.create(title="Alpha Owned", description="An owned game")
        cls.wish_game = Game.objects.create(title="Beta Wishlist", description="A future game")
        cls.secret_game = Game.objects.create(title="Other users secret title")
        cls.owned = UserGame.objects.create(user=cls.user, game=cls.owned_game, list_type="owned")
        cls.wish = UserGame.objects.create(user=cls.user, game=cls.wish_game, list_type="wishlist")
        UserGame.objects.create(user=cls.other_user, game=cls.secret_game, list_type="owned")
        UserGame.objects.create(user=cls.other_user, game=cls.wish_game, list_type="owned")

    def test_anonymous_library_requires_login(self):
        response = self.client.get(reverse("gameshelf:my_library"))
        self.assertRedirects(response, reverse("gameshelf:login") + "?next=/library/")

    def test_library_only_contains_current_users_entries(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("gameshelf:my_library"), {"user": self.other_user.pk})
        self.assertEqual(list(response.context["entries"]), [self.owned, self.wish])
        self.assertNotContains(response, self.secret_game.title)
        self.assertContains(response, "Owned")
        self.assertContains(response, "Wishlist")
        self.assertContains(response, reverse("gameshelf:game_detail", args=[self.owned_game.pk]))

    def test_owned_and_wishlist_filters_stay_selected(self):
        self.client.force_login(self.user)
        for list_type, expected in (("owned", self.owned), ("wishlist", self.wish)):
            with self.subTest(list_type=list_type):
                response = self.client.get(reverse("gameshelf:my_library"), {"list_type": list_type})
                self.assertEqual(list(response.context["entries"]), [expected])
                self.assertContains(response, f'value="{list_type}" selected')
                self.assertNotContains(response, self.secret_game.title)

    def test_all_filter_shows_both_lists(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("gameshelf:my_library"), {"list_type": "all"})
        self.assertEqual(list(response.context["entries"]), [self.owned, self.wish])
        self.assertContains(response, 'value="all" selected')

    def test_unknown_filter_shows_error_without_exposing_entries(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("gameshelf:my_library"), {"list_type": "unknown"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["library_form"].errors)
        self.assertFalse(response.context["entries"].exists())

    def test_empty_library_and_empty_filter_show_useful_message(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("gameshelf:my_library"), {"list_type": "wishlist"})
        self.assertContains(response, "No saved games in this view")
        empty_user = get_user_model().objects.create_user("empty_reader")
        self.client.force_login(empty_user)
        response = self.client.get(reverse("gameshelf:my_library"))
        self.assertContains(response, "No saved games in this view")
        self.assertContains(response, "Browse the catalog")

    def test_navigation_only_shows_library_when_logged_in(self):
        response = self.client.get(reverse("gameshelf:home"))
        self.assertNotContains(response, reverse("gameshelf:my_library"))
        self.client.force_login(self.user)
        self.assertContains(self.client.get(reverse("gameshelf:home")), reverse("gameshelf:my_library"))

    def test_library_loads_games_without_a_query_per_entry(self):
        self.client.force_login(self.user)
        # Session + authenticated user + entries with joined games/studios.
        with self.assertNumQueries(3):
            response = self.client.get(reverse("gameshelf:my_library"))
            self.assertEqual(len(response.context["entries"]), 2)
