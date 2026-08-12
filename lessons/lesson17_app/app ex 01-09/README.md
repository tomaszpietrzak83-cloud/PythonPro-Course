
# App exercises (app ex 01-09)

This is a small educational Flask application using SQLAlchemy. It contains simple example routes and templates for learning purposes.

Key files:

- `app.py` — Flask app and routes
- `database.py` — SQLAlchemy engine and session
- `models.py` — SQLAlchemy models (Product)
- `init_db.py` — creates the SQLite database and tables

Setup and run

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix / macOS
source .venv/bin/activate
```

2. Install dependencies (from repository root):

```bash
pip install -r requirements.txt
```

3. Initialize the database (creates `products.db` in this folder):

```bash
python init_db.py
```

4. Run the app:

```bash
python app.py
```

Notes

- Templates are in the `templates/` folder: `movies.html`, `book.html`, `gallery.html`, `products.html`.
- The `/products` route loads products from the local SQLite database.
- For development, the Flask app runs with `debug=True` in `app.py`.
