import os
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker

from GameShelf.models import Game, Genre, Studio, Tag, UserGame


SEED_USER_GROUP = "GameShelf seeded users"


class Command(BaseCommand):
    help = "Create reusable FAKE games, optional test users and personal libraries."

    def add_arguments(self, parser):
        parser.add_argument("--games", type=int, default=100)
        parser.add_argument("--seed", type=int, default=28)
        parser.add_argument("--users", type=int, default=0, help="Number of seeded users to create/reuse.")
        parser.add_argument(
            "--entries-per-user", type=int, default=0,
            help="Number of seeded games to save for each seeded user.",
        )
        parser.add_argument(
            "--user-password-env",
            help="Environment variable with a password for NEW users; otherwise login is disabled.",
        )

    def validate_options(self, options):
        if options["games"] < 1:
            raise CommandError("--games must be a positive integer.")
        if options["users"] < 0 or options["entries_per_user"] < 0:
            raise CommandError("--users and --entries-per-user cannot be negative.")
        if options["entries_per_user"] and not options["users"]:
            raise CommandError("--entries-per-user requires --users greater than zero.")
        if options["entries_per_user"] > options["games"]:
            raise CommandError("--entries-per-user cannot exceed --games.")
        password = None
        if options["user_password_env"]:
            password = os.getenv(options["user_password_env"])
            if not password or not password.strip():
                raise CommandError("The password environment variable is missing or empty.")
            try:
                validate_password(password)
            except ValidationError as error:
                raise CommandError("Seed user password: " + " ".join(error.messages)) from error
        return password

    def seed_taxonomy(self, fake, seed):
        fake.seed_instance(seed + 10000)
        genres, tags = [], []
        for model, prefix, count, target in (
            (Genre, "theme", 4, genres), (Tag, "feature", 6, tags),
        ):
            for number in range(1, count + 1):
                item, _ = model.objects.get_or_create(
                    slug=f"fake-{prefix}-{number:02d}",
                    defaults={"name": f"FAKE {prefix.title()} {number:02d}: {fake.word().title()}"},
                )
                target.append(item)
        return genres, tags

    def seed_users(self, count, fake, seed, password):
        if not count:
            return [], 0
        group, _ = Group.objects.get_or_create(name=SEED_USER_GROUP)
        if group.permissions.exists():
            raise CommandError("The seeded-user marker group must not grant permissions.")
        users, created_count = [], 0
        for number in range(1, count + 1):
            username = f"gameshelf_fake_{number:03d}"
            user = get_user_model().objects.filter(username=username).first()
            if user is None:
                fake.seed_instance(seed + 20000 + number)
                user = get_user_model().objects.create_user(
                    username=username, password=password,
                    email=f"gameshelf-fake-{number:03d}@example.invalid",
                    first_name=fake.first_name(), last_name=fake.last_name(),
                )
                user.groups.add(group)
                created_count += 1
            elif not user.groups.filter(pk=group.pk).exists():
                raise CommandError(
                    f"Username {username} belongs to a non-seeded user; nothing was changed."
                )
            users.append(user)
        return users, created_count

    def seed_libraries(self, users, games, count, fake, seed):
        created_count = 0
        for number, user in enumerate(users, start=1):
            fake.seed_instance(seed + 30000 + number)
            for index, game in enumerate(games[:count]):
                list_type = UserGame.ListType.WISHLIST
                status = UserGame.PlayStatus.NOT_STARTED
                rating = None
                if index % 2 == 0:
                    list_type = UserGame.ListType.OWNED
                    status = fake.random_element(UserGame.PlayStatus.values)
                    if status in (UserGame.PlayStatus.COMPLETED, UserGame.PlayStatus.PLAYING):
                        rating = fake.random_int(min=1, max=10)
                _, created = UserGame.objects.get_or_create(
                    user=user, game=game,
                    defaults={
                        "list_type": list_type, "play_status": status,
                        "rating": rating,
                        "note": f"FAKE demo note: {fake.sentence(nb_words=8)}",
                    },
                )
                created_count += int(created)
        return created_count

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["games"]
        password = self.validate_options(options)

        genre, _ = Genre.objects.get_or_create(slug="fake", defaults={"name": "FAKE"})
        tag, _ = Tag.objects.get_or_create(slug="fake", defaults={"name": "FAKE"})
        fake = Faker("en_US")
        genres, tags = self.seed_taxonomy(fake, options["seed"])
        created_count = 0
        games = []
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
            game.genres.add(genres[(number - 1) % len(genres)])
            game.tags.add(tags[(number - 1) % len(tags)])
            games.append(game)

        users, users_created = self.seed_users(options["users"], fake, options["seed"], password)
        entries_created = self.seed_libraries(
            users, games, options["entries_per_user"], fake, options["seed"]
        )

        self.stdout.write(self.style.SUCCESS(
            f"Created {created_count}; reused {count - created_count} FAKE games.\n"
            f"Users: created {users_created}; reused {len(users) - users_created}.\n"
            f"Library entries: created {entries_created}; "
            f"reused {len(users) * options['entries_per_user'] - entries_created}."
        ))
