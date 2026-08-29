# Lesson Setup

This lesson includes `run_before_checking_lesson.py` for standalone ZIP use.

From the lesson folder, run:

```bash
python run_before_checking_lesson.py
```

The script creates a local `.venv` folder inside this lesson and installs the packages listed in `requirements.txt`. It does not use or modify virtual environments outside this lesson folder.

After setup, activate the environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Then run the lesson files normally.

# Lesson25 Task Map

This file lists where `TASK` markers were added to make review easier.

HTTP request files use comments in the form `### TASK ...`.

## Tagged Locations

- `l25_pro/l25_pro/settings.py`
  - `# TASK 01` above the local `new_app` registration
  - `# TASK 01` above the `rest_framework` app registration
- `l25_pro/l25_pro/urls.py`
  - `# TASK 03 08` above the products router
  - `# TASK 06` above the notes router
  - `# TASK 09` above the authors and books routers
  - `# TASK 05` above the cookie routes
  - `# TASK 07` above the calculator route
  - `# TASK 08` above the separate filtering route
- `l25_pro/new_app/models.py`
  - `# TASK 02` above `Product`
  - `# TASK 06` above `Note`
  - `# TASK 09` above `Author`, `Book`, and the `Book.author` relation
- `l25_pro/new_app/serializers.py`
  - `# TASK 02` above `ProductSerializer`
  - `# TASK 06 10` above `NoteSerializer`
  - `# TASK 10` above `validate_title`
  - `# TASK 09` above `AuthorSerializer`, `BookSerializer`, and `author_name`
- `l25_pro/new_app/views.py`
  - `# TASK 03 08` above `ProductViewSet`
  - `# TASK 08` above `ProductViewSet.get_queryset`
  - `# TASK 06` above `NoteViewSet`
  - `# TASK 09` above `AuthorViewSet` and `BookViewSet`
  - `# TASK 05` above `set_name` and `hello`
  - `# TASK 07` above `calculate`
  - `# TASK 08` above `filter_by_price`
- `l25_pro/seed_authors_books.py`
  - `# TASK 09` above the seed data and seeding loop
- `postman_products.http`
  - `### TASK 04` above product create and list requests
- `postman_username.http`
  - `### TASK 05` above cookie test requests
- `postman_notes.http`
  - `### TASK 06` above notes CRUD requests
  - `### TASK 10` above the invalid short-title request
- `postman_calculations.http`
  - `### TASK 07` above calculator test requests
- `postman_filter_products.http`
  - `### TASK 08` above product filtering requests for the ViewSet endpoint
- `postman_filter_function.http`
  - `### TASK 08` above product filtering requests for the separate function endpoint
- `postman_authors_books.http`
  - `### TASK 09` above author and book API requests
- `tasks.md`
  - `## TASK 01` through `## TASK 10` in the cleaned-up task list

## Other Prepared Files

- `tasks.md` contains the original lesson tasks in a cleaner checklist format.
- `l25_pro/db.sqlite3` is the local SQLite database used during manual testing.
- `postman_products.http` contains product creation and listing requests.
- `postman_username.http` contains cookie-setting and cookie-reading requests.
- `postman_notes.http` contains note CRUD requests and the short-title validation test.
- `postman_calculations.http` contains calculator success and error-case requests.
- `postman_filter_products.http` contains filtering requests for `/api/products/`.
- `postman_filter_function.http` contains filtering requests for the separate `/api/filter-products/` function endpoint.
- `postman_authors_books.http` contains author and book API requests.
- `l25_pro/seed_authors_books.py` seeds authors and books through the Django ORM.

## Generated Django Files

These files are framework scaffolding or generated database state, so they do not need task markers unless custom lesson code is added there later.

- `l25_pro/manage.py` is the Django command-line entry point.
- `l25_pro/l25_pro/asgi.py` and `l25_pro/l25_pro/wsgi.py` are generated deployment entry points.
- `l25_pro/l25_pro/__init__.py` and `l25_pro/new_app/__init__.py` mark Python packages.
- `l25_pro/new_app/apps.py` contains the generated app config.
- `l25_pro/new_app/admin.py` and `l25_pro/new_app/tests.py` are currently not used by these tasks.
- `l25_pro/new_app/migrations/` contains Django-generated migration files for model changes.
- `l25_pro/db.sqlite3` is binary database state and should not be manually tagged.

## Short Task Notes

- Task 01 sets up the Django project, the lesson app, and Django REST Framework.
- Task 02 introduces a basic model and `ModelSerializer`.
- Task 03 exposes products through a `ModelViewSet` and `DefaultRouter`.
- Task 04 uses HTTP requests as a Postman alternative for product creation and listing.
- Task 05 demonstrates reading query parameters and setting/reading cookies.
- Task 06 builds a full CRUD API for notes.
- Task 07 demonstrates a function-based DRF endpoint with query parameters and validation.
- Task 08 filters products by price using `get_queryset`; the separate function endpoint is kept as an extra learning version.
- Task 09 demonstrates model relations with `Author`, `Book`, `ForeignKey`, and readable author names in serialized output.
- Task 10 adds custom serializer validation for note titles shorter than five characters.
