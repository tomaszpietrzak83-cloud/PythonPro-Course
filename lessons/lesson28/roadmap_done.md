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

## Version 0.1.4.1 - Faker Seeder: 100 FAKE Games

Status: done.

- `python manage.py seed_db` creates 100 fictional games with the FAKE genre and tag.
- `--games` changes the target count; `--seed` controls reproducible Faker data.
- Unique, nullable `Game.seed_key` identifies generated records without affecting manual games.
- Repeated runs reuse records and preserve edits; increasing the count adds missing records.
- Migration applied on PostgreSQL. All 22 tests pass; two local runs created 100 then reused 100 games.
- Verified `/games/?genre=fake&tag=fake` in the browser.

## Version 0.2.0 - Authentication

Status: done.

- Added registration using Django UserCreationForm, built-in login and POST-only logout.
- Navigation reflects authentication; forms show validation errors and use CSRF protection.
- Login respects safe local `next` destinations and rejects external redirects.
- Registration creates a regular account and sends the user to login.
- All 29 tests pass. Registered, logged in and logged out a local test account in the browser.

## Version 0.2.1 - UserGame Model

Status: done.

- Added UserGame with user/game foreign keys and Owned/Wishlist choices.
- Database constraints enforce one entry per user/game and reject invalid list types.
- Registered entries in admin with search, filters and autocomplete.
- Applied migration on PostgreSQL. All 35 tests pass, including uniqueness, user isolation,
  cascade behavior and the admin list; the public homepage still loads in the browser.

## Version 0.2.2 - Add to Owned

Status: done.

- Added a login-protected, CSRF-protected POST action and game detail button.
- `update_or_create` saves one entry for the current user; wishlist entries move to owned.
- Detail pages show the current user's saved list type and success messages.
- All 41 tests pass, covering repeated requests, authentication, CSRF, 404s and user isolation.
- Verified login with return to game details and adding a seeded game in the browser.

## Version 0.2.3 - Add to Wishlist

Status: done.

- Added a login-protected, CSRF-protected POST action and wishlist button.
- Repeated saves reuse the same entry and never change another user's collection.
- Owned games stay owned: a wishlist request shows an explanation instead of moving them.
- All 47 tests pass. Verified adding to wishlist and then moving to owned in the browser.

## Version 0.2.4 - My Library

Status: done.

- Added `/library/`, accessible only after login and always scoped to the current user.
- Added all/owned/wishlist filters, list labels, detail links and a useful empty state.
- Navigation and saved game details link to My Library.
- Related games/studios load together, avoiding a separate query per library card.
- All 55 tests pass on PostgreSQL. System checks and migration consistency checks pass.
- Verified registration, login/logout, owned/wishlist saves, moving wishlist to owned,
  library filters and the narrow-screen layout in the browser using a local test account.

### Learning notes for versions 0.1.4.1-0.2.4

- `get_or_create` reuses a record without changing it; `update_or_create` can update its list type.
- `UniqueConstraint` enforces one user/game pair even when requests arrive simultaneously.
- `request.user` comes from the authenticated session; a user ID submitted by a form is not trusted.
- `login_required` controls access, `require_POST` limits mutations, and CSRF protects submitted forms.
- Django's `UserCreationForm` validates passwords and stores their hashes rather than plain text.
- To regenerate the sample catalog safely: `python manage.py seed_db --games 100 --seed 28`.

## Version 0.3.0 - Play Status, Rating, and Notes

Status: done.

- Added Not started/Playing/Completed/Abandoned statuses, optional ratings (1-10), and private notes.
- A dedicated ModelForm edits only the current user's status, rating and note (up to 5000 characters).
- Notes appear in the owner's library and edit form, never in the public catalog or game detail.
- Database constraints enforce valid ratings/statuses; existing entries receive safe defaults.
- PostgreSQL migration applied. All 64 tests pass, including privacy, CSRF and validation cases.
- Verified saving Completed, 9/10 and a demo note through the browser.

## Version 0.3.1 - Remove From Library

Status: done.

- Library cards link to a confirmation page; GET never deletes data.
- A CSRF-protected POST removes only the current user's entry, then shows a success message.
- Catalog games and other users' entries are preserved; cancellation keeps the entry and its notes.
- All 71 tests pass, including deletion, user isolation, authentication and CSRF protection.
- Verified the confirmation page and cancellation in the browser.

## Version 0.4.0 - Better Admin

Status: done.

- Added searchable, ordered admin lists for all models with useful filters and autocomplete.
- Studio/genre/tag lists show annotated game counts; games show how many users saved them.
- Game forms include editable library entries; user game lists support inline progress/rating edits.
- Read-only seed identifiers help distinguish generated games; private notes stay out of inline lists.
- All 77 tests pass, including aggregate counts, admin search/filtering and rating validation.
- Verified the admin game search, saved-by count and library inline in the browser on a temporary admin.

