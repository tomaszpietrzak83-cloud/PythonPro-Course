from django.db import models
from django.utils import timezone


def get_deleted_author():
    """Return the shared placeholder used after an author is deleted."""
    author, _ = Author.objects.get_or_create(
        first_name="Author", last_name="deleted", is_placeholder=True
    )
    return author.pk


# SEARCH-SITE: Authors are separate entities, but each post has one author.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_placeholder = models.BooleanField(default=False)

    class Meta:
        ordering = ["last_name", "first_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"], name="unique_author_name"
            )
        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.full_name


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


# SEARCH-SITE: An explicit intermediary makes the Post-Tag relation visible.
class PostTag(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "tag"], name="unique_post_tag"
            )
        ]

    def __str__(self):
        return f"{self.post} — {self.tag}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=5000)
    publication_date = models.DateTimeField(default=timezone.now)
    # TASK 01
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # SEARCH-SITE: Deleting an author preserves their posts.
    author = models.ForeignKey(Author, on_delete=models.SET(get_deleted_author))
    # TASK 08
    tags = models.ManyToManyField(Tag, through=PostTag, blank=True)

    def __str__(self):
        return self.title
