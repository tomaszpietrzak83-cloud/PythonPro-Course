# Dziennik nauki

Ten dziennik powstal na podstawie historii commitow w `PythonPro-Course` oraz repozytoriach lekcyjnych zaimportowanych do niego przez `git subtree`.

## Oś czasu

| Data | Temat nauki | Widoczny postep |
| --- | --- | --- |
| 2026-04-17 | Pierwsze cwiczenia, pull requesty, commitlint | Poczatki pracy z GitHubem, branchami i konwencja commitow. |
| 2026-04-19 | Zmienne, funkcje, tablice, porzadkowanie plikow | Wiele refactorow: zmiana nazw zmiennych, wyciaganie funkcji, przenoszenie plikow. |
| 2026-04-20 - 2026-04-22 | Funkcje i logika warunkowa | Optymalizacja funkcji, alternatywne podejscia do zadan, pierwsze bardziej swiadome refactory. |
| 2026-04-24 - 2026-05-11 | Pliki, dane, kolejne zestawy cwiczen | Dodawanie cwiczen lekcji 08 i 09, praca z plikami tekstowymi, JSON, CSV i XLSX. |
| 2026-05-13 - 2026-05-18 | OOP, SQL, bazy danych | Lekcje 12-14: klasy, metody, diagram Mermaid, SQLite, zapytania i modele danych. |
| 2026-05-22 - 2026-05-31 | Projekty aplikacyjne i Git | Rozbudowa programu, wymagania, import brakujacych plikow, lekcja 16 i aplikacje lekcji 15/17. |
| 2026-06-05 - 2026-06-11 | Django i organizacja projektu | Aplikacje lekcji 18-20, `.gitignore`, czyszczenie `.venv` z repo, podstawy projektu Django. |
| 2026-06-20 - 2026-07-10 | Kolejne lekcje i merge branche | Lekcje 21-23, merge branchy lekcyjnych, dalsze dopracowywanie plikow. |
| 2026-08-06 - 2026-08-12 | Porzadkowanie repo i lepsze commity | Nowe materialy lekcji 09, trzy tematyczne commity do `lesson12`, scalenie repozytoriow lekcyjnych. |

## Najwazniejsze umiejetnosci widoczne w historii

- Podstawy Pythona: zmienne, warunki, petle, funkcje i formatowanie tekstu.
- Praca z plikami: TXT, JSON, CSV, XLSX oraz proste logi wynikow.
- OOP: klasy, `@dataclass`, properties, classmethod, staticmethod i `__str__` / `__repr__`.
- Obsluga bledow: `try` / `except`, wlasne klasy wyjatkow, walidacja danych.
- SQL i SQLite: tworzenie baz, zapytania, proste modele danych.
- Django: start projektu, aplikacje, struktura `manage.py`, `settings.py`, `urls.py`.
- Git: branche, merge, pull requesty, Conventional Commits, `.gitignore`, porzadkowanie historii bez rebase.

## Powtarzajace sie wzorce do poprawy

- Commit messages bywaly zbyt ogolne, np. `refactor: minor changes` albo `style: add white spaces`.
- Niektore commity laczyly za duzo zmian naraz.
- Nazwy plikow i katalogow mialy rozne style: `Lesson22`, `lesson-23`, `Lesson 17 app`, `lesson01`.
- Wczesniej pojawial sie problem z virtualenv i globalnym `pip`; od teraz `.venv` powinien byc lokalny i ignorowany.

## Dobre praktyki od teraz

1. Jeden commit powinien miec jeden glowny temat.
2. Commit message powinien odpowiadac na pytanie: co zmienilem i po co.
3. Przed commitem warto uruchomic przynajmniej sprawdzenie skladni:

```bash
python -m py_compile path/to/file.py
```

4. Dla nowych lekcji warto trzymac spójny katalog:

```text
lessons/lesson25/
```

5. Przy pracy z Django instalacje robic w aktywnym `.venv`:

```bash
source .venv/Scripts/activate
python -m pip install django
```

## Przyklad lepszych commitow z lesson12

Zamiast jednego duzego commita `refactor: minor changes`, zmiany zostaly podzielone tak:

```text
feat(lesson12): extend object model exercises
refactor(lesson12): simplify calculator exercises
feat(lesson12): add custom validation exceptions
```

To jest dobry kierunek: commit nie musi byc idealny, ale powinien mowic czytelnikowi, jaki byl temat zmiany.
