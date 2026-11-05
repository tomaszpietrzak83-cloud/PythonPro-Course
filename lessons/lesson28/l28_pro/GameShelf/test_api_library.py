from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from .models import Game, UserGame


class LibraryWriteTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("api_player")
        cls.other = get_user_model().objects.create_user("api_other_player")
        cls.game = Game.objects.create(title="Demo game")

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.collection = reverse("gameshelf_api:library-list")

    def sign_in(self, user):
        self.client.force_login(user)
        self.client.get(reverse("swagger-ui"))
        self.client.credentials(HTTP_X_CSRFTOKEN=self.client.cookies["csrftoken"].value)

    def test_complete_workflow_and_owned_rule(self):
        self.sign_in(self.user)
        data = {"game": self.game.pk, "list_type": "wishlist", "user": self.other.pk}
        response = self.client.post(self.collection, data, format="json")
        self.assertEqual(response.status_code, 201)
        pk = response.json()["id"]
        url = reverse("gameshelf_api:library-detail", args=[pk])
        self.assertEqual(self.client.get(url).json()["list_type"], "wishlist")
        self.assertEqual(UserGame.objects.get(pk=pk).user, self.user)
        duplicate = self.client.post(self.collection, data, format="json")
        self.assertEqual(duplicate.status_code, 400)
        self.assertIn("game", duplicate.json())

        result = self.client.patch(url, {
            "list_type": "owned", "play_status": "completed", "rating": 9, "note": "Private",
        }, format="json")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["rating"], 9)
        self.assertEqual(result.json()["list_type"], "owned")
        for invalid in ({"rating": 11}, {"rating": 0}, {"list_type": "wishlist"}, {"note": "x" * 5001}):
            self.assertEqual(self.client.patch(url, invalid, format="json").status_code, 400)
        self.assertEqual(self.client.get(url).json()["rating"], 9)
        self.assertIsNone(self.client.patch(url, {"rating": None}, format="json").json()["rating"])
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertFalse(UserGame.objects.filter(pk=pk).exists())
        self.assertTrue(Game.objects.filter(pk=self.game.pk).exists())

    def test_other_users_entry_is_404_for_all_detail_methods(self):
        entry = UserGame.objects.create(user=self.other, game=self.game, note="Private")
        self.sign_in(self.user)
        url = reverse("gameshelf_api:library-detail", args=[entry.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.patch(url, {"note": "Changed"}, format="json").status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)
        entry.refresh_from_db()
        self.assertEqual(entry.note, "Private")

    def test_anonymous_and_missing_csrf_writes_fail(self):
        entry = UserGame.objects.create(user=self.user, game=self.game)
        url = reverse("gameshelf_api:library-detail", args=[entry.pk])
        for signed_in in (False, True):
            if signed_in:
                self.client.force_login(self.user)
            self.assertEqual(self.client.post(self.collection, {}, format="json").status_code, 403)
            self.assertEqual(self.client.patch(url, {"rating": 3}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(url).status_code, 403)
        entry.refresh_from_db()
        self.assertIsNone(entry.rating)
