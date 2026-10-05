from django.db import migrations


# Starter subset, not the entire RAWG tag database.
# Source: https://rawg.io/tags (2026-10-05).
TAGS = (
    ("Singleplayer", "singleplayer"), ("Multiplayer", "multiplayer"),
    ("Co-op", "co-op"), ("Open World", "open-world"),
    ("Story Rich", "story-rich"), ("Atmospheric", "atmospheric"),
    ("Horror", "horror"), ("Fantasy", "fantasy"),
    ("Exploration", "exploration"), ("Survival", "survival"),
    ("Sandbox", "sandbox"), ("Stealth", "stealth"),
)


def seed_tags(apps, schema_editor):
    Tag = apps.get_model("GameShelf", "Tag")
    for name, slug in TAGS:
        Tag.objects.using(schema_editor.connection.alias).get_or_create(
            slug=slug, defaults={"name": name}
        )


class Migration(migrations.Migration):
    dependencies = [("GameShelf", "0005_tag_game_tags")]
    operations = [migrations.RunPython(seed_tags, migrations.RunPython.noop)]
