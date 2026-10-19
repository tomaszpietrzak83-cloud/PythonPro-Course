from django.core.management.base import BaseCommand
from laboratory.models import Category, Product


class Command(BaseCommand):
    help = "Uzupełnia dane demonstracyjne bez nadpisywania istniejących produktów."

    def handle(self, *args, **options):
        stationery, _ = Category.objects.get_or_create(id=1, defaults={"name": "Papier i biuro"})
        electronics, _ = Category.objects.get_or_create(id=2, defaults={"name": "Elektronika"})
        for pk, name, price, category in [
            (1, "Notatnik", "24.90", stationery),
            (2, "Pióro", "39.00", stationery),
            (3, "Klawiatura", "149.00", electronics),
        ]:
            Product.objects.get_or_create(id=pk, defaults={"name": name, "price": price, "category": category})
        self.stdout.write(self.style.SUCCESS("Dane demonstracyjne gotowe."))
