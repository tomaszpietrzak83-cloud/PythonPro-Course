from django.test import TestCase
from django.urls import reverse

from .models import Article, Category


class Lesson21ViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Sport")
        Article.objects.create(
            title="How to Start Running",
            content="Training basics.",
            category=self.category,
        )
        Article.objects.create(
            title="Hidden Draft",
            content="This article should not be visible.",
            category=self.category,
            is_published=False,
        )

    # --- TASK 03 ---
    def test_category_list_view_displays_categories(self):
        response = self.client.get(reverse("myapp:category_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sport")

    # --- TASK 06 07 ---
    def test_category_detail_view_displays_related_articles(self):
        response = self.client.get(
            reverse("myapp:category_detail", args=[self.category.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How to Start Running")

    def test_category_detail_view_returns_404_for_missing_category(self):
        response = self.client.get(reverse("myapp:category_detail", args=[999]))

        self.assertEqual(response.status_code, 404)

    # --- TASK 08 ---
    def test_article_list_view_hides_unpublished_articles(self):
        response = self.client.get(reverse("myapp:article_list"))

        self.assertContains(response, "How to Start Running")
        self.assertNotContains(response, "Hidden Draft")

    # --- TASK 10 ---
    def test_article_list_view_filters_by_query(self):
        response = self.client.get(reverse("myapp:article_list"), {"q": "running"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How to Start Running")
        self.assertNotContains(response, "Hidden Draft")
