
if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from course_runtime import use_course_python
    use_course_python(__file__)

from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config["development"])
db = SQLAlchemy(app)


class TestConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))


@app.route("/")
def index():
    return "Flask + PostgreSQL działa! 🎉"


@app.route("/test-db")
# TASK 01
def test_db():
    """Testuje połączenie z bazą."""
    try:
        db.session.execute(db.text("SELECT 1"))
        return "✅ Połączenie z PostgreSQL OK!"
    except Exception as e:
        return f"❌ Błąd połączenia: {str(e)}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tabele utworzone!")
    app.run(debug=True)
