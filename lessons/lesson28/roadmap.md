# GameShelf Roadmap

This roadmap is designed so that every version of the project is usable. Do not try to build everything at once. Finish one version, run the server, click through the app, and only then move to the next version.

## Version 0.0.1 - Project Runs

Goal: the Django project starts without errors.

Tasks:

1. Go to `lessons/lesson28/l28_pro`.
2. Add `GameShelf` to `INSTALLED_APPS`.
3. Run initial migrations.
4. Start the development server.
5. Open the default Django page or admin URL.

Working result:

- `python manage.py runserver` works.
- The project loads in the browser.

Suggested check:

```bash
python manage.py check
```

## Version 0.0.2 - First Real Page

Goal: create one working view.

Tasks:

1. Create a `urls.py` file inside `GameShelf`.
2. Add a simple home view.
3. Connect `GameShelf.urls` in the main project `urls.py`.
4. Create a basic template.
5. Add a link to the admin page.

Working result:

- `/` shows a GameShelf homepage.
- The page is simple, but it is yours.

## Version 0.0.3 - First Model

Goal: store games in the database.

Tasks:

1. Create the `Game` model with only the most important fields:
   - `title`
   - `description`
   - `release_date`
2. Create and run migrations.
3. Register `Game` in Django admin.
4. Create a superuser.
5. Add a few games manually in admin.

Working result:

- You can add games in admin.
- The database contains real records.

## Version 0.0.4 - Game Catalog

Goal: show games from the database.

Tasks:

1. Create a game list view.
2. Create a game list template.
3. Display game titles and short descriptions.
4. Add links from homepage to catalog.
5. Add links from catalog back to homepage.

Working result:

- `/games/` shows games from the database.

## Version 0.0.5 - Game Detail Page

Goal: each game has its own page.

Tasks:

1. Create a game detail view.
2. Add a URL with a game id or slug.
3. Create a detail template.
4. Link every game in the catalog to its detail page.
5. Handle missing games correctly with `get_object_or_404`.

Working result:

- Clicking a game opens its detail page.

## Version 0.1.0 - Minimum Usable App

Goal: GameShelf is now a small but usable catalog.

Tasks:

1. Add basic navigation.
2. Add simple CSS.
3. Improve the homepage.
4. Improve the catalog layout.
5. Add a basic test for the homepage.
6. Add a basic test for the game list page.
7. Add a basic test for the game detail page.

Working result:

- A visitor can open the site, browse games, and view game details.
- You have your first stable version.

## Version 0.1.1 - Studio Model

Goal: connect games with studios.

Tasks:

1. Create a `Studio` model.
2. Add a `ForeignKey` from `Game` to `Studio`.
3. Update migrations.
4. Register `Studio` in admin.
5. Show studio names in catalog and detail pages.

Working result:

- Games can belong to studios.

## Version 0.1.2 - Genres

Goal: add game categories.

Tasks:

1. Create a `Genre` model.
2. Add a `ManyToManyField` from `Game` to `Genre`.
3. Update admin.
4. Show genres on the game detail page.
5. Add a genre filter to the catalog.

Working result:

- Users can filter games by genre.

## Version 0.1.3 - Tags

Goal: add flexible filtering.

Tasks:

1. Create a `Tag` model.
2. Add a `ManyToManyField` from `Game` to `Tag`.
3. Update admin.
4. Show tags on the game detail page.
5. Add a tag filter to the catalog.

Working result:

- Users can filter games by tags such as `single-player`, `open-world`, `story-rich`, or `co-op`.

## Version 0.1.4 - Search

Goal: make the catalog easier to use.

Tasks:

1. Add a search form to the catalog.
2. Search by game title.
3. Optionally search by studio name.
4. Keep search and filters readable in the URL query string.

Working result:

- Users can search games by text.

## Version 0.2.0 - Authentication

Goal: users can log in and log out.

Tasks:

1. Add login and logout URLs.
2. Create login template.
3. Add navigation links depending on authentication state.
4. Create a registration view.
5. Create a registration template.
6. Test registration manually.

Working result:

- A new user can register.
- A registered user can log in and log out.

## Version 0.2.1 - UserGame Model

Goal: prepare owned games and wishlist.

Tasks:

1. Create the `UserGame` model.
2. Connect it with `User` and `Game`.
3. Add `list_type` with values:
   - `owned`
   - `wishlist`
4. Add a uniqueness rule so one user cannot add the same game twice.
5. Register `UserGame` in admin.
6. Add tests for the model rule.

Working result:

- The database can store a user's relationship with a game.

## Version 0.2.2 - Add to Owned

Goal: logged-in users can add games to owned games.

Tasks:

1. Add an "Add to owned" button on the game detail page.
2. Create a POST view for this action.
3. Require login for the action.
4. If the game is already on the wishlist, move it to owned.
5. Show a success message.

Working result:

- A logged-in user can save a game as owned.

## Version 0.2.3 - Add to Wishlist

Goal: logged-in users can add games to wishlist.

Tasks:

1. Add an "Add to wishlist" button on the game detail page.
2. Create a POST view for this action.
3. Require login for the action.
4. If the game is already owned, decide whether to block the change or move it to wishlist.
5. Show a success message.

Working result:

