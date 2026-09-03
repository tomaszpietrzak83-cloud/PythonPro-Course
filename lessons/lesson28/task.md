# Lesson 28 - Final Project: GameShelf

## Project Goal

Build a fully functional Django web application called **GameShelf**.

GameShelf is a personal PC game library. Visitors can browse a public catalog of PC games, view game details, and filter games by genre or tags. Registered users can save games to their own account as either:

- owned games,
- wishlist games.

The project should grow step by step. Each version should be small, usable, and working before you add the next feature.

## Base Project

Use the existing Django project:

```text
lessons/lesson28/l28_pro
```

Use the existing Django app:

```text
GameShelf
```

Do not create a new project unless your current project is broken beyond repair.

## Core Requirements

Your application must include:

- user registration, login, and logout using Django's built-in authentication system,
- a public game catalog,
- a game detail page,
- owned games and wishlist functionality for logged-in users,
- a user dashboard or library page,
- Django admin configuration,
- test data generation using Faker or an external games API,
- a custom management command, for example:

```bash
python manage.py seed_db
```

- basic unit tests,
- image support for game covers,
- a clean and usable interface.

## Suggested Models

Start with a small model structure. You can extend it later.

### Game

Suggested fields:

- `title`
- `description`
- `release_date`
- `cover`
- `studio`
- `genres`
- `tags`
- `source_url`
- `external_id`

### Studio

Suggested fields:

- `name`
- `description`
- `logo`

### Genre

Suggested fields:

- `name`
- `slug`

### Tag

Suggested fields:

- `name`
- `slug`

### UserGame

This model connects a Django user with a game.

Suggested fields:

- `user`
- `game`
- `list_type`
- `play_status`
- `rating`
- `note`
- `created_at`
- `updated_at`

Suggested `list_type` values:

- `owned`
- `wishlist`

Suggested `play_status` values:

- `not_started`
- `playing`
- `completed`
- `abandoned`

Important rule:

One user should not be able to add the same game to their library more than once.

## Main Features

### Public Features

Users who are not logged in should be able to:

- view the homepage,
- view the game catalog,
- search games by title,
- filter games by genre,
- filter games by tag,
- open a game detail page.

### Logged-In User Features

Logged-in users should be able to:

- add a game to owned games,
- add a game to wishlist,
- move a game from wishlist to owned games,
- view their personal library,
- filter their library by owned and wishlist games,
- update play status,
- add or edit rating,
- add or edit a private note,
- remove a game from their library.

## Admin Requirements

Configure Django admin for the main models.

Use:

- `list_display`,
- `search_fields`,
- `list_filter`,
- inline editing where it makes sense,
- custom admin methods where they make the admin panel easier to read.

Example admin ideas:

- show game title, studio, release date, and number of users who added the game,
- search games by title and studio name,
- filter games by genre, tag, or release year,
- edit related user-game entries from the game admin page.

## Test Data

You have two possible paths:

### Option A - Fake Data

Use Faker to create imaginary games, studios, genres, tags, and users.

This is easier and safer for the first working version.

### Option B - External Game Data

Later in the project, you may import real PC game data from an external games API such as RAWG.

The importer should be a management command, for example:

```bash
python manage.py import_games --genre action --limit 100
```

Do not start with the external API. First build a small local version that works with your own database.

## Image Requirement

The final project should support game covers.

In early versions, you can use:

- a default placeholder cover,
- manually uploaded test covers,
- Faker-generated image URLs,
- later, covers imported from an external API.

Do not block the whole project because of covers. A working catalog with placeholder images is better than a broken catalog waiting for perfect assets.

## Frontend Requirement

Start with simple Django templates and your own CSS.

Near the end of the project, improve the frontend using a UI library or component examples. Good candidates:

- Bootstrap components: https://getbootstrap.com/docs/5.3/getting-started/javascript/
- Flowbite components: https://flowbite.com/docs/getting-started/introduction/
- htmx for small dynamic interactions: https://htmx.org/docs/

Use frontend helpers only after the backend works. The main goal is still Django, models, views, forms, authentication, and tests.

## API Documentation Extension

Because Lesson 28 is about API documentation, add a small API part near the end of the project.

Suggested API endpoints:

- list games,
- show game details,
- list genres,
- list tags,
- show current user's library.

Use Django REST Framework and document the API with `drf-spectacular`.

The API does not need to replace your HTML pages. Treat it as an additional feature.

## Final Checklist

Your final GameShelf project should have:

- working homepage,
- working game catalog,
- working game detail page,
- working registration and login,
- owned games,
- wishlist,
- user library page,
- admin panel,
- seed command,
- basic tests,
- media/image support,
- optional external game import,
- optional improved frontend,
- small documented API with Swagger UI.
