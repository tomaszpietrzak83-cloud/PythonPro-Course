# PythonPro-Course

This repository contains my exercises from the Python Pro course. It is a learning workspace for Python, Django, SQL, file handling, testing, and Git practice.

## Structure

```text
PythonPro-Course/
  lessons/              # lessons and lesson projects
  README.md             # repository overview
  MERGE_REPORT.md       # repository consolidation documentation
  LEARNING_JOURNAL.md   # learning journal based on commit history
  .gitignore            # ignored local files, caches, and virtual environments
```

Current lesson directories:

```text
lessons/lesson01
lessons/lesson02
lessons/lesson03
lessons/lesson04
lessons/lesson05
lessons/lesson06
lessons/lesson07
lessons/lesson08
lessons/lesson09
lessons/lesson10
lessons/lesson11
lessons/lesson12
lessons/lesson13
lessons/lesson14
lessons/lesson15_project_sql_app
lessons/lesson16
lessons/lesson17_app
lessons/lesson18_app
lessons/lesson19
lessons/lesson20
lessons/lesson21
lessons/lesson22
lessons/lesson23
lessons/lesson24
```

## Working With Virtual Environments

Use one `.venv` in the course root for all lessons. With Python 3.12 installed:

```powershell
python setup_course.py
.\.venv\Scripts\Activate.ps1
python run_lesson.py lessons/lesson01/task1_hello.py
```

`setup_course.py` installs the shared dependencies. Lesson setup scripts call it as well.
See [URUCHAMIANIE.md](URUCHAMIANIE.md) for Windows setup, application launchers,
external services and the limitations of the checks.

Before merging the shared environment changes, read [MERGE_NOTES.md](MERGE_NOTES.md)
for the reasons, dependencies between changes, PostgreSQL requirements and validation.

Install packages with:

```bash
python -m pip install package_name
```

## Commit Guidelines

Prefer small commits that describe the purpose of the change, for example:

```text
feat(lesson12): add custom validation exceptions
refactor(lesson12): simplify calculator exercises
chore: organize course lessons directory
```

Do not rewrite existing repository history unless there is a strong reason. For a public repository, changing old commits usually requires `force push`, which is risky.

## Documentation

- `MERGE_REPORT.md` explains how the separate lesson repositories were consolidated into this repository.
- `LEARNING_JOURNAL.md` summarizes learning progress based on commit history.
