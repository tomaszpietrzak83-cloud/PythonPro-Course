# Registry app

Simple registration app built with Flask and SQLAlchemy.

Key files:

- `app.py` — Flask app and registration routes
- `database.py` — SQLAlchemy engine and session
- `models.py` — SQLAlchemy models (`Registry`)
- `init_db.py` — creates the SQLite database and tables

Setup and run

1. Create and activate a virtual environment (from repository root):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix / macOS
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the database (creates `registry.db`):

```bash
python init_db.py
```

4. Run the app:

```bash
python app.py
```

After successful registration the form redirects to the confirmation page `ty.html`.
