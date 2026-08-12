# Importujemy Path, aby stabilnie zbudowac sciezke do pliku bazy danych.
from pathlib import Path

# Importujemy create_engine do utworzenia polaczenia z baza.
from sqlalchemy import create_engine, inspect
# Importujemy sessionmaker do tworzenia sesji ORM.
from sqlalchemy.orm import sessionmaker


# Wyznaczamy katalog glowny tego rozwiazania.
BASE_DIR = Path(__file__).resolve().parent.parent
# Budujemy pelna sciezke do pliku SQLite.
DATABASE_FILE = BASE_DIR / "todo_orm_tags.db"
# Budujemy URL bazy SQLite.
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"
# Tworzymy silnik SQLAlchemy.
engine = create_engine(DATABASE_URL, echo=False)
# Przygotowujemy fabryke sesji.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Funkcja sprawdza, czy baza zostala juz przygotowana migracjami.
def ensure_database_ready() -> None:
    # Najpierw sprawdzamy, czy sam plik bazy istnieje.
    if not DATABASE_FILE.exists():
        # Jesli nie, przerywamy z jasna instrukcja dla uzytkownika.
        raise RuntimeError(
            "Baza danych nie jest jeszcze zainicjalizowana. "
            "Uruchom migracje poleceniem: alembic upgrade head "
            "w katalogu zadanie_09_sqlalchemy_tagi."
        )

    # Odczytujemy liste tabel istniejacych w pliku bazy.
    existing_tables = set(inspect(engine).get_table_names())
    # Definiujemy minimalny zestaw tabel wymaganych przez aplikacje.
    required_tables = {"zadania", "tagi", "zadanie_tagi", "alembic_version"}
    # Sprawdzamy, czy wszystkie potrzebne tabele sa obecne.
    if not required_tables.issubset(existing_tables):
        # Przygotowujemy czytelna liste brakujacych tabel.
        missing_tables = ", ".join(sorted(required_tables - existing_tables))
        # Zglaszamy blad z instrukcja naprawy.
        raise RuntimeError(
            "Baza danych istnieje, ale nie ma pelnego schematu. "
            f"Brakujace tabele: {missing_tables}. "
            "Uruchom migracje poleceniem: alembic upgrade head "
            "w katalogu zadanie_09_sqlalchemy_tagi."
        )


# Generator get_db przydaje sie np. wtedy, gdy zechcesz podpiac FastAPI.
def get_db():
    # Tworzymy nowa sesje.
    db = SessionLocal()
    # Wchodzimy do bloku try, aby zawsze domknac polaczenie.
    try:
        # Zwracamy sesje wywolujacemu.
        yield db
    # Blok finally wykona sie po zakonczeniu generatora.
    finally:
        # Zamykamy sesje.
        db.close()
