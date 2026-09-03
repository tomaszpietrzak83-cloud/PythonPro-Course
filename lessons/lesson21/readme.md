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

Then run the Django project:

```bash
cd l21_pro
python manage.py migrate
python manage.py seed_lesson21
python manage.py runserver
```

For local development the project uses a non-secret fallback `SECRET_KEY`.
For a real deployment, set `DJANGO_SECRET_KEY` in your environment instead of committing it to Git.

Useful URLs:

- `http://127.0.0.1:8000/categories/`
- `http://127.0.0.1:8000/categories/1/`
- `http://127.0.0.1:8000/articles/`
- `http://127.0.0.1:8000/articles/?q=python`
- `http://127.0.0.1:8000/admin/`

# Lesson21 Implementation Map

The original lesson content was moved to `lesson-21.md`.

Your markdown answers were moved into a separate `solutions/` directory:

- `solutions/01.md` - Category model and migration commands.
- `solutions/02.md` - shell code for creating categories.
- `solutions/03.md` - category list view, template, and URL.
- `solutions/04.md` - static CSS and loading CSS in the template.
- `solutions/05.md` - `Category.objects.get(name="Sport")` shell query.
- `solutions/06.md` - category detail view, template, and URL.
- `solutions/07.md` - `Article` relation to `Category` and article seed data.
- `solutions/08.md` - `is_published` filtering and recent article badge.
- `solutions/09.md` - Django admin template override.
- `solutions/10.md` - GET search form and article filtering.

The implemented project is in `l21_pro/`, with one app named `myapp`, following the same pattern as the neighboring Django lessons.

## How the solution files were implemented

- Tasks 01, 07, and 08 are implemented in `l21_pro/myapp/models.py`.
- Task 02 and the article data from task 07 are implemented as a repeatable management command in `l21_pro/myapp/management/commands/seed_lesson21.py`.
- Tasks 03, 06, 07, 08, and 10 are implemented in `l21_pro/myapp/views.py`.
- Tasks 03, 06, and 10 are wired in `l21_pro/myapp/urls.py`; the app URLs are included from `l21_pro/l21_pro/urls.py`.
- Task 04 is implemented in `l21_pro/myapp/static/myapp/style.css` and loaded by `l21_pro/myapp/templates/myapp/base.html`.
- Task 09 is implemented with `l21_pro/templates/admin/base_site.html`, `TEMPLATES["DIRS"]` in `l21_pro/l21_pro/settings.py`, and admin site labels in `l21_pro/myapp/admin.py`.
- Task 05 stays documented in `solutions/05.md`, because it is a shell query rather than application code.

## Tagged locations

Code uses `# --- TASK ... ---` comments. Templates use Django template comments in the form `{# TASK ... #}`.

- `l21_pro/myapp/models.py`
  - `# --- TASK 01 ---` above `Category`
  - `# --- TASK 07 08 ---` above `Article`
- `l21_pro/myapp/views.py`
  - `# --- TASK 03 ---` above `category_list_view`
  - `# --- TASK 06 07 ---` above `category_detail_view`
  - `# --- TASK 08 10 ---` above `article_list_view`
- `l21_pro/myapp/urls.py`
  - `# --- TASK 03 ---` above `/categories/`
  - `# --- TASK 06 07 ---` above `/categories/<int:pk>/`
  - `# --- TASK 08 10 ---` above `/articles/`
- `l21_pro/l21_pro/urls.py`
  - `# --- TASK 03 06 08 10 ---` above the `myapp.urls` include
- `l21_pro/l21_pro/settings.py`
  - `# --- TASK 09 ---` above the project template directory setting
- `l21_pro/myapp/templates/myapp/category_list.html`
  - `{# TASK 03 04 #}` above the category list
- `l21_pro/myapp/templates/myapp/category_detail.html`
  - `{# TASK 06 #}` above the category title
  - `{# TASK 07 #}` above the related article list
- `l21_pro/myapp/templates/myapp/article_list.html`
  - `{# TASK 10 #}` above the search form
  - `{# TASK 08 #}` above the recent article badge
- `l21_pro/templates/admin/base_site.html`
  - `{# TASK 09 #}` above admin branding
- `l21_pro/myapp/static/myapp/style.css`
  - `/* TASK 04 */` above the body background rule
- `l21_pro/myapp/management/commands/seed_lesson21.py`
  - `# --- TASK 02 ---` above category seed data
  - `# --- TASK 07 08 ---` above article seed data
- `l21_pro/myapp/tests.py`
  - task comments above view tests

## Checks

From `l21_pro/`, run:

```bash
python manage.py check
python manage.py test
```
