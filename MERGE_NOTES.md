# Informacje do scalenia wspólnego środowiska kursu

Zmiany przygotowane 8 października 2026 mają umożliwić korzystanie z jednego środowiska Python na wszystkich lekcjach, również na Windows i w katalogu ze spacjami. PostgreSQL pozostaje bazą projektów, które używały go wcześniej. Brak serwera na tym komputerze nie jest powodem do zamiany ich bazy na SQLite.

## Punkt wyjścia i zakres zmian

Punkt wyjścia: gałąź `main`, commit `c20ab91380d3d45aaf324f42416af9a8989b0ebe`. Aktualnie wybrana gałąź to `shared-course-env`. Poprawki pozostają lokalne i nie zostały jeszcze zacommitowane ani wypchnięte.

Przed pracą w katalogu znajdowały się już nieśledzone pliki API Lab z lekcji 28 i projektu lekcji 29. Nie należy traktować wszystkich nieśledzonych plików jako nowych poprawek środowiska. Przejrzyj te projekty osobno przed dodaniem ich do commita. Lokalna zmiana w `lessons/lesson20/myproject/myproject/urls.py`, usuwająca komentarz początkowy, nie pochodzi z opisanej naprawy środowiska.

## Dlaczego zmiany były potrzebne

| Problem | Rozwiązanie | Znaczenie przy scalaniu |
| --- | --- | --- |
| Windows blokował `_ctypes` starego lokalnego Pythona 3.12.13. Importy Django i Flask kończyły się błędem. | Lokalny runtime 3.12.14 i odtworzenie interpretera wspólnego `.venv`. | Nie przenosić runtime ani `.venv` przez Git. Nie zmieniano zasad bezpieczeństwa Windows. |
| Pliki zależności lekcji zawierały sprzeczne wersje Django, Flask i SQLAlchemy. | Wspólne `requirements.txt`; wersje sprawdzone w `requirements-lock.txt`; listy lekcji odsyłają do głównej listy. | Zachować spójny zestaw zależności. Nie przywracać pojedynczych starych pinów bez ponownego sprawdzenia całego zestawu. |
| Instalatory tworzyły osobne środowiska lekcji. | Wszystkie wywołują `setup_course.py`; pozostaje jedno `.venv` w katalogu kursu. | Łączyć zmiany instalatorów razem z nowym modułem głównym. |
| Launchery używały przypadkowego interpretera; względne ścieżki zależały od miejsca uruchomienia. | `course_runtime.py` wybiera interpreter kursu; `run_lesson.py` ustawia katalog roboczy wybranego skryptu. | Nie wstawiać do kodu absolutnej ścieżki konta DELL ani adresów drugiego komputera. |
| `runserver.py` wykonywał migracje tylko po wykryciu zmian modeli. Istniejące migracje mogły pozostać niewykonane. | Kontrola konfiguracji, zastosowanie istniejących migracji, start serwera; opcje `--check`, `--no-migrate`, `--port`. | Zachować wykonywanie istniejących migracji. Nowe migracje tworzy się jawnie, bez automatycznego `makemigrations` przy starcie. |
| Celery na Windows wymagało `pywin32`. | Zależność z warunkiem `sys_platform == "win32"`. | Zachować warunek systemowy. Plik lock jest zestawem ograniczeń, nie bezwarunkową listą pakietów dla każdego systemu. |
| Backend plikowy Celery nie dekodował `%20` generowanego przez `Path.as_uri()` w ścieżce `Python Pro Course`. | Poprawiona lokalna ścieżka backendu; prawidłowa opcja `processed_folder`. | Zachować obsługę spacji oraz konfigurację ścieżek. Działanie w katalogu bez spacji nie potwierdza tej poprawki. |
| Bootstrap nadpisywał zależności pakietami aktywnego środowiska. | Bootstrap odsyła do instalatora kursu. | Nie przywracać automatycznego zapisywania przypadkowego `pip freeze` do list lekcji. |

Pozostałe małe poprawki: zapytanie SQL w `lesson13/04.py` miało cały SELECT po komentarzu `--sql` na jednej linii; demonstracja pustej listy w `lesson08/04.py` kończyła program nieobsłużonym oczekiwanym wyjątkiem. W lekcji 22 dostosowano nieaktualny test i opis podpowiedzi do istniejącego zachowania interfejsu i backendu od jednego znaku. Nie zmieniono progu podpowiedzi aplikacji.

## PostgreSQL bez zmiany kodu aplikacji

Na czas pracy bez serwera można odłożyć wyłącznie uruchamianie zadań wymagających PostgreSQL. Nie usuwać ich, nie wyłączać na stałe testów i nie zmieniać produkcyjnej konfiguracji projektów na SQLite. Lekcje 18, 19 i projekt GameShelf z lekcji 28 pozostają zależne od dostępności PostgreSQL; API Lab z lekcji 28 jest odrębną aplikacją SQLite.

Dostępne rozwiązania:

