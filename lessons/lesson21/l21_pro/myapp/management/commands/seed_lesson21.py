from django.core.management.base import BaseCommand

from myapp.models import Article, Category


class Command(BaseCommand):
    help = "Create sample categories and articles for lesson 21."

    def handle(self, *args, **options):
        # --- TASK 02 ---
        category_names = ["Sport", "Technology", "Culture"]
        categories = {
            name: Category.objects.get_or_create(name=name)[0]
            for name in category_names
        }

        # --- TASK 07 08 ---
        articles_data = [
            {
                "title": "How to Start Running",
                "content": (
                    "A beginner guide to building a simple running habit "
                    "without overtraining."
                ),
                "category": categories["Sport"],
            },
            {
                "title": "Best Home Workout Ideas",
                "content": (
                    "A few practical bodyweight exercises you can do at home "
                    "with no equipment."
                ),
                "category": categories["Sport"],
            },
            {
                "title": "Healthy Recovery After Exercise",
                "content": (
                    "Sleep, hydration, and light stretching can improve "
                    "recovery after training."
                ),
                "category": categories["Sport"],
            },
            {
                "title": "Python for Daily Automation",
                "content": (
                    "Python can automate repetitive tasks like file renaming "
                    "and data cleanup."
                ),
                "category": categories["Technology"],
            },
            {
                "title": "Why Version Control Matters",
                "content": (
                    "Git helps teams track changes, collaborate safely, and "
                    "recover earlier versions."
                ),
                "category": categories["Technology"],
            },
            {
                "title": "Understanding Web Frameworks",
                "content": (
                    "Frameworks like Django provide routing, templates, ORM, "
                    "and admin tooling."
                ),
                "category": categories["Technology"],
            },
            {
                "title": "Why Museums Still Matter",
                "content": (
                    "Museums preserve memory, context, and access to important "
                    "cultural works."
                ),
                "category": categories["Culture"],
            },
            {
                "title": "Books That Shape Imagination",
                "content": (
                    "Reading fiction expands vocabulary, empathy, and "
                    "long-form concentration."
                ),
                "category": categories["Culture"],
            },
            {
                "title": "The Role of Film in Society",
                "content": (
                    "Cinema reflects social values and often influences "
                    "public conversations."
                ),
                "category": categories["Culture"],
            },
        ]

        created_count = 0
        for article_data in articles_data:
            _, created = Article.objects.get_or_create(
                title=article_data["title"],
                defaults=article_data,
            )
            created_count += int(created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Categories: {len(categories)}, "
                f"new articles: {created_count}."
            )
        )
