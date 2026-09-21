import random
import subprocess
import sys
from pathlib import Path

# Running this file directly delegates to manage.py using the main course environment.
# This block must precede Django imports, which require initialized settings.
if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[3]
    course_dir = project_dir.parents[2]
    venv_dir = course_dir / ".venv"
    python_path = (
        venv_dir / "Scripts" / "python.exe"
        if sys.platform == "win32"
        else venv_dir / "bin" / "python"
    )
    if not python_path.is_file():
        raise SystemExit(
            f"Main course environment Python not found: {python_path}"
        )

    result = subprocess.run(
        [
            str(python_path),
            str(project_dir / "manage.py"),
            "seed_blog",
            *sys.argv[1:],
        ],
        cwd=project_dir,
    )
    raise SystemExit(result.returncode)

from blog.models import Author, Category, Post, PostTag, Tag
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker


# TASK 07 09
class Command(BaseCommand):
    help = "Seeds the database with categories, authors, tags and 2,000 posts"

    def handle(self, *args, **kwargs):
        fake = Faker("en_US")

        # SEARCH-SITE: Delete dependants first so PROTECT never blocks cleanup.
        self.stdout.write("Cleaning old data...")
        Post.objects.all().delete()
        Author.objects.all().delete()
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
            "security",
            "performance",
            "deployment",
            "docker",
            "linux",
            "windows",
            "cloud",
            "devops",
            "javascript",
            "html",
            "css",
            "accessibility",
            "design",
            "architecture",
            "clean-code",
            "git",
            "automation",
            "data-science",
            "machine-learning",
            "ai",
            "analytics",
            "sql",
            "sqlite",
            "postgresql",
            "rest",
            "authentication",
            "forms",
            "pagination",
            "search",
            "beginners",
        ]

        Tag.objects.bulk_create([Tag(name=name) for name in tag_names])
        tags = list(Tag.objects.all())

        # SEARCH-SITE: Faker supplies 90 unique people for the Author table.
        author_names = set()
        while len(author_names) < 90:
            author_names.add((fake.first_name(), fake.last_name()))
        Author.objects.bulk_create(
            [
                Author(first_name=first_name, last_name=last_name)
                for first_name, last_name in author_names
            ]
        )
        authors = list(Author.objects.filter(is_placeholder=False))

        self.stdout.write(f"Created {len(categories)} categories.")
        self.stdout.write(f"Created {len(authors)} authors.")

        # TASK 07
        posts = []
        guaranteed_authors = authors.copy()
        random.shuffle(guaranteed_authors)
        for index in range(2000):
            posts.append(
                Post(
                    title=fake.sentence(nb_words=10),
                    content=" ".join(fake.paragraphs(nb=4)),
                    publication_date=fake.date_time_this_year(
                        tzinfo=timezone.get_current_timezone()
                    ),
                    category=random.choice(categories),
                    author=(
                        guaranteed_authors[index]
                        if index < len(guaranteed_authors)
                        else random.choice(authors)
                    ),
                )
            )

        Post.objects.bulk_create(posts)

        # TASK 09
        posts = list(Post.objects.all())

        post_tags = []
        for post in posts:
            selected_tags = random.sample(tags, k=random.randint(1, 5))
            post_tags.extend(
                PostTag(post=post, tag=tag) for tag in selected_tags
            )
        PostTag.objects.bulk_create(post_tags)

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
        self.stdout.write(f"Created {len(posts)} posts.")
        self.stdout.write(f"Created {len(tags)} tags.")
