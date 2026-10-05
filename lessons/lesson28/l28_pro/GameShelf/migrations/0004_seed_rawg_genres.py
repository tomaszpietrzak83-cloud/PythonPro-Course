from django.db import migrations


# RAWG genre names and slugs: https://rawg.io/genres (2026-10-05).
GENRES = (
    ("Action", "action"), ("Adventure", "adventure"), ("Arcade", "arcade"),
    ("Board Games", "board-games"), ("Card", "card"), ("Casual", "casual"),
    ("Educational", "educational"), ("Family", "family"), ("Fighting", "fighting"),
    ("Indie", "indie"), ("Massively Multiplayer", "massively-multiplayer"),
    ("Platformer", "platformer"), ("Puzzle", "puzzle"), ("Racing", "racing"),
    ("RPG", "role-playing-games-rpg"), ("Shooter", "shooter"),
    ("Simulation", "simulation"), ("Sports", "sports"), ("Strategy", "strategy"),
)


def seed_genres(apps, schema_editor):
    Genre = apps.get_model("GameShelf", "Genre")
    for name, slug in GENRES:
        Genre.objects.using(schema_editor.connection.alias).get_or_create(
            slug=slug, defaults={"name": name}
        )


class Migration(migrations.Migration):
    dependencies = [("GameShelf", "0003_genre_game_genres")]
    operations = [migrations.RunPython(seed_genres, migrations.RunPython.noop)]
