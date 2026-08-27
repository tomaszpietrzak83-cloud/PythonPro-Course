from django.db import models
from django.utils import timezone


# TASK 02
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)


# TASK 06
class Note(models.Model):
    title = models.CharField(max_length=50, unique=True)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
