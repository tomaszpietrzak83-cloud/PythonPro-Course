# API Lab — lekcja 28

Niezależny projekt Django w `lessons/lesson28/api_lab`. Korzysta z własnych aplikacji,
adresów i bazy `.runtime/lab.sqlite3`. GameShelf pozostaje w `../l28_pro`.

## Uruchomienie z katalogu kursu

Projekt korzysta ze wspólnego `.venv` w głównym katalogu kursu.

```powershell
python setup_course.py
.\.venv\Scripts\python.exe lessons\lesson28\api_lab\run_app.py
```

Launcher wybiera wspólny interpreter również przy uruchomieniu innym Pythonem.

Launcher wykonuje migracje, uzupełnia dane startowe i uruchamia serwer pod
http://127.0.0.1:8028/. Otwiera przeglądarkę. Ctrl+C zatrzymuje serwer.
Opcje: `--no-browser`, `--port 8038`. Jeśli port jest zajęty, launcher zgłasza błąd; wybierz inny port.
Wypisuje jej PID i czeka na zwolnienie portu. Na Windows używa narzędzi systemowych;
na Linux/macOS wymaga `lsof`.

## Przykłady

| Nr | Temat | Powiązanie z lesson-28.md |
|---|---|---|
| 1 | Automatyczna dokumentacja z serializera | Rozdział 3 |
| 2 | Jeden schemat, Swagger UI i ReDoc | Rozdziały 2–3 |
| 3 | Porównanie opisu z docstringa z widokiem automatycznym | Rozdział 5 |
| 4 | Parametr category i rzeczywiste filtrowanie | Rozdział 6 |
| 5 | Tworzenie produktu, przykład JSON, walidacja 400 i sukces 201 | Rozdział 6 |
| 6 | Szczegóły produktu, summary/description/tags, 200 i 404 | Rozdział 6 |
| 7 | DELETE, OpenApiResponse, 204 bez treści i 404 | Rozdział 6 |
| 8 | Oddzielne wejście/wyjście analizy tekstu i limit 500 znaków | Rozdział 7 |

Każdy kafelek zawiera: Wstęp, Zastosowania i demo, Krok po kroku, Cały kod,
Pytania z ukrytymi odpowiedziami. Tryb slajdów/ciągły jest zapamiętywany.
Główna ścieżka obejmuje też sekcję **Porównaj dokumentację** przed wykonaniem operacji.
Wersje: sam kod, docstring, `@extend_schema` (przypisany do metod przez `@extend_schema_view`).
Po lewej jest rzeczywisty kod, po prawej opis pobrany z aktualnego schematu OpenAPI.
Można przełączać GET/POST/DELETE i rozwinąć prawdziwy Swagger UI wewnątrz prezentacji.
Każda wersja ma oddzielny schemat i adresy `/api/v1/comparison/{wersja}/products/`,
ale korzysta z tych samych modeli, serializera i bazy. Demo wykonuje żądania
do wybranej wersji i porównuje otrzymany kod HTTP z jej dokumentacją.
Brak opisu błędu w wersji automatycznej jest celowy: generator nie odgaduje wszystkich
możliwych błędów. Dekorator uzupełnia m.in. 400 dla POST oraz 404 dla DELETE.
Układ i ścieżka nauki nawiązują do lekcji 29; treść jest po polsku.
Fragmenty i pełne pliki są czytane z aktualnych źródeł, z kolorowaniem składni.

Panel demo wysyła prawdziwe żądania i pokazuje HTTP, treść oraz nagłówki odpowiedzi.
Każdy przykład ma gotowe przyciski GET, POST (utworzenie i błąd walidacji) oraz DELETE.
Kliknięcie demonstracji od razu wysyła żądanie. Formularz pokazuje wysłane dane,
a pod wynikiem HTTP znajduje się objaśnienie i wskazówka kolejnego kroku.
Wstęp wyjaśnia API na przykładzie sklepu: kliknięcie, prośba do serwera, zapis i odpowiedź.
Ćwiczenie prowadzi przez obejrzenie listy, dodanie notesu, usunięcie go i sprawdzenie listy.
Produkty są pokazane czytelnie z nazwą, ceną i numerem; formularz oraz JSON można rozwinąć.
Po udanym POST panel zapamiętuje ID utworzonego produktu i przygotowuje jego adres
do DELETE. Usunięcie daje 204 bez treści, ponowne wysłanie DELETE daje 404.
Produkty są wspólne dla wszystkich przykładów. Po POST użyj zwróconego ID w GET/DELETE.
Kategorie startowe: 1 — Papier i biuro, 2 — Elektronika. Nieprawidłowy parametr
category daje 400, nieistniejąca kategoria daje pustą listę. Brak produktu daje 404.

Schemat: `/api/schema/?format=json`, Swagger: `/api/schema/swagger-ui/`,
ReDoc: `/api/schema/redoc/`. Zasoby obu interfejsów są lokalne dzięki sidecar.
Zmiany przez POST i DELETE wymagają CSRF, również dla anonimowego użytkownika.
Strona laboratorium oraz Swagger UI pobierają token ze swojego widoku.

Analiza sentymentu to demonstracja słownikowa, bez usług zewnętrznych i modelu AI.
Nie rozumie negacji ani ironii; nie podaje fikcyjnego confidence_score.
API jest lokalnym ćwiczeniem i nie wymaga konta.

## Pliki

- `academy/settings.py`, `academy/urls.py` — konfiguracja i dokumentacja.
- `laboratory/models.py`, `serializers.py`, `api.py` — działające API.
- `laboratory/comparison_api.py`, `documentation.py` — trzy wersje dokumentacji i odczyt rzeczywistego OpenAPI.
- `laboratory/curriculum.py` — scenariusze, zastosowania, kroki i pytania.
- `laboratory/views.py` — prezentacja i pobieranie kodu z rzeczywistych plików.
- `laboratory/templates`, `laboratory/static` — interfejs edukacyjny.
- `laboratory/management/commands/seed_lab.py` — uzupełnienie danych startowych.

Seed nie nadpisuje istniejących rekordów. Przy kolejnym uruchomieniu uzupełnia
brakujące produkty o ID 1–3. Dodatkowe produkty pozostają w bazie.

## Weryfikacja

```powershell
.venv\Scripts\python.exe lessons\lesson28\api_lab\manage.py check
.venv\Scripts\python.exe lessons\lesson28\api_lab\manage.py test laboratory
.venv\Scripts\python.exe lessons\lesson28\api_lab\manage.py spectacular --validate --fail-on-warn --file lessons\lesson28\api_lab\.runtime\schema.yaml
```

Dokumentacja biblioteki: https://drf-spectacular.readthedocs.io/en/stable/readme.html
