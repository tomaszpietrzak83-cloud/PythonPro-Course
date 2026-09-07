from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
