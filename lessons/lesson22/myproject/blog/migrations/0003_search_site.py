import django.db.models.deletion
from django.db import migrations, models

import blog.models


def move_existing_relations(apps, schema_editor):
    Author = apps.get_model("blog", "Author")
    Post = apps.get_model("blog", "Post")
    PostTag = apps.get_model("blog", "PostTag")

    placeholder, _ = Author.objects.get_or_create(
        first_name="Author", last_name="deleted", is_placeholder=True
    )
    Post.objects.filter(author__isnull=True).update(author=placeholder)

    old_relation = Post.tags.through
    PostTag.objects.bulk_create(
        [
            PostTag(post_id=relation.post_id, tag_id=relation.tag_id)
            for relation in old_relation.objects.all()
        ],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):
    dependencies = [("blog", "0002_alter_post_content")]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("is_placeholder", models.BooleanField(default=False)),
            ],
            options={"ordering": ["last_name", "first_name"]},
        ),
        migrations.AddConstraint(
            model_name="author",
            constraint=models.UniqueConstraint(
                fields=("first_name", "last_name"), name="unique_author_name"
            ),
        ),
        migrations.CreateModel(
            name="PostTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blog.post",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blog.tag",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="posttag",
            constraint=models.UniqueConstraint(
                fields=("post", "tag"), name="unique_post_tag"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="blog.category"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=models.SET(blog.models.get_deleted_author),
                to="blog.author",
            ),
        ),
        migrations.RunPython(move_existing_relations, migrations.RunPython.noop),
        migrations.RemoveField(model_name="post", name="tags"),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                blank=True, through="blog.PostTag", to="blog.tag"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                on_delete=models.SET(blog.models.get_deleted_author),
                to="blog.author",
            ),
        ),
    ]