## Version 0.5.0 - Seed Command

Status: done.

- Extended `seed_db` with Faker-generated genres/tags, optional test users and personal libraries.
- Kept the default 100 FAKE games and existing stable game seed identifiers.
- Added `--users`, `--entries-per-user` and optional `--user-password-env` for NEW accounts.
- Seeded users are regular accounts identified by a permission-free marker group and stable usernames.
- Repeated runs preserve game edits, library notes/ratings and passwords; manual username collisions
  roll back the entire command. Lower target counts never delete existing data.
- Verified 100 existing games, 3 new users and 30 entries; the second run reused all of them.
- Verified login and the generated library through the browser. Temporary UI-test accounts were cleaned up.
- All 84 tests pass on PostgreSQL; system checks and migration consistency checks pass.
- Added project README with setup, seeder options and learning notes.

### Learning notes for versions 0.3.0-0.5.0

- A ModelForm's `fields` list limits which values a submitted form can change.
- Filter a private object by both its ID and `request.user` before editing or deleting it.
- Field validators provide form errors; database constraints also protect direct ORM writes.
- `annotate(Count(...))` calculates admin counters without a separate query for each row.
- `transaction.atomic` rolls back the whole seeder when any validation or collision fails.

## Version 0.5.0.1 - ImageField Upload and Display

Status: done.

- Added optional Game.cover (ImageField), MEDIA_ROOT/MEDIA_URL and DEBUG-only local media routes.
- Admin validates image uploads; catalog and detail pages display uploaded covers without requiring one.
- Uploaded files stay under media/covers and are ignored by Git; the database stores relative paths.
- Applied migration on PostgreSQL. All 89 tests pass, including real PNG upload and invalid-file rejection.
- Uploaded a local PNG through admin and verified the actual image loads on its public detail page.

## Version 0.6.0 - Cover Images

Status: done.

- Kept Game.cover and local media storage; added a project-owned SVG placeholder.
- Game.cover_url selects the actual uploaded file or the placeholder, including stale file references.
- Catalog, details and personal libraries display consistent cover images with fixed aspect ratios.
- All 93 tests pass; no additional migration is needed.
- Verified that both the uploaded PNG and SVG placeholder load correctly in the browser.

## Version 0.7.0 - Tests

Status: done.

- Reviewed model creation, public pages, login requirements, uniqueness and ownership tests.
- Added connected player workflows with real registration, sessions and enforced CSRF.
- Verified the wishlist-to-owned-to-edit-to-remove flow and two independent users' privacy.
- Added a development media response test that decodes the actual served PNG bytes.
- Added automatic freshness checks for the four generated Polish learning documents.
- Added taskPL.md, roadmapPL.md, lesson-28-DONE.md (red status comments) and most_interesting.md.
- update_docs.py extracts current code/line numbers and completion states; runserver.py refreshes the guides.
- The lesson's AGENTS.md requires documentation regeneration and verification with every future change.
- All 97 tests pass on PostgreSQL. Python application branch/statement coverage is 99%
  (tests and migrations excluded); system checks and migration consistency checks pass.
- Browser checks confirmed PNG upload, loaded placeholder images and a 390px layout without overflow.

## Version 0.8.0 - Optional External Import

Status: done.

- Added a bounded PC-game importer for RAWG, with unique IDs and local cover storage.
- Verified behavior with simulated RAWG responses; live import requires RAWG_API_KEY.

## Version 0.9.0 - Small API

Status: done.

- Added read-only DRF catalog routes and a session-protected library scoped to the current user.
- Reused catalog filters; verified public access, validation, missing games and library isolation.

## Version 0.9.0.1 - OpenAPI and Swagger UI

Status: done.

- Generated OpenAPI with DRF serializers and explicit filter, authentication and error documentation.
- Added Swagger UI and ReDoc using local sidecar assets.
- Verified filtered FAKE games, a game detail and a missing game through Swagger Try it out.

## Version 0.9.0.2 - Additional API Endpoints and Swagger Demonstration

Status: done.

- Added session- and CSRF-protected library POST, detail GET, PATCH and DELETE.
- Enforced ownership, duplicate prevention, rating validation and the owned/wishlist rule.
- Documented request examples and actual success/error responses in OpenAPI.
- Verified the Swagger session and CSRF flow: wishlist 201, move to owned 200,
  invalid rating 400 and removal of the demo entry 204.
- All 111 GameShelf tests pass on PostgreSQL; OpenAPI validates without warnings.

## Next Version

Continue with: Version 0.10.0 - Frontend Polish.
