from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'todo_orm.db'}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Generator sesji bazy danych."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Import modeli i utwórz tabele, jeśli ich jeszcze nie ma.
# To wygodne podczas developmentu — migracje Alembic nadal działają
# jeśli użyjesz `alembic upgrade head` zamiast tej automatycznej ścieżki.
try:
    from .models import Base

    Base.metadata.create_all(bind=engine)
except Exception as e:  # noqa: BLE001
    # Nie przerywamy importu aplikacji jeśli tworzenie schematu się nie powiedzie.
    print(f"Error occurred while creating tables: {e}")
