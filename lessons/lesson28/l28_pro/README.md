# GameShelf 0.5.0

Katalog gier z rejestracją i prywatną biblioteką użytkownika. Gra może należeć
do posiadanych albo wishlisty. W bibliotece można edytować status rozgrywki,
opcjonalną ocenę 1–10 i prywatną notatkę oraz usunąć wpis po potwierdzeniu.
Usunięcie wpisu nie usuwa gry z katalogu.

## Uruchamianie

Korzystaj ze wspólnego `.venv` kursu. Polecenia `manage.py` wykonuj z tego folderu.
Konfiguracja PostgreSQL i Django jest pobierana z lokalnego `../.env`.

```powershell
python manage.py migrate
python manage.py runserver
```

Katalog: `/games/`, biblioteka: `/library/`, panel administratora: `/admin/`.

## Seeder

```powershell
# Domyślnie 100 fikcyjnych gier, bez tworzenia użytkowników.
python manage.py seed_db

# 3 użytkowników, po 10 gier w każdej bibliotece.
python manage.py seed_db --games 100 --users 3 --entries-per-user 10 --seed 28
```

- Każda gra ma gatunek i tag FAKE oraz dodatkowy fikcyjny gatunek/tag.
- Polecenie wykorzystuje istniejące identyfikatory `Game.seed_key` i dodaje
  brakujące rekordy. Ponowne uruchomienie nie nadpisuje tytułów, ocen, notatek
  ani haseł. Mniejsze wartości opcji nie usuwają wcześniejszych danych.
- Użytkownicy mają nazwy `gameshelf_fake_001`, `gameshelf_fake_002` itd.
  Grupa `GameShelf seeded users` oznacza konta seedera i nie nadaje uprawnień.
  Kolizja z ręcznie utworzonym kontem przerywa polecenie i wycofuje jego zmiany.
- `--entries-per-user` wymaga `--users` i nie może przekraczać `--games`.
  Wpisy obejmują posiadane gry i wishlistę, przykładowe statusy, oceny i notatki.

Domyślnie nowe konta testowe mają nieużywalne hasło. Aby umożliwić im logowanie,
przed pierwszym utworzeniem ustaw własne silne hasło w zmiennej środowiskowej
`GAMESHELF_SEED_PASSWORD` (lub lokalnym, ignorowanym przez Git pliku `../.env`):

```powershell
python manage.py seed_db --users 3 --entries-per-user 10 --user-password-env GAMESHELF_SEED_PASSWORD
```

Seeder odczyta hasło ze zmiennej i zastosuje je wyłącznie do **nowych** kont.
Nie wypisuje hasła. Hasło istniejącego konta można zmienić w panelu admina.

## Panel admina

Listy wspierają wyszukiwanie, filtrowanie i sortowanie. Gry pokazują liczbę
użytkowników, którzy je zapisali; studia, gatunki i tagi pokazują liczbę gier.
Przy grze można edytować powiązane wpisy bibliotek. Prywatne notatki nie trafiają
do publicznego katalogu; uprawniony administrator ma dostęp do nich w formularzu wpisu.

## Sprawdzanie

```powershell
python manage.py test GameShelf
python manage.py check
python manage.py makemigrations --check --dry-run
```

Warto prześledzić `UserGameEditForm` (lista dozwolonych pól), widoki biblioteki
(`user=request.user`), ograniczenia bazy w `UserGame.Meta` i różnicę między
`get_or_create` a `update_or_create`. Dokumentacja etapów: `../roadmap_done.md`.
