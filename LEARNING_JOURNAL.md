# Learning Journal

This journal was created from the commit history in `PythonPro-Course` and from lesson repositories imported into it with `git subtree`.

## Timeline

| Date | Learning topic | Visible progress |
| --- | --- | --- |
| 2026-04-17 | First exercises, pull requests, commitlint | Early GitHub practice with branches, pull requests, and commit conventions. |
| 2026-04-19 | Variables, functions, arrays, file organization | Several refactors: variable names, extracted functions, and moving files into better places. |
| 2026-04-20 - 2026-04-22 | Functions and conditional logic | Function optimization, alternative solutions, and more intentional refactoring. |
| 2026-04-24 - 2026-05-11 | Files, data, and new exercise sets | Lessons 08 and 09, work with TXT, JSON, CSV, and XLSX files. |
| 2026-05-13 - 2026-05-18 | OOP, SQL, databases | Lessons 12-14: classes, methods, Mermaid diagrams, SQLite, queries, and data models. |
| 2026-05-22 - 2026-05-31 | Application projects and Git | Larger program work, requirements, missing files, lesson 16, and lesson 15/17 applications. |
| 2026-06-05 - 2026-06-11 | Django and project organization | Lessons 18-20, `.gitignore`, removing `.venv` from tracking, and Django project basics. |
| 2026-06-20 - 2026-07-10 | More lessons and branch merges | Lessons 21-23, lesson branch merges, and continued file cleanup. |
| 2026-08-06 - 2026-08-12 | Repository cleanup and better commits | New lesson 09 materials, three focused `lesson12` commits, and consolidation of lesson repositories. |

## Main Skills Visible In The History

- Python basics: variables, conditionals, loops, functions, and string formatting.
- File handling: TXT, JSON, CSV, XLSX, and simple output logs.
- OOP: classes, `@dataclass`, properties, class methods, static methods, `__str__`, and `__repr__`.
- Error handling: `try` / `except`, custom exception classes, and data validation.
- SQL and SQLite: creating databases, writing queries, and working with simple data models.
- Django: starting a project, creating apps, and understanding `manage.py`, `settings.py`, and `urls.py`.
- Git: branches, merges, pull requests, Conventional Commits, `.gitignore`, and preserving history without rebasing.

## Repeating Patterns To Improve

- Some commit messages were too general, for example `refactor: minor changes` or `style: add white spaces`.
- Some commits grouped too many changes together.
- File and directory naming styles were inconsistent: `Lesson22`, `lesson-23`, `Lesson 17 app`, `lesson01`.
- There were earlier issues with virtual environments and global `pip`; from now on, `.venv` should stay local and ignored.

## Good Practices From Now On

1. One commit should have one main topic.
2. A commit message should answer: what changed and why.
3. Before committing Python files, run at least a syntax check:

```bash
python -m py_compile path/to/file.py
```

4. New lessons should use a consistent directory name:

```text
lessons/lesson25/
```

5. For Django work, install packages only inside an active `.venv`:

```bash
source .venv/Scripts/activate
python -m pip install django
```

## Example Of Better lesson12 Commits

Instead of one large `refactor: minor changes` commit, the changes were split by topic:

```text
feat(lesson12): extend object model exercises
refactor(lesson12): simplify calculator exercises
feat(lesson12): add custom validation exceptions
```

This is a better direction: a commit does not have to be perfect, but it should clearly tell the reader what the change is about.
