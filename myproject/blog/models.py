from django.db import models
from django.utils import timezone


# TASK 01
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# TASK 08
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
    # TASK 01
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # TASK 08
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
