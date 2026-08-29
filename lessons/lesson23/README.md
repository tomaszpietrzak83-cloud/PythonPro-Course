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

# Lesson23 Task Map

This file lists the places where `TASK` markers were added to make review easier.

## Tagged locations

- `project/cars/admin.py`
  - `# TASK 10` above `CarInline`
  - `# TASK 10` above `DealerAdmin`
  - `# TASK 01 02 03 04 05 06 07 08 09` above `CarAdmin`
  - `# TASK 02 06 09` above `list_display`
  - `# TASK 03` above `search_fields`
  - `# TASK 04` above `list_filter`
  - `# TASK 05` above `ordering`
  - `# TASK 07` above `readonly_fields`
  - `# TASK 08` above `actions`
  - `# TASK 06` above `full_name` and `full_name.short_description`
  - `# TASK 08` above `mark_as_unavailable`
  - `# TASK 09` above `display_photo` and `display_photo.short_description`
- `project/cars/models.py`
  - `# TASK 10` above `Dealer`
  - `# TASK 10` above `Car`
- `project/project/settings.py`
  - `# TASK 01 02 03 04 05 06 07 08 09 10` above the `cars` app entry in `INSTALLED_APPS`
  - `# TASK 09` above `MEDIA_URL`
  - `# TASK 09` above `MEDIA_ROOT`
- `project/project/urls.py`
  - `# TASK 09` on the media-serving `urlpatterns` extension

## Other prepared files

- `.gitignore` prepared for the Lesson 23 project root
- `README.md` added to help the reviewer find task-related code quickly
