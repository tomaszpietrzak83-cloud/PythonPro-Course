# Zadanie 8 - refaktoryzacja do klas

Ten katalog zawiera rozwiazanie zadania 8 w osobnej, bezpiecznej kopii.

Pliki:
- `task_manager_raw.py` - klasa `TaskManagerRaw`, ktora obsluguje cala baze SQLite.
- `app_raw_sql_class.py` - prosta aplikacja konsolowa korzystajaca z tej klasy.

Uruchomienie:

```bash
python app_raw_sql_class.py
```

Najwazniejsze rzeczy do przeanalizowania:
- konstruktor `__init__`, ktory od razu inicjalizuje baze,
- metody prywatne `_connect()` i `_initialize_database()`,
- `cursor.lastrowid`, dzieki ktoremu dostajesz ID nowego rekordu,
- `cursor.rowcount`, dzieki ktoremu sprawdzasz, czy `UPDATE` albo `DELETE` cos zmienily.