- A logged-in user can save a game to wishlist.

## Version 0.2.4 - My Library

Goal: users can see their saved games.

Tasks:

1. Create a personal library view.
2. Require login.
3. Show owned games and wishlist games.
4. Add filters for:
   - all
   - owned
   - wishlist
5. Add a navigation link to "My Library".

Working result:

- A user can manage a visible personal collection.

## Version 0.3.0 - Play Status, Rating, and Notes

Goal: the library becomes personal.

Tasks:

1. Add `play_status` to `UserGame`.
2. Add `rating` to `UserGame`.
3. Add `note` to `UserGame`.
4. Create a form for editing a saved game.
5. Add an edit page or inline edit view.
6. Add validation for rating.

Working result:

- A user can track whether they are playing, completed, or abandoned a game.
- A user can rate games and add private notes.

## Version 0.3.1 - Remove From Library

Goal: users can clean their library.

Tasks:

1. Add a remove button.
2. Use POST for deletion.
3. Add a confirmation step or clear button text.
4. Show a success message after deletion.
5. Test that users cannot remove another user's entry.

Working result:

- A user can remove a game from their own library.

## Version 0.4.0 - Better Admin

Goal: admin is useful, not just enabled.

Tasks:

1. Add `list_display` to all important models.
2. Add `search_fields`.
3. Add `list_filter`.
4. Add useful ordering.
5. Add inline editing where it helps.
6. Add custom display methods, for example number of users who saved a game.

Working result:

- You can manage project data efficiently from admin.

## Version 0.5.0 - Seed Command

Goal: create test data automatically.

Tasks:

1. Create management command folders.
2. Add `seed_db`.
3. Use Faker to create:
   - studios,
   - genres,
   - tags,
   - games,
   - test users,
   - user library entries.
4. Make the command safe to run more than once.
5. Add command options such as `--games 50`.

Working result:

- You can rebuild useful test data with one command.

Suggested command:

```bash
python manage.py seed_db --games 50
```

## Version 0.6.0 - Cover Images

Goal: games have images.

Tasks:

1. Configure `MEDIA_URL` and `MEDIA_ROOT`.
2. Add an image field for game covers.
3. Add a default placeholder cover.
4. Show covers in catalog and detail pages.
5. Make sure missing images do not break templates.

Working result:

- The catalog looks like a game library, even with placeholder covers.

## Version 0.7.0 - Tests

Goal: protect the most important behavior.

Tasks:

1. Test model creation.
2. Test catalog view status code.
3. Test detail view status code.
4. Test adding to owned requires login.
5. Test adding to wishlist requires login.
6. Test users cannot duplicate the same game in their library.
7. Test users cannot edit another user's library entry.

Working result:

- Core behavior is checked by automated tests.

## Version 0.8.0 - Optional External Import

Goal: import real game data.

Tasks:

1. Choose an external source, for example RAWG.
2. Store the API key outside the code.
3. Create an import management command.
4. Start with one genre and a small limit.
5. Save external ids to avoid duplicates.
6. Save image URLs or download covers into media files.
7. Handle API errors clearly.

Working result:

- You can import real games without manual data entry.

Suggested first test:

```bash
python manage.py import_games --genre action --limit 10
```

## Version 0.9.0 - Small API

Goal: connect the project with Lesson 28 API documentation.

Tasks:

1. Install and configure Django REST Framework.
2. Create serializers for games, genres, tags, and user library entries.
3. Create read-only endpoints for public catalog data.
4. Create an endpoint for the logged-in user's library.
5. Install and configure `drf-spectacular`.
6. Add Swagger UI.
7. Add descriptions to important endpoints.

Working result:

- The project has a small documented API.

## Version 0.10.0 - Frontend Polish

Goal: improve the interface after the backend works.

Tasks:

1. Review the main screens:
   - homepage,
   - catalog,
   - detail page,
   - login/register,
   - my library.
2. Choose a frontend helper:
   - Bootstrap for fast components: https://getbootstrap.com/docs/5.3/getting-started/javascript/
   - Flowbite if you want Tailwind-based components: https://flowbite.com/docs/getting-started/introduction/
   - htmx for small dynamic interactions: https://htmx.org/docs/
3. Improve navigation.
4. Improve forms.
5. Improve cards and spacing.
6. Add empty states for pages with no results.
7. Add message styling.
8. Check the app on a narrow screen.

Working result:

- The app is comfortable to use and looks finished enough for a course project.

## Version 1.0.0 - Final Review

Goal: prepare the project as a final lesson project.

Tasks:

1. Run all tests.
2. Run Django system checks.
3. Click through the main user flow.
4. Remove unused code.
5. Check that migrations are committed or saved.
6. Check that secret keys and API keys are not committed.
7. Update README or project notes.
8. Write a short summary of what the app does.

Working result:

- GameShelf is a complete Django project with a working catalog, user library, wishlist, admin, seed data, tests, and optional API documentation.

## Recommended Development Rule

After every version, answer these questions:

1. Does the server start?
2. Can I click through the feature in the browser?
3. Did I run migrations if models changed?
4. Did I add or update at least one useful test?
5. Did I keep the code smaller than my ambition?

If the answer to the first two questions is not yes, do not start the next version yet.
