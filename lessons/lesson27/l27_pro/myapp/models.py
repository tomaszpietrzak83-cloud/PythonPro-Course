from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    short_description = models.CharField(max_length=200, default=("empty"))


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)

    def __str__(self):
        return self.name
