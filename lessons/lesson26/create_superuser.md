# Create a Django Superuser and Open the Admin Panel

In Django, the name **superuser** is correct. A superuser is an administrator account with full access to the Django admin panel.

## 1. Go to the Django project directory

Open PowerShell and move to the directory that contains `manage.py`:

```powershell
cd .\lessons\lesson26\l26_pro
```

## 2. Apply database migrations

Before creating the admin user, make sure the database tables exist:

```powershell
python manage.py migrate
```

If you are using the course virtual environment without activating it, you can run:

```powershell
..\..\..\.venv\Scripts\python.exe manage.py migrate
```

## 3. Create the superuser

Run:

```powershell
python manage.py createsuperuser
```

If you are using the course virtual environment without activating it:

```powershell
..\..\..\.venv\Scripts\python.exe manage.py createsuperuser
```

Django will ask for:

- username
- email address
- password
- password confirmation

When typing the password, PowerShell may not show any characters. This is normal.

## 4. Start the Django server

Run:

```powershell
python manage.py runserver
```

Or, without activating the course virtual environment:

```powershell
..\..\..\.venv\Scripts\python.exe manage.py runserver
```

## 5. Open the admin panel

In your browser, go to:

```text
http://127.0.0.1:8000/admin/
```

Log in with the username and password you created with `createsuperuser`.

## Common Problems

If the admin page shows a database error, run:

```powershell
python manage.py migrate
```

If `python` does not use the correct environment, activate the course virtual environment first or use the full path to `.venv\Scripts\python.exe`.
