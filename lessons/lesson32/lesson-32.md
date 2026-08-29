# Lekcja 32: Budowanie asynchronicznych API z Aiohttp i Async SQLAlchemy

`#lekcja` `#python` `#asyncio` `#aiohttp` `#sqlalchemy` `#web` `#api`

W poprzednich lekcjach omówiliśmy teorię asynchroniczności, korutyny, pętlę zdarzeń i moduł `asyncio`.

Teraz przechodzimy do praktyki. Zobaczymy, jak tworzyć aplikacje webowe, które mogą obsługiwać wiele jednoczesnych połączeń.

W tej lekcji użyjemy:

- `aiohttp` - asynchronicznego frameworka webowego,
- asynchronicznego SQLAlchemy - do nieblokującej komunikacji z bazą danych.

## 1. Dlaczego asynchroniczność?

Operacje blokujące spowalniają aplikacje. Są to zadania I/O-bound, czyli związane z wejściem i wyjściem.

Przykłady:

- wysyłanie zapytania do bazy danych i czekanie na odpowiedź,
- odczytywanie dużego pliku z dysku,
- wysyłanie zapytania do zewnętrznego API, na przykład pogody, kursów walut albo modelu AI.

> [!definition]
>
> Operacja I/O-bound to taka, w której czas wykonania jest zdominowany przez oczekiwanie na zasoby zewnętrzne: dysk, sieć albo bazę danych, a nie przez obliczenia procesora.

W podejściu synchronicznym program czeka na każde zapytanie po kolei.

W podejściu asynchronicznym może rozpocząć kilka operacji i wrócić do nich, gdy odpowiedzi będą gotowe.

Przykład:

```python
import asyncio
import time


async def fetch_data(task_id: int, delay: int) -> str:
    """
    Asynchroniczna korutyna symulująca pobieranie danych.
    """
    print(f"[Task {task_id}] Rozpoczynam pobieranie danych (potrwa {delay}s)...")

    await asyncio.sleep(delay)

    print(f"[Task {task_id}] Dane pobrane.")
    return f"Dane z zadania {task_id}"


async def main():
    start_time = time.time()
    print("Uruchamiam zadania asynchronicznie...")

    tasks_to_run = [
        fetch_data(1, 2),
        fetch_data(2, 1),
        fetch_data(3, 3),
    ]

    results = await asyncio.gather(*tasks_to_run)

    print(f"\nOtrzymane wyniki: {results}")
    print(f"Całkowity czas wykonania: {time.time() - start_time:.2f} sekundy")


if __name__ == "__main__":
    asyncio.run(main())
```

> [!note]
>
> Suma opóźnień to 2 + 1 + 3 = 6 sekund, ale program powinien wykonać się w około 3 sekundy, czyli tyle, ile trwa najdłuższe zadanie.

<p style="color:red"><strong>Komentarz mentora:</strong> W kodzie asynchronicznym używaj nieblokujących funkcji, na przykład `await asyncio.sleep()`. Zwykłe `time.sleep()` zablokuje cały event loop.</p>

## 2. Wprowadzenie do Aiohttp

Znacie już Flaska i Django. Działają one historycznie w oparciu o standard WSGI, który jest synchroniczny.

Dla aplikacji asynchronicznych powstał standard ASGI. `aiohttp` jest frameworkiem napisanym z myślą o `asyncio`.

> [!definition]
>
> Aiohttp to asynchroniczny framework webowy dla Pythona. Składa się z klienta HTTP oraz serwera do budowania asynchronicznych aplikacji webowych.

Instalacja:

```bash
pip install aiohttp
```

Pierwszy serwer:

```python
from aiohttp import web


async def handle_hello(request):
    """
    Handler obsługujący GET na ścieżce '/'.
    """
    name = request.query.get("name", "Świecie")
    return web.Response(text=f"Witaj, {name}!", content_type="text/html")


app = web.Application()
app.router.add_get("/", handle_hello)


if __name__ == "__main__":
    print("Uruchamiam serwer na http://127.0.0.1:8080")
    web.run_app(app, host="127.0.0.1", port=8080)
```

Po uruchomieniu wejdź w przeglądarce na:

```text
http://127.0.0.1:8080
http://127.0.0.1:8080/?name=Student
```

## 3. Aiohttp i AI

