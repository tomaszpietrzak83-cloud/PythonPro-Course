from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    password = "Test-Only-Orbit!4829"

    def registration_data(self, **overrides):
        return {
            "username": "new_player",
            "password1": self.password,
            "password2": self.password,
            **overrides,
        }

    def test_registration_creates_regular_user_with_hashed_password(self):
        response = self.client.post(
            reverse("gameshelf:register"), self.registration_data()
        )
        self.assertRedirects(response, reverse("gameshelf:login"))
        user = get_user_model().objects.get(username="new_player")
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertNotEqual(user.password, self.password)

    def test_registration_rejects_mismatch_weak_password_and_duplicate_username(
        self,
    ):
        url = reverse("gameshelf:register")
        for data in (
            self.registration_data(password2="Different!8294"),
            self.registration_data(password1="123", password2="123"),
        ):
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)
        self.assertFalse(get_user_model().objects.exists())
        self.client.post(url, self.registration_data())
        response = self.client.post(url, self.registration_data())
        self.assertIn("username", response.context["form"].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_login_navigation_and_post_logout(self):
        user = get_user_model().objects.create_user(
            "player", password=self.password
        )
        response = self.client.post(
            reverse("gameshelf:login"),
            {
                "username": user.username,
                "password": self.password,
            },
        )
        self.assertRedirects(response, reverse("gameshelf:game_list"))
        page = self.client.get(reverse("gameshelf:home"))
        self.assertContains(page, "Log out")
        self.assertNotContains(page, ">Register</a>")
        self.assertEqual(
            self.client.get(reverse("gameshelf:logout")).status_code, 405
        )
        self.assertIn("_auth_user_id", self.client.session)
        response = self.client.post(reverse("gameshelf:logout"))
        self.assertRedirects(response, reverse("gameshelf:home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_invalid_login_and_external_next_are_safe(self):
        user = get_user_model().objects.create_user(
            "player", password=self.password
        )
        url = reverse("gameshelf:login")
        response = self.client.post(
            url, {"username": "player", "password": "wrong"}
        )
        self.assertTrue(response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(
            url,
            {
                "username": user.username,
                "password": self.password,
                "next": "https://example.com/untrusted",
            },
        )
        self.assertRedirects(response, reverse("gameshelf:game_list"))

    def test_login_respects_local_next(self):
        get_user_model().objects.create_user("player", password=self.password)
        target = reverse("gameshelf:game_list") + "?genre=action"
        response = self.client.post(
            reverse("gameshelf:login"),
            {
                "username": "player",
                "password": self.password,
                "next": target,
            },
        )
        self.assertRedirects(response, target)

    def test_auth_forms_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        for name in ("login", "register"):
            url = reverse(f"gameshelf:{name}")
            self.assertEqual(client.get(url).status_code, 200)
            self.assertEqual(
                client.post(url, self.registration_data()).status_code, 403
            )

    def test_authenticated_user_cannot_register_another_account(self):
        user = get_user_model().objects.create_user("player")
        self.client.force_login(user)
        response = self.client.post(
            reverse("gameshelf:register"), self.registration_data()
        )
        self.assertRedirects(response, reverse("gameshelf:game_list"))
        self.assertEqual(get_user_model().objects.count(), 1)
