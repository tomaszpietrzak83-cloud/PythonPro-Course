# Lekcja 33 · FastAPI Studio

Lokalna aplikacja edukacyjna obejmująca wszystkie 20 zadań z `tasks.md`.
Kod i komunikaty przykładów są po angielsku; interfejs, objaśnienia i pytania
mają przełącznik PL/ENG.

## Uruchomienie

Z katalogu głównego kursu, przy włączonym PostgreSQL:

```powershell
.venv\Scripts\python.exe lessons\lesson33\run_app.py
```

Adres: [http://127.0.0.1:8033/](http://127.0.0.1:8033/).
`--no-browser` pomija otwarcie przeglądarki. Ponowne uruchomienie restartuje tylko
serwer tej lekcji i jego procesy potomne, po sprawdzeniu ich tożsamości.

Konfiguracja PostgreSQL jest w ignorowanym `.env` lekcji 33. Osobna baza
`lesson33` została przygotowana przy użyciu danych lokalnego PostgreSQL
z `.env` lekcji 28. Hasło nie jest publikowane w kodzie, interfejsie ani Gicie.
W razie potrzeby `setup_database.py` tworzy brakującą bazę i lokalną konfigurację.
Na innym komputerze `.env` musi zawierać `DATABASE_URL` z driverem
`postgresql+asyncpg`, wskazujący bazę `lesson33`.

Zależności:

```powershell
.venv\Scripts\python.exe -m pip install -r lessons\lesson33\requirements.txt
```

## Kolejność nauki

Każde zadanie zawiera: **Treść zadania → Wstęp → Obserwuj działanie →
Zrozum kod → Cały kod → Pytania**.

Wstęp ma trzy slajdy:

1. Pojęcie oraz najważniejsze nowe narzędzia.
2. **Jak zadziała to zadanie?** — konkretne dane, kolejność etapów i mapa przepływu.
3. **Jakiego wyniku się spodziewać?** — oczekiwane wartości, statusy oraz efekty uboczne.

Dzięki temu przed czytaniem kodu wiadomo, co będzie robił program.
Pokazy uruchamiają rzeczywisty serwer **Uvicorn** i klienta **HTTPX**.
Panel „Żądanie → odpowiedź” pokazuje wysłany JSON, odebrane body i status.
W zadaniach z plikami wyświetla także rzeczywistą zawartość plików po pokazie.

**Dokładne** jest domyślne przy otwarciu zadania i odświeżeniu strony.
Ten tryb omawia kolejne instrukcje, dekoratory, parametry i wywołania.
Instrukcje wielowierszowe są omawiane razem z dokładnym zakresem linii.
Gdy dokładnych slajdów jest ponad 20, dostępny jest przełącznik **Szybkie / Dokładne**.
Szybkie to osobna kompilacja mechanizmów, maksymalnie 20 slajdów.
W projektach 19–20 ma odpowiednio 9 i 10 slajdów.

Dostępne są tryb ciągły, większy tekst, pełny ekran, strzałki ←/→,
historia pokazów i odtwarzanie zarejestrowanego przebiegu.
Objaśnienia po polsku można czytać także w `explanations/task01.md`–`task20.md`.

## Organizacja plików

Każde zadanie ma osobny katalog `examples/task01`–`task20` oraz własny `main.py`.
Zadanie 9 ma dodatkowo `routers/books.py` i `routers/authors.py`.
Projekty 19 i 20 mają osobne `models.py`, `schemas.py`, `auth.py` i routery.
„Zrozum kod” automatycznie przełącza plik zgodnie z omawianym fragmentem,
a „Cały kod” udostępnia wszystkie pliki zadania oraz pomocniki.

Pomocniki:

- `demo_support.py`: fabryka sesji, lifecycle PostgreSQL i ścieżki plików pokazu.
- `lab_support.py`: rzeczywiste zdarzenia i pomiar czasu.
- `run_task.py`: start Uvicorn, klient HTTPX, sprawdzenie odpowiedzi i odczyt plików.
- `scenarios.py`: jawne żądania i oczekiwane wyniki każdego pokazu.

Pojedynczy pokaz z terminala:

```powershell
.venv\Scripts\python.exe lessons\lesson33\examples\run_task.py 14
```

Samodzielny serwer zadania (pozostaje uruchomiony do Ctrl+C):

```powershell
.venv\Scripts\python.exe lessons\lesson33\examples\run_task.py 8 --serve --port 8133
```

Wówczas Swagger jest pod [http://127.0.0.1:8133/docs](http://127.0.0.1:8133/docs).
Przycisk w aplikacji uruchamia go automatycznie. Jednocześnie działa jeden serwer
Swagger: wybranie dokumentacji innego zadania zamyka poprzedni serwer tej lekcji.
Ma on własne dane, niezależne od pokazów. Nie zamykamy obcych usług zajmujących port.
Domyślny Swagger UI ładuje pliki JS/CSS z CDN, więc jego interfejs potrzebuje internetu;
same pokazy i schemat OpenAPI nie potrzebują zewnętrznych API.

Zadania bez wspólnego pomocnika można uruchamiać również bezpośrednio przez
`uvicorn main:app --app-dir lessons/lesson33/examples/task01 --reload`.
Dla pozostałych prostszą opcją jest powyższy `run_task.py --serve`, który ustawia
ścieżkę importów. Polecenie Uvicorn wymaga aktywnego środowiska kursu.

## Mapa zadań

| Zadania | Weryfikowany mechanizm |
|---|---|
| 01–04 | Trasy, czas UTC, losowanie, Path, query, kalkulator, model Product. |
| 05–06 | CRUD w pamięci, a następnie statusy 201/204/404. |
| 07–08 | EmailStr i dokumentacja OpenAPI/Swagger. |
| 09–12 | APIRouter, dependency klucza API, zagnieżdżone modele i field_validator. |
| 13–14 | Prawdziwy async PostgreSQL CRUD, relacja autor–książki i selectinload. |
| 15–17 | BackgroundTasks, pliki, middleware, X-Request-ID i lifespan z cache. |
| 18 | Filtry, sortowanie z listą dozwolonych pól, offset i limit. |
| 19 | Blog: CRUD użytkowników/postów, sprawdzanie autora, komentarze i powiadomienie. |
| 20 | Rozszerzenie bloga o jawne symulacje podsumowania, sentymentu i moderacji. |

Każdy pokaz SQL tworzy losowy schemat `demo_...` w bazie `lesson33`, po zakończeniu
usuwa go i zamyka połączenia. Pliki wynikowe pozostają w osobnych katalogach
`.runtime/taskXX-...`, aby można było je sprawdzić. Wymuszone zabicie procesu może
pozostawić schemat demonstracyjny; nie wpływa na dane pozostałych lekcji.
Pokazy słowników zaczynają od pustych danych. Od zadania 13 ceny w bazie są całkowite,
w groszach; wcześniejsze modele używają prostych wartości liczbowych z poleceń.

Pydantic używa składni v2 (`field_validator`, `model_dump`, `ConfigDict`).
Start/zamknięcie pokazujemy przez `lifespan`. Modele ORM i Pydantic są oddzielone.
Sesja żądania jest zamykana przez dependency z `yield`; transakcja przez `db.begin()`.

Klucz `lesson-demo-key` z zadania 10 jest publiczną daną ćwiczenia.
Blog używa `demo-anna-key` dla konta ID 1 i `demo-jan-key` dla ID 2.
To demonstracja identyfikacji i autoryzacji, a nie gotowy system kont do wdrożenia.
Autor posta zawsze pochodzi z dependency, nigdy z dowolnego `user_id` w JSON.
Podsumowanie to pierwszych 12 słów; sentyment używa słów great/bad; moderacja
odrzuca demonstracyjny znacznik forbiddenword. Żaden email nie jest wysyłany.
Te reguły pokazują przepływ danych, nie jakość prawdziwego modelu AI.

## Testy i edycja

```powershell
.venv\Scripts\python.exe lessons\lesson33\test_lesson33.py
```

Testy uruchamiają wszystkie 20 przykładów z prawdziwym HTTP i PostgreSQL.
Sprawdzają statusy, konkretne wyniki, walidację, blokowanie cudzej edycji,
rollback konfliktu nazwy, efekty BackgroundTasks, pliki cache/logów,
kompletność zakresów objaśnień, limit wersji szybkiej, CSRF oraz dostęp do źródeł.

Po zmianie przykładu przejrzyj odpowiadające mu opisy w `teaching.py`
i `course_content.py`, a następnie uruchom `create_material.py`.
Zmiany samego formatowania, kolejności importów i usunięcie nieużywanych importów
są wykrywane przy starcie oraz wczytywaniu materiałów: zakresy objaśnień
przeliczają się automatycznie. Zmiana logiki nadal wymaga przeglądu objaśnień;
launcher zgłosi konkretny plik zamiast czekać na odpowiedź z błędem 500.
`build_examples.py` służy wyłącznie do odtworzenia bazowych rozwiązań:
jego uruchomienie **nadpisuje pliki zadań**, więc nie uruchamiaj go na własnych zmianach.

Dokumentacja: [FastAPI](https://fastapi.tiangolo.com/tutorial/),
[BackgroundTasks](https://fastapi.tiangolo.com/tutorial/background-tasks/),
[Pydantic](https://docs.pydantic.dev/latest/),
[SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).
