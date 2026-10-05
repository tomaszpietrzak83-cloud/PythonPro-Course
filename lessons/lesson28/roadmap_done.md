# GameShelf Completed Roadmap

This file tracks completed GameShelf versions.

## Version 0.0.1 - Project Runs

Status: done.

Completed:

1. The Django project exists in `lessons/lesson28/l28_pro`.
2. The `GameShelf` app is added to `INSTALLED_APPS`.
3. Initial migrations were created and applied.
4. The development server can start.
5. Django system check passes.

Working result:

- `python manage.py runserver` works.
- The project loads in the browser.
- `python manage.py check` reports no issues.

## Version 0.0.2 - First Real Page

Status: done.

Completed:

1. `GameShelf/urls.py` was created.
2. A simple `home` view was added.
3. `GameShelf.urls` is connected in the main project `urls.py`.
4. A basic homepage template was created.
5. The homepage includes a link to the admin page.

Working result:

- `/` shows a GameShelf homepage.
- The homepage returns HTTP 200.

## Version 0.0.3 - First Model

Status: done.

Completed:

1. The `Game` model was created with:
   - `title`
   - `description`
   - `release_date`
2. Model migrations were created and applied.
3. `Game` was registered in Django admin.
4. A superuser/admin creation helper exists as `create_admin.py`.
5. Several games were added manually through the Django admin panel.

Working result:

- Games can be managed from Django admin.
- The database contains manually added game records.

## Version 0.0.4 - Game Catalog

Status: done.

Completed:

1. A public game list view was added.
2. The `/games/` route displays games from the database.
3. The game list template displays titles and descriptions.
4. The homepage links to the game catalog.
5. The game catalog links back to the homepage.

Working result:

- `/games/` shows the games stored in the database.
- Visitors can navigate between the homepage and the catalog.

## Version 0.0.5 - Game Detail Page

Status: done.

Completed:

1. A game detail view was added.
2. The detail page uses a URL containing the game ID.
3. A dedicated detail template displays the game's information.
4. Every game in the catalog links to its detail page.
5. Missing games return a standard 404 response through `get_object_or_404`.

Working result:

- Clicking a game in `/games/` opens its detail page.
- An unknown game ID returns HTTP 404.

## Version 0.1.0 - Minimum Usable App

Status: done.

Completed:

1. Shared navigation was added to the base template.
2. A responsive stylesheet was added for the main pages.
3. The homepage and game catalog received clearer layouts and empty states.
4. The game detail page received matching visual styling.
5. Tests were added for the homepage, catalog, detail page, and 404 behavior.

Working result:

- Visitors can navigate through a consistent, styled GameShelf interface.
- The main views are covered by automated tests.

## Version 0.1.1 - Studio Model

Status: done.

- Added Studio and an optional Game.studio foreign key.
- Deleting a studio keeps its games (SET_NULL).
- Studios can be managed in admin and appear in catalog and detail pages.
- Applied migrations on PostgreSQL; all 5 tests and system checks pass.
- Verified the catalog in the browser. Studio names are entered manually.

## Version 0.1.2 - Genres

Status: done.

- Added Genre (unique name and slug) and Game.genres (many-to-many).
- Seeded all 19 RAWG genres with a data migration; no API key is needed.
- Source: https://rawg.io/genres (2026-10-05).
- Added admin editing, genre links on detail pages, and a GET catalog filter.
- Unknown genres produce a form error instead of a server error.
- Migrations, 8 tests, system checks, and browser catalog verification pass.

## Version 0.1.3 - Tags

Status: done.

- Added Tag (unique name and slug) and Game.tags (many-to-many).
- Seeded 12 popular RAWG tags, including Singleplayer, Co-op and Open World.
- Source: https://rawg.io/tags (2026-10-05); this is an extensible starter subset.
- Tags can be assigned in admin and displayed as filter links on detail pages.
- Genre and tag filters combine using AND; selected values stay in the URL.
- Migrations, 11 tests, system checks, and browser verification pass.

## Version 0.1.4 - Search

Status: done.

- Added case-insensitive title search using `q`, combined with `genre` and `tag`.
- Added `/games/suggestions/?q=a`: up to 3 matching database titles, ordered by title then ID.
- Suggestions appear while typing from the first non-whitespace character.
- Links open game details; Tab navigates links, Escape closes suggestions, Enter submits search.
- JavaScript debounces requests and cancels stale responses; search also works without JavaScript.
- Existing games were preserved; studios, genres and tags can be assigned through admin.
- All 19 tests, system checks, migration consistency and browser search verification pass.

### Learning notes

- `ForeignKey`: many games can share one studio; `SET_NULL` preserves games when a studio is deleted.
- `ManyToManyField`: a game can have several genres/tags, and each genre/tag can describe many games.
- `select_related` joins the studio; `prefetch_related` loads collections without a query for every item.
- `ModelChoiceField` validates URL filter values against actual database records.
- `title__icontains` searches inside titles regardless of letter case; `[:3]` limits results in SQL.
- PostgreSQL was already configured and available; all migrations and tests ran against it.

## Next Version

Continue with: Version 0.2.0 - Authentication.
