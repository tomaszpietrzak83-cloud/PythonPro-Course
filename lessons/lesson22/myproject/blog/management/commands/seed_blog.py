import random

from blog.models import Category, Post, Tag
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker


# TASK 07 09
class Command(BaseCommand):
    help = "Seeds the database with categories and posts"

    def handle(self, *args, **kwargs):
        fake = Faker("en_US")

        # TASK 07 09
        self.stdout.write("Cleaning old data...")
        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()

        # TASK 07
        category_names = [
            "Technology",
            "Travel",
            "Food",
            "Health",
            "Sports",
            "Business",
            "Science",
            "Entertainment",
            "People",
            "Places",
        ]

        categories = []
        for name in category_names:
            category = Category.objects.create(name=name)
            categories.append(category)

        # TASK 09
        tag_names = [
            "python",
            "django",
            "web",
            "orm",
            "database",
            "tutorial",
            "api",
            "testing",
            "frontend",
            "backend",
        ]

        Tag.objects.bulk_create([Tag(name=name) for name in tag_names])
        tags = list(Tag.objects.all())

        self.stdout.write(f"Created {len(categories)} categories.")

        # TASK 07
        posts = []
        for _ in range(100):
            posts.append(
                Post(
                    title=fake.sentence(nb_words=10),
                    content=" ".join(fake.paragraphs(nb=4)),
                    publication_date=fake.date_time_this_year(
                        tzinfo=timezone.get_current_timezone()
                    ),
                    category=random.choice(categories),
                )
            )

        Post.objects.bulk_create(posts)

        # TASK 09
        posts = list(Post.objects.all())

        for post in posts:
            selected_tags = random.sample(tags, k=random.randint(1, 5))
            post.tags.add(*selected_tags)

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
        self.stdout.write(f"Created {len(posts)} posts.")
        self.stdout.write(f"Created {len(tags)} tags.")
