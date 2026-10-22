from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import Game, Genre, Studio, Tag, UserGame


class GameShelfAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            "catalog_admin", "admin@example.com", password=None
        )
        cls.user = get_user_model().objects.create_user("catalog_player")
        cls.studio = Studio.objects.create(name="Catalog Studio")
        cls.game = Game.objects.create(title="Admin Orbit", studio=cls.studio)
        cls.empty_game = Game.objects.create(title="Empty Orbit")
        cls.genre = Genre.objects.get(slug="action")
        cls.tag = Tag.objects.get(slug="singleplayer")
        cls.game.genres.add(cls.genre)
        cls.game.tags.add(cls.tag)
        cls.entry = UserGame.objects.create(
            user=cls.user, game=cls.game, play_status="playing", rating=8
        )
        UserGame.objects.create(user=cls.admin_user, game=cls.game, list_type="wishlist")

    def setUp(self):
        self.client.force_login(self.admin_user)

    def test_all_model_lists_render_with_search_and_counts(self):
        for model, search in ((Game, "Admin Orbit"), (Studio, "Catalog Studio"),
                              (Genre, "Action"), (Tag, "Singleplayer"), (UserGame, "catalog_player")):
            with self.subTest(model=model):
                response = self.client.get(
                    reverse(f"admin:GameShelf_{model._meta.model_name}_changelist"), {"q": search}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context["cl"].result_count, 1)

    def test_annotated_counts_are_correct_without_per_row_queries(self):
        request = RequestFactory().get("/admin/")
        request.user = self.admin_user
        model_admin = admin.site._registry[Game]
        # Add an extra genre to catch accidentally multiplied aggregate counts.
        self.game.genres.add(Genre.objects.get(slug="adventure"))
        with self.assertNumQueries(1):
            games = list(model_admin.get_queryset(request).order_by("title"))
            self.assertEqual([model_admin.saved_by(game) for game in games], [2, 0])
        for model, obj in ((Studio, self.studio), (Genre, self.genre), (Tag, self.tag)):
            model_admin = admin.site._registry[model]
            with self.assertNumQueries(1):
                counted = model_admin.get_queryset(request).get(pk=obj.pk)
                self.assertEqual(model_admin.game_count(counted), 1)

    def test_admin_filters_entries_by_progress_and_rating(self):
        response = self.client.get(reverse("admin:GameShelf_usergame_changelist"), {
            "play_status__exact": "playing", "rating__exact": 8,
        })
        self.assertEqual(list(response.context["cl"].result_list), [self.entry])

    def test_game_change_page_contains_library_inline_without_private_notes(self):
        response = self.client.get(reverse("admin:GameShelf_game_change", args=[self.game.pk]))
        self.assertContains(response, 'name="library_entries-TOTAL_FORMS"')
        self.assertContains(response, "catalog_player")
        self.assertNotContains(response, 'name="library_entries-0-note"')
        self.assertEqual(self.client.get(reverse("admin:GameShelf_game_add")).status_code, 200)

    def test_list_editing_saves_progress_and_rejects_invalid_rating(self):
        url = reverse("admin:GameShelf_usergame_changelist")
        data = {
            "form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "1",
            "form-MIN_NUM_FORMS": "0", "form-MAX_NUM_FORMS": "1000",
            "form-0-id": str(self.entry.pk), "form-0-list_type": "owned",
            "form-0-play_status": "completed", "form-0-rating": "10", "_save": "Save",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual((self.entry.play_status, self.entry.rating), ("completed", 10))
        response = self.client.post(url, {**data, "form-0-rating": "11"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["cl"].formset.errors)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.rating, 10)

    def test_regular_users_cannot_access_admin_lists(self):
        self.client.force_login(self.user)
        for model in (Game, Studio, Genre, Tag, UserGame):
            url = reverse(f"admin:GameShelf_{model._meta.model_name}_changelist")
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse("admin:login")))
