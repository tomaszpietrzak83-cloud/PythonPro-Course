from django.conf import settings
from django.db import models


class Studio(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ("name", "pk")

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Game(models.Model):
    seed_key = models.CharField(max_length=80, unique=True, null=True, blank=True, editable=False)
    title = models.CharField(max_length=120)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    studio = models.ForeignKey(
        Studio, on_delete=models.SET_NULL, null=True, blank=True, related_name="games"
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name="games")
    tags = models.ManyToManyField(Tag, blank=True, related_name="games")

    def __str__(self):
        return self.title


class UserGame(models.Model):
    class ListType(models.TextChoices):
        OWNED = "owned", "Owned"
        WISHLIST = "wishlist", "Wishlist"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_entries"
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="library_entries"
    )
    list_type = models.CharField(max_length=8, choices=ListType.choices, default=ListType.OWNED)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("user", "game"), name="unique_user_game"),
            models.CheckConstraint(
                condition=models.Q(list_type__in=("owned", "wishlist")),
                name="valid_user_game_list_type",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.game} ({self.get_list_type_display()})"
