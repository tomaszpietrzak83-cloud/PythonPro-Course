from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from notes.models import Note


# TASK 25
class Command(BaseCommand):
    help = "Dodaje przykładowe notatki wskazanemu użytkownikowi z istniejącej bazy."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            required=True,
            help="Nazwa użytkownika, któremu przypisać przykładowe notatki.",
        )

    def handle(self, *args, **options):
        user_model = get_user_model()
        username = options["username"]

        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist as exc:
            raise CommandError(
                f"Nie znaleziono użytkownika {username!r}. "
                "Polecenie nie tworzy użytkowników."
            ) from exc

        samples = [
            ("Plan nauki", "Powtórzyć middleware i JWT."),
            ("Pomysł na API", "Sprawdzić filtrowanie notatek po właścicielu."),
        ]
        created_count = 0

        for title, content in samples:
            _, created = Note.objects.get_or_create(
                owner=user,
                title=title,
                defaults={"content": content},
            )
            created_count += int(created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Użytkownik {username!r}: dodano {created_count} przykładowych "
                "notatek (istniejące rekordy pozostawiono bez zmian)."
            )
        )
