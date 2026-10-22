from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from .models import Game, UserGame


class LibraryEditTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("editor")
        cls.other = get_user_model().objects.create_user("other_editor")
        cls.game = Game.objects.create(title="Editable game")
        cls.entry = UserGame.objects.create(
            user=cls.user, game=cls.game, note="My private galaxy note"
        )

    def setUp(self):
        self.url = reverse("gameshelf:edit_library_entry", args=[self.entry.pk])

    def test_edit_requires_login(self):
        for method in (self.client.get, self.client.post):
            self.assertEqual(method(self.url).status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.note, "My private galaxy note")

    def test_owner_can_edit_and_cannot_change_user_game_or_list_type(self):
        self.client.force_login(self.user)
        self.assertContains(self.client.get(self.url), self.entry.note)
        other_game = Game.objects.create(title="Different game")
        response = self.client.post(self.url, {
            "play_status": "completed", "rating": 9, "note": "Finished the journey",
            "user": self.other.pk, "game": other_game.pk, "list_type": "wishlist",
        }, follow=True)
        self.assertContains(response, "has been updated")
        self.entry.refresh_from_db()
        self.assertEqual((self.entry.play_status, self.entry.rating, self.entry.note),
                         ("completed", 9, "Finished the journey"))
        self.assertEqual((self.entry.user, self.entry.game, self.entry.list_type),
                         (self.user, self.game, "owned"))

    def test_rating_can_be_cleared_and_boundaries_are_valid(self):
        self.client.force_login(self.user)
        for value, expected in ((1, 1), (10, 10), ("", None)):
            with self.subTest(value=value):
                self.assertEqual(self.client.post(self.url, {
                    "play_status": "playing", "rating": value, "note": "",
                }).status_code, 302)
                self.entry.refresh_from_db()
                self.assertEqual(self.entry.rating, expected)

    def test_invalid_ratings_status_and_oversized_note_do_not_save(self):
        self.client.force_login(self.user)
        invalid = [{"rating": rating} for rating in (-1, 0, 11, "2.5", "text")]
        invalid += [{"play_status": "invalid"}, {"note": "x" * 5001}]
        for values in invalid:
            with self.subTest(values=list(values)):
                response = self.client.post(self.url, {
                    "play_status": "playing", "rating": 7, "note": "Changed", **values,
                })
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
                self.entry.refresh_from_db()
                self.assertEqual(self.entry.note, "My private galaxy note")
                self.assertIsNone(self.entry.rating)

    def test_other_users_and_missing_entries_return_404(self):
        self.client.force_login(self.other)
        for url in (self.url, reverse("gameshelf:edit_library_entry", args=[999999])):
            for method in (self.client.get, self.client.post):
                self.assertEqual(method(url).status_code, 404)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.note, "My private galaxy note")

    def test_private_note_is_not_public_or_visible_in_another_library(self):
        for user in (None, self.other):
            if user:
                self.client.force_login(user)
            for url in (reverse("gameshelf:game_list"),
                        reverse("gameshelf:game_detail", args=[self.game.pk])):
                self.assertNotContains(self.client.get(url), self.entry.note)
        self.assertNotContains(self.client.get(reverse("gameshelf:my_library")), self.entry.note)
        self.client.force_login(self.user)
        self.assertContains(self.client.get(reverse("gameshelf:my_library")), self.entry.note)

    def test_notes_are_escaped_when_displayed(self):
        self.entry.note = '<script>alert("test")</script>'
        self.entry.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse("gameshelf:my_library"))
        self.assertNotContains(response, "<script>alert")
        self.assertContains(response, "&lt;script&gt;")

    def test_edit_post_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(self.url, {"note": "Changed"}).status_code, 403)

    def test_database_rejects_out_of_range_ratings_and_invalid_status(self):
        for changes in ({"rating": 0}, {"rating": 11}, {"play_status": "invalid"}):
            with self.subTest(changes=changes), self.assertRaises(IntegrityError), transaction.atomic():
                UserGame.objects.filter(pk=self.entry.pk).update(**changes)
