from django.db import models


# --- TASK 03 ---
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(
        "Category",
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


# --- TASK 08 ---
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
