model_definition = """
from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    published_date = models.DateTimeField(auto_now_add=True)
"""
