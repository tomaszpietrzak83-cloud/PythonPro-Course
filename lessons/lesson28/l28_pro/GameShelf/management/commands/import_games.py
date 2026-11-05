from io import BytesIO
from urllib.parse import urlsplit

import requests
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_date
from django.utils.html import strip_tags

from GameShelf.models import Game, Genre, Tag


API_URL = "https://api.rawg.io/api"
MAX_IMAGE_BYTES = 10 * 1024 * 1024
IMAGE_TYPES = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}


def rawg_json(endpoint, key, **params):
    try:
        with requests.get(
            f"{API_URL}/{endpoint}", params={"key": key, **params},
            timeout=(5, 20), allow_redirects=False,
        ) as response:
            if response.status_code != 200:
                raise CommandError(f"RAWG returned HTTP {response.status_code}. Check the key and quota.")
            data = response.json()
    except (requests.RequestException, ValueError):
        # Do not display exceptions containing the API key in the request URL.
        raise CommandError("RAWG did not return a valid response. Check the connection and retry.") from None
    if not isinstance(data, dict):
        raise CommandError("RAWG returned an unexpected response format.")
    return data


def download_cover(url):
    if not isinstance(url, str):
        raise ValueError("Invalid image URL")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "media.rawg.io":
        raise ValueError("Unsupported image host")
    with requests.get(url, stream=True, timeout=(5, 20), allow_redirects=False) as response:
        if response.status_code != 200:
            raise ValueError("Image request failed")
        content = bytearray()
        for chunk in response.iter_content(64 * 1024):
            content.extend(chunk)
            if len(content) > MAX_IMAGE_BYTES:
                raise ValueError("Image is too large")
    with Image.open(BytesIO(content)) as image:
        extension = IMAGE_TYPES.get(image.format)
        if not extension or image.width * image.height > 20_000_000:
            raise ValueError("Unsupported image format or dimensions")
        image.verify()
    return extension, ContentFile(bytes(content))


def slugs(items):
    if not isinstance(items, list):
        return []
    return [item["slug"] for item in items if isinstance(item, dict) and isinstance(item.get("slug"), str)]


class Command(BaseCommand):
    help = "Import a small batch of RAWG games and download their covers."

    def add_arguments(self, parser):
        parser.add_argument("--genre", default="action")
        parser.add_argument("--limit", type=int, default=10)

    def handle(self, *args, **options):
        key = settings.RAWG_API_KEY
        if not key:
            raise CommandError("Set RAWG_API_KEY in the environment or lessons/lesson28/.env.")
        limit = options["limit"]
        if not 1 <= limit <= 20:
            raise CommandError("--limit must be between 1 and 20.")
        genre = Genre.objects.filter(slug=options["genre"]).first()
        if genre is None or genre.slug.startswith("fake"):
            raise CommandError("--genre must be an existing RAWG genre, for example action.")
        payload = rawg_json("games", key, genres=genre.slug, platforms=4, page_size=limit)
        results = payload.get("results")
        if not isinstance(results, list):
            raise CommandError("RAWG response is missing the game list.")

        created_count = reused_count = skipped_count = 0
        for item in results[:limit]:
            if not isinstance(item, dict):
                skipped_count += 1
                continue
            rawg_id, title = item.get("id"), item.get("name")
            if type(rawg_id) is not int or not 0 < rawg_id < 2**63 or not isinstance(title, str) or not title.strip():
                skipped_count += 1
                continue
            game = Game.objects.filter(rawg_id=rawg_id).first()
            if game is None:
                detail = rawg_json(f"games/{rawg_id}", key)
                description = detail.get("description_raw") or detail.get("description")
                try:
                    released = parse_date(item.get("released") or "")
                except (TypeError, ValueError):
                    released = None
                game, created = Game.objects.get_or_create(
                    rawg_id=rawg_id, defaults={
                        "title": title.strip()[:120],
                        "description": strip_tags(description) if isinstance(description, str) else "",
                        "release_date": released,
                    },
                )
                if created:
                    game.genres.add(genre, *Genre.objects.filter(slug__in=slugs(item.get("genres"))))
                    game.tags.add(*Tag.objects.filter(slug__in=slugs(item.get("tags"))))
                created_count += int(created)
                reused_count += int(not created)
            else:
                reused_count += 1
            if not game.cover and item.get("background_image"):
                try:
                    extension, content = download_cover(item["background_image"])
                except (requests.RequestException, OSError, ValueError, Image.DecompressionBombError):
                    self.stderr.write(f"RAWG game {rawg_id}: cover unavailable; using placeholder.")
                else:
                    game.cover.save(f"rawg-{rawg_id}.{extension}", content)
        self.stdout.write(f"Created {created_count}; reused {reused_count}; skipped {skipped_count}.")