Asynchroniczność jest ważna dla aplikacji AI, bo wiele z nich wykonuje długie operacje I/O:

1. odbiera zapytanie od użytkownika,
2. wysyła zapytanie do modelu językowego,
3. pobiera historię użytkownika z bazy danych,
4. łączy wyniki i zwraca odpowiedź.

`aiohttp` dobrze pasuje do budowania takich bramek do usług AI, ponieważ może obsługiwać wiele oczekujących połączeń bez blokowania serwera.

## 4. Architektura aplikacji Aiohttp

Najważniejsze elementy aplikacji `aiohttp`:

1. **Aplikacja (`web.Application`)** - główny obiekt przechowujący trasy, ustawienia, middleware i stan.
2. **Handlery** - asynchroniczne funkcje `async def`, które przyjmują `request` i zwracają `response`.
3. **Router** - mapuje ścieżki URL i metody HTTP na handlery.
4. **Sygnały startup/cleanup** - funkcje uruchamiane przy starcie i zamykaniu serwera.

Przykład:

```python
from aiohttp import web


async def handle_index(request):
    counter = request.app["app_counter"]
    return web.Response(text=f"Strona główna. Licznik startów serwera: {counter}")


async def handle_user(request):
    user_id = request.match_info.get("id", "0")

    try:
        user_id_int = int(user_id)
        return web.Response(text=f"Dane użytkownika o ID: {user_id_int}")
    except ValueError:
        raise web.HTTPBadRequest(text="ID użytkownika musi być liczbą")


async def on_startup(app):
    print("Serwer startuje! Inicjalizuję zasoby...")
    app["app_counter"] = app.get("app_counter", 0) + 1


async def on_cleanup(app):
    print("Serwer się zamyka. Czyszczę zasoby.")


def create_app():
    app = web.Application()

    app.router.add_get("/", handle_index)
    app.router.add_get("/user/{id}", handle_user)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=8080)
```

## 5. Routing w Aiohttp

> [!definition]
>
> Routing to proces mapowania adresu URL i metody HTTP na konkretną funkcję w kodzie, która obsłuży zapytanie.

Podstawowe metody dodawania tras:

```python
app.router.add_get(sciezka, handler)
app.router.add_post(sciezka, handler)
app.router.add_put(sciezka, handler)
app.router.add_delete(sciezka, handler)
app.router.add_route(metoda, sciezka, handler)
```

## 6. Obsługa danych wejściowych

W handlerze mamy dostęp do części zapytania przez obiekt `request`.

Przykład obsługi:

- dynamicznej części ścieżki,
- query params,
- danych JSON z body.

```python
import json

from aiohttp import web


async def handle_data_demo(request: web.Request):
    """
    Obsługuje POST na /api/demo/{id_uzytkownika}?kategoria=test
    """
    user_id = request.match_info.get("id")
    category = request.query.get("kategoria", "domyślna")

    data_source = "brak danych w ciele"

    if request.content_type == "application/json":
        try:
            json_data = await request.json()
            data_source = json_data.get("source", "nieznany")
        except json.JSONDecodeError:
            raise web.HTTPBadRequest(text="Niepoprawny format JSON")

    response_data = {
        "dynamic_path_id": user_id,
        "query_param_category": category,
        "body_data_source": data_source,
        "status": "przetworzono",
    }

    return web.json_response(response_data, status=200)


app = web.Application()
app.router.add_post("/api/demo/{id}", handle_data_demo)


if __name__ == "__main__":
    web.run_app(app, port=8080)
```

Test przykładowego endpointu:

```text
POST http://127.0.0.1:8080/api/demo/101?kategoria=testy
```

Body JSON:

```json
{
  "source": "Jestem z JSONa"
}
```

## 7. Podstawy asynchronicznego SQLAlchemy

SQLAlchemy znacie już jako ORM. Domyślnie może działać synchronicznie, co oznacza, że zapytania do bazy blokują aplikację na czas oczekiwania.

W świecie `asyncio` używamy asynchronicznego trybu SQLAlchemy.

> [!definition]
>
> Asynchroniczne SQLAlchemy to tryb pracy ORM, który pozwala wykonywać zapytania do bazy danych w sposób nieblokujący. Wymaga użycia asynchronicznego drivera do bazy danych.

