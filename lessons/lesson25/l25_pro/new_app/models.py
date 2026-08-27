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


# TASK 09
class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# TASK 09
class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    publication_year = models.CharField(max_length=4)
    # TASK 09
    author = models.ForeignKey(Author, verbose_name="", on_delete=models.CASCADE)
