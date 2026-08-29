# Lesson Setup

This lesson uses the course-level virtual environment in the repository root.

From the repository root, install only the lesson dependencies with:

```bash
.venv\Scripts\python.exe -m pip install -r lessons\lesson26\requirements.txt
```

Then start the Django project from the folder that contains `manage.py`:

```bash
cd lessons\lesson26\l26_pro
..\..\..\.venv\Scripts\python.exe manage.py runserver
```

For standalone ZIP use, this lesson also includes `run_before_checking_lesson.py`.
That script creates a local `.venv` folder inside this lesson and installs the packages listed in `requirements.txt`.

# Lesson26 Task Map

This file lists where `TASK` markers were added to make review easier.

HTTP request files use comments in the form `### TASK ...`.

## Tagged Locations

- `task01.py`
  - `# TASK 01` above the middleware explanation answers
- `requirements.txt`
  - `# TASK 02` above the lesson dependency list
- `l26_pro/l26_pro/settings.py`
  - `# TASK 03` above the DRF, Simple JWT, and Djoser app registrations
  - `# TASK 03` above `REST_FRAMEWORK`
  - `# TASK 07` above the custom middleware registration
  - `# TASK 09` above `SIMPLE_JWT`
- `l26_pro/l26_pro/urls.py`
  - `# TASK 04` above the Djoser URL includes
  - `# TASK 08` above the protected `/user/` endpoint
- `l26_pro/myapp/middleware.py`
  - `# TASK 07` above `SimpleMethodMiddleware`
- `l26_pro/myapp/views.py`
  - `# TASK 08` above `SomeProtectedView`
- `creating_user_postman.http`
  - `### TASK 05` above the registration request
- `creating_jwt_postman.http`
  - `### TASK 06` above the JWT login request
- `checking_name_of_user_postman.http`
  - `### TASK 08` above the protected endpoint tests
- `task09_token_lifetime.http`
  - `### TASK 09` above the token creation and protected endpoint test requests
- `task10_using_refresh_token.http`
  - `### TASK 10` above the login, refresh, and refreshed-token test requests
- `tasks.md`
  - `## TASK 01` through `## TASK 10` in the task list

## Other Prepared Files

- `lesson-26.md` contains the lesson notes about middleware, JWT, DRF, Simple JWT, and Djoser.
- `tasks.md` contains the lesson task list.
- `create_superuser.md` explains how to create a Django superuser and open the admin panel.
- `run_before_checking_lesson.py` creates a lesson-local virtual environment for standalone setup.
- `task06.py` contains notes from inspecting the JWT payload and calculating access-token lifetime.
- `my_acces_token.py` and `l26_pro/db.sqlite3` are local runtime artifacts used during manual testing and are intentionally ignored by Git.

## Generated Django Files

These files are framework scaffolding or generated database state, so they do not need task markers unless custom lesson code is added there later.

- `l26_pro/manage.py` is the Django command-line entry point.
- `l26_pro/l26_pro/asgi.py` and `l26_pro/l26_pro/wsgi.py` are generated deployment entry points.
- `l26_pro/l26_pro/__init__.py` and `l26_pro/myapp/__init__.py` mark Python packages.
- `l26_pro/myapp/apps.py` contains the generated app config.
- `l26_pro/myapp/models.py` and `l26_pro/myapp/tests.py` are currently not used by these tasks.
- `l26_pro/myapp/migrations/` contains Django migration package files.
- `l26_pro/db.sqlite3` is binary database state and should stay outside version control.

## Short Task Notes

- Task 01 explains what `SessionMiddleware` and `AuthenticationMiddleware` do.
- Task 02 prepares the lesson dependencies for Django, DRF, Simple JWT, and Djoser.
- Task 03 configures DRF and JWT authentication in Django settings.
- Task 04 exposes Djoser authentication and JWT URLs under `/auth/`.
- Task 05 registers a user with `POST /auth/users/`.
- Task 06 logs in with `POST /auth/jwt/create/` and inspects the access token payload.
- Task 07 adds custom middleware that prints the HTTP method and response status.
- Task 08 adds a protected DRF `APIView` under `/user/`.
- Task 09 uses the `SIMPLE_JWT` token lifetime setting and tests the protected endpoint before and after expiry.
- Task 10 uses a refresh token to get a new access token and test the protected endpoint again.
