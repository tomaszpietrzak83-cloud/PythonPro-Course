from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    short_description = models.CharField(max_length=200, default="empty")

    def __str__(self):
        return self.name