1. Korzystać z PostgreSQL na drugim komputerze, gdy jest włączony i osiągalny. W lokalnym, ignorowanym przez Git `.env` ustawić jego adres oraz poprawne dane logowania. Serwer musi przyjmować połączenia z tego komputera; wymaga to odpowiedniej konfiguracji nasłuchu, reguł `pg_hba.conf` i zapory. Szczegóły opisuje [dokumentacja PostgreSQL](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html).
2. Uruchomić PostgreSQL lokalnie, bez zmiany aplikacji. Odtworzyć osobną kopię baz z drugiego komputera albo utworzyć puste bazy i wykonać migracje oraz udokumentowane skrypty danych demonstracyjnych. Migracje tworzą schemat; nie odtwarzają automatycznie dotychczasowych rekordów.
3. Tymczasowo odłożyć zadania wymagające serwera i kontynuować pozostałe lekcje. To ograniczenie dostępności infrastruktury, nie zmiana rozwiązania zadania.

Django z lekcji 19 odczytuje `.env` w `lessons/lesson19`, a GameShelf w `lessons/lesson28`. Używają `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` i `DJANGO_SECRET_KEY`. Projekty Flask z lekcji 18 odczytują `DATABASE_URL`.

Nie utworzono tu rzeczywistych plików połączenia, bo adres serwera i dane logowania nie zostały podane. Nie sprawdzono zdalnego PostgreSQL ani nie kopiowano danych z drugiego komputera.

## Dane bazy i branch

Branch przechowuje wersje kodu i plików, nie stan działającego PostgreSQL. Dane przenosi się przez kopię bazy, np. `pg_dump` i `pg_restore`, poza repozytorium. [Dokumentacja pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html) opisuje odtwarzanie archiwów `pg_dump`. Dane przykładowe można utrzymywać jako przeglądane skrypty seed lub fixtures bez haseł i prywatnych rekordów.

Do przeglądu kodu zalecana jest tymczasowa gałąź, np. `shared-course-env`. Nie ma potrzeby utrzymywania na stałe osobnej wersji aplikacji dla tego komputera. Zmiany lokalnej konfiguracji zostają w `.env` i środowisku systemowym. Samo utworzenie brancha nie zapisuje niezacommitowanych zmian; przed przekazaniem ich do scalenia potrzebny jest przejrzany commit.

Nie dodawać do commita: `.venv`, `.python-runtime`, `.env`, cache, lokalnych baz i dumpów PostgreSQL. Cztery stare środowiska usunięto lokalnie; ich usunięcie nie jest migracją danych bazy i nie wymaga zmian na drugim komputerze.

## Wyniki i granice sprawdzenia

- Sprawdzono składnię 531 plików Python i niezdefiniowane nazwy.
- Przeszły kontrole konfiguracji 14 projektów Django i 33 istniejące testy Django.
- Sprawdzono pięć aplikacji Flask, cztery aplikacje konsolowe SQL i 12 launcherów `runserver.py` w trybie `--check`.
- W tymczasowych kopiach wystartowało 14 serwerów Django oraz launchery API Lab i Celery Lab. Worker Celery wykonał `6 × 7` i zwrócił `42`.
- Zależności wspólnego środowiska są zgodne według `pip check`.

Kontrole aplikacji korzystały z tymczasowych kopii, testowych baz SQLite i ustawień testowych. Start serwera nie oznacza sprawdzenia każdego endpointu; niektóre projekty nie mają widoku pod `/`. Wyniki nie potwierdzają poprawności docelowych połączeń PostgreSQL/Redis, wszystkich wariantów wejścia użytkownika, fragmentów kodu w materiałach Markdown ani usług AWS/OpenAI. Działania na drugim koncie nie zweryfikowano.

## Przebieg przeglądu i scalenia

1. Przejrzeć diff względem wskazanego commita i oddzielić poprawki środowiska od niezależnych zmian lekcji oraz wcześniej nieśledzonych projektów. Nie wykonywać zbiorczego dodawania wszystkich plików bez przeglądu.
2. Zachować razem `setup_course.py`, `course_runtime.py`, `run_lesson.py`, wspólne zależności oraz wywołujące je launchery i instalatory. Przeniesienie samych wrapperów bez modułów głównych zepsuje start.
3. Przy konfliktach zależności ustalić jeden zgodny zestaw wersji, sprawdzić go na Pythonie 3.12 i aktualizować lock na podstawie instalacji, a nie przez mechaniczne łączenie pinów obu stron. Obecny zestaw używa Django 5.2 zamiast historycznych pinów 6.1 w części lekcji.
4. Zachować istniejące migracje projektów. Naprawa środowiska nie tworzyła nowych migracji ani nie zamieniała docelowych baz PostgreSQL na SQLite.
5. Na obu komputerach uruchomić `setup_course.py`, wybrać główne `.venv`, powtórzyć kontrole i istniejące testy. Instrukcje znajdują się w `URUCHAMIANIE.md`; narzędzia kontroli to `audit_course.py` i `audit_startups.py`.
6. Na komputerze z dostępnym PostgreSQL dodatkowo sprawdzić połączenie, migracje oraz działania właściwych aplikacji na osobnej bazie testowej. Dopiero ta kontrola potwierdzi zachowanie z PostgreSQL.

Potencjalne konflikty dotyczą przede wszystkim list zależności, launcherów i instrukcji zmienianych równolegle. Lokalnych baz i ustawień kont nie należy rozwiązywać przez merge Git.
