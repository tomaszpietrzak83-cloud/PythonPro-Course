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
