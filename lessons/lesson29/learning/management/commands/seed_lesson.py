from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from learning.models import LogEntry


class Command(BaseCommand):
    help = "Create local educational fixtures without replacing existing data."

    def handle(self, *args, **options):
        for name in ("anna", "jan", "alex"):
            get_user_model().objects.get_or_create(username=name, defaults={"email": f"{name}@example.com"})
        for days in (120, 100, 30, 1):
            LogEntry.objects.get_or_create(message=f"Example: {days} days old", defaults={"created_at": timezone.now() - timedelta(days=days)})
