from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ["id"]
