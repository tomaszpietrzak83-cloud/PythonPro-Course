# Importujemy konfiguracje loggerow z pliku ini.
from logging.config import fileConfig

# Importujemy obiekt context z Alembic.
from alembic import context
# Importujemy funkcje do tworzenia silnika SQLAlchemy.
from sqlalchemy import engine_from_config, pool
# Importujemy ten sam URL bazy, z ktorego korzysta aplikacja.
from sqlalchemy_app.database import DATABASE_URL
# Importujemy metadata modeli, aby Alembic mogl porownywac schemat.
from sqlalchemy_app.models import Base


# Pobieramy konfiguracje Alembic.
config = context.config

# Jesli istnieje plik konfiguracyjny, ustawiamy logowanie.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Nadpisujemy URL z pliku ini, aby Alembic i aplikacja zawsze trafialy
# do dokladnie tego samego pliku bazy danych, niezaleznie od katalogu uruchomienia.
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Przekazujemy metadata modelu do autogenerowania migracji.
target_metadata = Base.metadata


# Funkcja uruchamia migracje w trybie offline.
def run_migrations_offline() -> None:
    # Pobieramy URL bazy danych z pliku ini.
    url = config.get_main_option("sqlalchemy.url")
    # Konfigurujemy context bez otwierania polaczenia DBAPI.
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Otwieramy transakcje migracyjna.
    with context.begin_transaction():
        # Uruchamiamy migracje.
        context.run_migrations()


# Funkcja uruchamia migracje w trybie online.
def run_migrations_online() -> None:
    # Tworzymy obiekt silnika na podstawie configu.
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Otwieramy polaczenie z baza danych.
    with connectable.connect() as connection:
        # Konfigurujemy context z aktywnym polaczeniem.
        context.configure(connection=connection, target_metadata=target_metadata)

        # Rozpoczynamy transakcje migracyjna.
        with context.begin_transaction():
            # Wykonujemy migracje.
            context.run_migrations()


# Wybieramy odpowiedni tryb pracy Alembic.
if context.is_offline_mode():
    # Uruchamiamy migracje offline.
    run_migrations_offline()
else:
    # Uruchamiamy migracje online.
    run_migrations_online()
