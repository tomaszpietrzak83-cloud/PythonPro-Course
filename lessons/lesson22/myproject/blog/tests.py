from django.core.management import call_command
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Author, Category, Post, PostTag, Tag


class SearchSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.technology = Category.objects.create(name="Technology")
        cls.travel = Category.objects.create(name="Travel")
        cls.tom = Author.objects.create(first_name="Thomas", last_name="Stone")
        cls.jane = Author.objects.create(first_name="Jane", last_name="River")
        cls.django = Tag.objects.create(name="django")
        cls.travel_tag = Tag.objects.create(name="travel")

        cls.matching_post = Post.objects.create(
            title="Practical Python patterns",
            content="A detailed guide to useful Python techniques.",
            publication_date=timezone.now(),
            category=cls.technology,
            author=cls.tom,
        )
        PostTag.objects.create(post=cls.matching_post, tag=cls.django)
        cls.other_post = Post.objects.create(
            title="A weekend by the sea",
            content="A calm route through small coastal towns.",
            publication_date=timezone.now(),
            category=cls.travel,
            author=cls.jane,
        )
        PostTag.objects.create(post=cls.other_post, tag=cls.travel_tag)

    def test_empty_search_url_shows_form_without_results(self):
        response = self.client.get(reverse("blog:article_search"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["submitted"])
        self.assertContains(response, "Find the article you remember")

    def test_keywords_and_tags_create_match_score_and_hide_zero_matches(self):
        response = self.client.get(
            reverse("blog:article_search"),
            {"keyword": ["python", "rust"], "tag": "django"},
        )

        results = list(response.context["page_obj"])
        self.assertEqual(results, [self.matching_post])
        self.assertEqual(results[0].match_count, 2)
        self.assertEqual(results[0].criteria_count, 3)
        self.assertEqual(results[0].match_percent, 67)
        self.assertContains(response, "67% match")

    def test_author_fragments_are_combined_with_or(self):
        response = self.client.get(
            reverse("blog:article_search"),
            {"author": ["tho", "Jane"]},
        )

        self.assertEqual(response.context["result_count"], 2)

    def test_multiple_categories_are_combined_with_or(self):
        response = self.client.get(
            reverse("blog:article_search"),
            {"category": [str(self.technology.pk), str(self.travel.pk)]},
        )

        self.assertEqual(response.context["result_count"], 2)

    def test_invalid_or_reversed_dates_show_validation_message(self):
        invalid = self.client.get(
            reverse("blog:article_search"), {"from": "not-a-date"}
        )
        reversed_range = self.client.get(
            reverse("blog:article_search"),
            {"from": "2026-09-10", "to": "2026-09-01"},
        )

        self.assertContains(invalid, "The start date is invalid")
        self.assertContains(
            reversed_range, "The start date cannot be later than the end date"
        )

    def test_autocomplete_starts_after_three_characters(self):
        url = reverse("blog:author_suggestions")

        self.assertJSONEqual(self.client.get(url, {"q": "th"}).content, [])
        self.assertJSONEqual(
            self.client.get(url, {"q": "tho"}).content,
            [{"value": "Thomas Stone", "text": "Thomas Stone"}],
        )

    def test_pagination_displays_five_results_per_page(self):
        for number in range(5):
            Post.objects.create(
                title=f"Python extra {number}",
                content="python",
                category=self.technology,
                author=self.tom,
            )

        response = self.client.get(
            reverse("blog:article_search"), {"keyword": "python"}
        )

        self.assertEqual(response.context["result_count"], 6)
        self.assertEqual(len(response.context["page_obj"]), 5)
        self.assertEqual(response.context["page_obj"].paginator.num_pages, 2)

    def test_deleting_author_preserves_post_with_placeholder(self):
        self.tom.delete()

        self.matching_post.refresh_from_db()
        self.assertEqual(self.matching_post.author.full_name, "Author deleted")
        self.assertTrue(self.matching_post.author.is_placeholder)

    def test_used_category_is_protected(self):
        with self.assertRaises(ProtectedError):
            self.technology.delete()

    def test_deleting_tag_does_not_delete_post(self):
        self.django.delete()

        self.assertTrue(Post.objects.filter(pk=self.matching_post.pk).exists())
        self.assertFalse(
            PostTag.objects.filter(post_id=self.matching_post.pk).exists()
        )


class SeederTests(TestCase):
    def test_seeder_creates_requested_dataset(self):
        call_command("seed_blog", verbosity=0)

        self.assertEqual(Post.objects.count(), 2000)
        self.assertEqual(Author.objects.filter(is_placeholder=False).count(), 90)
        self.assertEqual(Tag.objects.count(), 40)
        self.assertTrue(PostTag.objects.exists())
        self.assertFalse(Author.objects.filter(post__isnull=True).exists())