Instalacja dla PostgreSQL:

```bash
pip install "sqlalchemy[asyncio]" asyncpg
```

Jeśli używasz MySQL albo SQLite, potrzebne będą inne sterowniki, na przykład `aiomysql` albo `aiosqlite`.

Kluczowe różnice:

1. Zamiast `create_engine` używamy `create_async_engine`.
2. String połączeniowy musi wskazywać asynchroniczny sterownik, na przykład `postgresql+asyncpg://...`.
3. Używamy `async_sessionmaker` i `AsyncSession`.
4. Operacje I/O na sesji, takie jak `commit`, `execute`, `flush`, `close`, muszą być wywoływane z `await`.
5. Zamiast `with session` używamy `async with session`.

<p style="color:red"><strong>Komentarz mentora:</strong> Jeśli przypadkiem użyjesz zwykłego synchronicznego drivera, na przykład `postgresql+psycopg2`, kod może wyglądać podobnie, ale nie będzie działał jak prawdziwie asynchroniczny dostęp do bazy.</p>

## 8. Integracja SQLAlchemy Async z Aiohttp

Przykład API dla modelu `User` z operacjami:

- `POST /users` - tworzenie użytkownika,
- `GET /users` - pobieranie listy użytkowników.

```python
import os

from aiohttp import web
from sqlalchemy import Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


DB_URL = os.environ.get(
    "DB_URL",
    "postgresql+asyncpg://postgres:postgres@localhost/aio_test_db",
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
```

Startup i cleanup bazy:

```python
async def init_db(app: web.Application):
    print(f"Inicjalizuję połączenie z bazą danych: {DB_URL}")

    engine = create_async_engine(DB_URL, echo=True)
    async_session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app["db_engine"] = engine
    app["db_session_factory"] = async_session_factory

    print("Połączenie z bazą danych gotowe.")


async def close_db(app: web.Application):
    print("Zamykam pulę połączeń z bazą danych.")
    await app["db_engine"].dispose()
```

<p style="color:red"><strong>Komentarz mentora:</strong> W materiale cleanup był pokazany jako uproszczony. W prawdziwej aplikacji warto jawnie przechować `engine` w `app` i zamknąć go przez `await engine.dispose()`.</p>

Handler `POST /users`:

```python
async def create_user(request: web.Request):
    try:
        data = await request.json()
        username = data["username"]
        email = data["email"]
    except Exception:
        raise web.HTTPBadRequest(text="Oczekiwano JSON z 'username' i 'email'")

    session_factory: async_sessionmaker[AsyncSession] = request.app["db_session_factory"]

    async with session_factory() as session:
        async with session.begin():
            stmt_exists = select(User).where(User.username == username)
            existing_user = await session.execute(stmt_exists)

            if existing_user.scalar_one_or_none() is not None:
                raise web.HTTPConflict(text=f"Użytkownik {username} już istnieje")

            new_user = User(username=username, email=email)
            session.add(new_user)

            await session.flush()
            user_data = new_user.to_dict()

    return web.json_response(user_data, status=201)
```

Handler `GET /users`:

```python
async def get_users(request: web.Request):
    session_factory: async_sessionmaker[AsyncSession] = request.app["db_session_factory"]

    async with session_factory() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
        users_data = [user.to_dict() for user in users]

    return web.json_response(users_data)
```

Tworzenie aplikacji:

```python
def create_app():
    app = web.Application()

    app.router.add_post("/users", create_user)
    app.router.add_get("/users", get_users)

    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)

    return app


if __name__ == "__main__":
    app = create_app()
    print("Start serwera na http://127.0.0.1:8080")
    print(f"Upewnij się, że baza danych na {DB_URL} działa i jest utworzona.")
    web.run_app(app, port=8080)
```

## 9. Podsumowanie

W tej lekcji ćwiczymy:

- asynchroniczne zadania I/O-bound,
- `asyncio.gather`,
- budowę serwera w `aiohttp`,
- handlery `async def`,
- routing w `aiohttp`,
- odczyt parametrów z URL, query params i JSON body,
- asynchroniczny dostęp do bazy przez SQLAlchemy,
- `create_async_engine`,
- `async_sessionmaker`,
- `AsyncSession`,
- startup i cleanup zasobów aplikacji.
