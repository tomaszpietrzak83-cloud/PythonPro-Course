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

## Next Version

Continue with:

```text
Version 0.0.4 - Game Catalog
```

The next goal is to show games from the database on a public `/games/` page.
