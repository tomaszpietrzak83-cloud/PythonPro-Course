from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker

from GameShelf.models import Game, Genre, Studio, Tag


class Command(BaseCommand):
    help = "Create reusable fictional games, marked with the FAKE genre and tag."

    def add_arguments(self, parser):
        parser.add_argument("--games", type=int, default=100)
        parser.add_argument("--seed", type=int, default=28)

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["games"]
        if count < 1:
            raise CommandError("--games must be a positive integer.")

        genre, _ = Genre.objects.get_or_create(slug="fake", defaults={"name": "FAKE"})
        tag, _ = Tag.objects.get_or_create(slug="fake", defaults={"name": "FAKE"})
        fake = Faker("en_US")
        created_count = 0
        for number in range(1, count + 1):
            seed_key = f"gameshelf-fake-{number:04d}"
            game = Game.objects.filter(seed_key=seed_key).first()
            if game is None:
                # Per-record seeds keep earlier titles stable when --games changes.
                fake.seed_instance(options["seed"] + number)
                title = f"FAKE {number:03d}: {fake.sentence(nb_words=4).rstrip('.')}"
                description = fake.paragraph(nb_sentences=4)
                release_date = fake.date_between(
                    start_date=date(1980, 1, 1), end_date=date(2026, 1, 1)
                )
                studio, _ = Studio.objects.get_or_create(
                    name=f"FAKE {fake.company()}"[:120]
                )
                game, created = Game.objects.get_or_create(
                    seed_key=seed_key,
                    defaults={
                        "title": title[:120], "description": description,
                        "release_date": release_date, "studio": studio,
                    },
                )
                created_count += int(created)
            game.genres.add(genre)
            game.tags.add(tag)

        self.stdout.write(self.style.SUCCESS(
            f"Created {created_count}; reused {count - created_count} FAKE games."
        ))
