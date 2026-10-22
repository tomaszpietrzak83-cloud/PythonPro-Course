from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Game, UserGame


class LibraryRemovalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("remover")
        cls.other = get_user_model().objects.create_user("other_remover")
        cls.game = Game.objects.create(title="Shared catalog game")
        cls.entry = UserGame.objects.create(user=cls.user, game=cls.game, note="Private note")
        cls.other_entry = UserGame.objects.create(user=cls.other, game=cls.game)

    def setUp(self):
        self.url = reverse("gameshelf:remove_library_entry", args=[self.entry.pk])

    def test_get_displays_confirmation_without_deleting(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(response, self.game.title)
        self.assertContains(response, "Yes, remove from my library")
        self.assertContains(response, "Cancel and keep this game")
        self.assertEqual(UserGame.objects.count(), 2)

    def test_post_deletes_only_current_users_entry_and_keeps_catalog_game(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, follow=True)
        self.assertContains(response, "has been removed from your library")
        self.assertFalse(UserGame.objects.filter(pk=self.entry.pk).exists())
        self.assertTrue(UserGame.objects.filter(pk=self.other_entry.pk).exists())
        self.assertTrue(Game.objects.filter(pk=self.game.pk).exists())
        self.assertNotContains(response, "Private note")

    def test_other_user_cannot_view_confirmation_or_delete(self):
        self.client.force_login(self.other)
        for method in (self.client.get, self.client.post):
            self.assertEqual(method(self.url).status_code, 404)
        self.assertEqual(UserGame.objects.count(), 2)

    def test_anonymous_requests_require_login(self):
        for method in (self.client.get, self.client.post):
            self.assertEqual(method(self.url).status_code, 302)
        self.assertEqual(UserGame.objects.count(), 2)

    def test_missing_entry_returns_404(self):
        self.client.force_login(self.user)
        url = reverse("gameshelf:remove_library_entry", args=[999999])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.post(url).status_code, 404)

    def test_csrf_is_required_to_delete(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(self.url).status_code, 403)
        self.assertTrue(UserGame.objects.filter(pk=self.entry.pk).exists())
        client.get(self.url)
        response = client.post(self.url, {"csrfmiddlewaretoken": client.cookies["csrftoken"].value})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(UserGame.objects.filter(pk=self.entry.pk).exists())

    def test_other_http_methods_cannot_delete(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.delete(self.url).status_code, 405)
        self.assertTrue(UserGame.objects.filter(pk=self.entry.pk).exists())
