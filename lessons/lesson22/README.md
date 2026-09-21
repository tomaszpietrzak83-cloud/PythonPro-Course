# Running inside PythonPro-Course

Inside this repository, lesson 22 uses the main `PythonPro-Course/.venv` environment.
VS Code settings point to this environment when opening either the whole course
or lesson 22 as a separate folder. If VS Code previously saved a different
interpreter, use `Python: Select Interpreter` and select
`PythonPro-Course/.venv/Scripts/python.exe`.

You can run `myproject/blog/management/commands/seed_blog.py` directly using
Run Python File. It delegates to `manage.py seed_blog` using the main course
environment regardless of which interpreter starts the file.
The seeder deletes existing posts, authors, categories, and tags and creates new sample data.

The advanced article search added for this lesson is documented in
[`SEARCH_SITE.md`](SEARCH_SITE.md). It explains the models, scoring algorithm,
JavaScript libraries, seeder and tests.

You can also run this command from the course root folder:

```powershell
.\.venv\Scripts\python.exe lessons\lesson22\myproject\manage.py seed_blog
```

To create a Django administrator, run `create_superuser.py` and answer the
interactive questions about username, email and password:

```powershell
.\.venv\Scripts\python.exe lessons\lesson22\create_superuser.py
```

The script finds the course virtual environment and delegates to Django's
`manage.py createsuperuser` command. It does not store a password in source code.

# Lesson Setup (standalone ZIP)

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

# Lesson22 Task Map

This file lists the places where `TASK` markers were added to make review easier.

Templates use Django template comments in the form `{# TASK ... #}`.

## Tagged locations

- `myproject/blog/models.py`
  - `# TASK 01` above `Category`
  - `# TASK 08` above `Tag`
  - `# TASK 01` above `Post.category`
  - `# TASK 08` above `Post.tags`
- `myproject/blog/views.py`
  - `# TASK 03 06` above `post_views`
  - `# TASK 06` above search query handling
  - `# TASK 03` above latest-post slicing
  - `# TASK 02` above `category`
- `myproject/blog/urls.py`
  - `# TASK 03 06` above home route
  - `# TASK 02` above category route
- `myproject/blog/templates/post_views.html`
  - `{# TASK 03 06 #}` above page title and post list
  - `{# TASK 06 #}` above search form
- `myproject/blog/templates/sort_by_category.html`
  - `{# TASK 02 #}` above page title
- `myproject/blog/management/commands/seed_blog.py`
  - `# TASK 07 09` above command class and cleanup block
  - `# TASK 07` above category creation and post creation blocks
  - `# TASK 09` above tag creation and tag assignment blocks
- `myproject/myproject/settings.py`
  - `# TASK 10` above `allauth` app entries
  - `# TASK 10` above authentication backends
  - `# TASK 10` above `AccountMiddleware`
  - `# TASK 10` above login and signup settings
- `myproject/myproject/urls.py`
  - `# TASK 02 03 06` above blog include
  - `# TASK 10` above `accounts/` include
- `faker_test.py`
  - `# TASK 05` above Faker test script

## Other prepared files

- `.gitignore` updated with extra SQLite and Django-generated file ignores
- `requirements.txt` generated from the current virtual environment
