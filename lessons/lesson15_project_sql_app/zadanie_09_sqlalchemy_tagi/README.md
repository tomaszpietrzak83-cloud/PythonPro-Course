# Zadanie 9 - tagi w SQLAlchemy

Ten katalog zawiera osobne rozwiazanie zadania 9 z relacja wiele-do-wielu:
- model `Zadanie`,
- model `Tag`,
- tabele posrednia `zadanie_tagi`,
- migracje Alembic,
- aplikacje konsolowa z opcja dodawania taga do zadania.

Uruchomienie:

```bash
alembic upgrade head
python app_orm.py
```

Jesli uruchamiasz migracje spoza tego katalogu, podaj plik konfiguracyjny jawnie:

```bash
python -m alembic -c C:\sciezka\do\zadanie_09_sqlalchemy_tagi\alembic.ini upgrade head
```

Na co zwrocic uwage:
- `relationship(..., secondary=...)` laczy `zadania` i `tagi`,
- tabela `zadanie_tagi` przechowuje same powiazania,
- funkcja `get_or_create_tag()` tworzy tag tylko wtedy, gdy jeszcze nie istnieje,
- migracje sa lepsze od `create_all()` wtedy, gdy chcesz rozwijac schemat bazy krok po kroku.
- `ensure_database_ready()` zatrzymuje aplikacje z czytelnym komunikatem, jesli baza nie zostala jeszcze przygotowana migracjami.
