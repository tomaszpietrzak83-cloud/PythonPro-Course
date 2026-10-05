from django.db import models


class Studio(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ("name", "pk")

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    studio = models.ForeignKey(
        Studio, on_delete=models.SET_NULL, null=True, blank=True, related_name="games"
    )

    def __str__(self):
        return self.title
