from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Game, Genre, Studio, Tag, UserGame


class PlayerWorkflowTests(TestCase):
    """Exercise connected HTML flows with real sessions and CSRF checks."""

    @classmethod
    def setUpTestData(cls):
        studio = Studio.objects.create(name="Workflow Studio")
        cls.game = Game.objects.create(
            title="Workflow Orbit",
            description="Explore a new world",
            studio=studio,
        )
        cls.game.genres.add(Genre.objects.get(slug="action"))
        cls.game.tags.add(Tag.objects.get(slug="singleplayer"))

    def post_form(self, client, url, data=None, form_url=None):
        page = client.get(form_url or url)
        self.assertEqual(page.status_code, 200)
        return client.post(
            url,
            {
                **(data or {}),
                "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
            },
        )

    def register_and_login(self, username):
        client = Client(enforce_csrf_checks=True)
        password = "Workflow-Only-Nebula!8742"
        response = self.post_form(
            client,
            reverse("gameshelf:register"),
            {
                "username": username,
                "password1": password,
                "password2": password,
            },
        )
        self.assertRedirects(response, reverse("gameshelf:login"))
        response = self.post_form(
            client,
            reverse("gameshelf:login"),
            {
                "username": username,
                "password": password,
                "next": reverse("gameshelf:my_library"),
            },
        )
        self.assertRedirects(response, reverse("gameshelf:my_library"))
        return client

    def test_register_discover_save_edit_remove_and_logout(self):
        detail = reverse("gameshelf:game_detail", args=[self.game.pk])
        response = self.client.get(
            reverse("gameshelf:game_list"),
            {
                "q": "Orbit",
                "genre": "action",
                "tag": "singleplayer",
            },
        )
        self.assertContains(response, self.game.title)
        self.assertContains(response, "cover-placeholder.svg")
        client = self.register_and_login("workflow_player")
        wishlist = reverse("gameshelf:add_to_wishlist", args=[self.game.pk])
        self.assertRedirects(
            self.post_form(client, wishlist, form_url=detail), detail
        )
        entry = UserGame.objects.get()
        original_pk = entry.pk
        self.assertEqual(entry.list_type, "wishlist")
        self.post_form(client, wishlist, form_url=detail)
        self.assertEqual(UserGame.objects.count(), 1)
        self.post_form(
            client,
            reverse("gameshelf:add_to_owned", args=[self.game.pk]),
            form_url=detail,
        )
        entry.refresh_from_db()
        self.assertEqual((entry.pk, entry.list_type), (original_pk, "owned"))
        edit_url = reverse("gameshelf:edit_library_entry", args=[entry.pk])
        response = self.post_form(
            client,
            edit_url,
            {
                "play_status": "completed",
                "rating": 10,
                "note": "Workflow private note",
            },
        )
        self.assertRedirects(response, reverse("gameshelf:my_library"))
        self.assertContains(
            client.get(reverse("gameshelf:my_library")), "Workflow private note"
        )
        self.assertNotContains(self.client.get(detail), "Workflow private note")
        remove_url = reverse("gameshelf:remove_library_entry", args=[entry.pk])
        self.assertRedirects(
            self.post_form(client, remove_url), reverse("gameshelf:my_library")
        )
        self.assertFalse(UserGame.objects.exists())
        self.assertTrue(Game.objects.filter(pk=self.game.pk).exists())
        response = self.post_form(
            client,
            reverse("gameshelf:logout"),
            form_url=reverse("gameshelf:my_library"),
        )
        self.assertRedirects(response, reverse("gameshelf:home"))
        self.assertNotIn("_auth_user_id", client.session)

    def test_two_real_sessions_cannot_read_edit_or_remove_each_others_entries(
        self,
    ):
        owner = self.register_and_login("workflow_owner")
        visitor = self.register_and_login("workflow_visitor")
        detail = reverse("gameshelf:game_detail", args=[self.game.pk])
        self.post_form(
            owner,
            reverse("gameshelf:add_to_owned", args=[self.game.pk]),
            form_url=detail,
        )
        entry = UserGame.objects.get(user__username="workflow_owner")
        self.post_form(
            owner,
            reverse("gameshelf:edit_library_entry", args=[entry.pk]),
            {
                "play_status": "playing",
                "rating": 8,
                "note": "Owner-only secret",
            },
        )
        library_url = reverse("gameshelf:my_library")
        self.assertNotContains(visitor.get(library_url), "Owner-only secret")
        visitor.get(library_url)  # Obtain this session's valid CSRF token.
        for name in ("edit_library_entry", "remove_library_entry"):
            url = reverse(f"gameshelf:{name}", args=[entry.pk])
            self.assertEqual(visitor.get(url).status_code, 404)
            response = visitor.post(
                url,
                {
                    "csrfmiddlewaretoken": visitor.cookies["csrftoken"].value,
                    "play_status": "abandoned",
                    "note": "Tampered",
                    "rating": 1,
                },
            )
            self.assertEqual(response.status_code, 404)
        entry.refresh_from_db()
        self.assertEqual((entry.note, entry.rating), ("Owner-only secret", 8))
        self.assertEqual(
            entry.user, get_user_model().objects.get(username="workflow_owner")
        )
