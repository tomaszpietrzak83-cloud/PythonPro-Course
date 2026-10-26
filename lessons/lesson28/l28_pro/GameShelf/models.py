from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
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
    cover = models.ImageField(upload_to="covers/", blank=True)
    release_date = models.DateField(null=True, blank=True)
    studio = models.ForeignKey(
        Studio, on_delete=models.SET_NULL, null=True, blank=True, related_name="games"
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name="games")
    tags = models.ManyToManyField(Tag, blank=True, related_name="games")

    def __str__(self):
        return self.title


class UserGame(models.Model):
    class PlayStatus(models.TextChoices):
        NOT_STARTED = "not_started", "Not started"
        PLAYING = "playing", "Playing"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"

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
    play_status = models.CharField(
        max_length=11, choices=PlayStatus.choices, default=PlayStatus.NOT_STARTED
    )
    rating = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    note = models.TextField(blank=True, max_length=5000)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("user", "game"), name="unique_user_game"),
            models.CheckConstraint(
                condition=models.Q(list_type__in=("owned", "wishlist")),
                name="valid_user_game_list_type",
            ),
            models.CheckConstraint(
                condition=models.Q(rating__isnull=True) | models.Q(rating__gte=1, rating__lte=10),
                name="user_game_rating_1_to_10",
            ),
            models.CheckConstraint(
                condition=models.Q(play_status__in=("not_started", "playing", "completed", "abandoned")),
                name="valid_user_game_play_status",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.game} ({self.get_list_type_display()})"
