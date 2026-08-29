# Lekcja 33: FastAPI - Nowoczesny Framework dla Asynchronicznych API

`#lekcja` `#python` `#fastapi` `#async` `#api` `#rest` `#pydantic`

W poprzedniej lekcji poznaliśmy `aiohttp`, czyli niskopoziomowy framework do budowania aplikacji asynchronicznych.

FastAPI idzie krok dalej. Daje gotowy, nowoczesny sposób tworzenia API REST, który łączy:

- asynchroniczność,
- typowanie Pythona,
- walidację danych,
- automatyczną dokumentację,
- prostą strukturę kodu.

## 1. Czym jest FastAPI?

FastAPI to framework webowy do budowania API w Pythonie.

Jest oparty o:

- `Starlette` - obsługa HTTP, routing, middleware, async,
- `Pydantic` - walidacja danych i modele,
- standardowe type hints Pythona.

FastAPI dobrze sprawdza się w projektach, w których aplikacja ma udostępniać endpointy dla frontendu, aplikacji mobilnej, innego backendu albo integracji z AI.

## 2. Dlaczego FastAPI?

Najważniejsze zalety:

- wysoka wydajność dzięki ASGI i `async`,
- prosta składnia,
- walidacja danych na podstawie typów,
- automatyczna dokumentacja Swagger UI i ReDoc,
- dobra współpraca z bazami danych,
- czytelna struktura dla większych projektów.

W praktyce FastAPI pozwala pisać mniej kodu technicznego, bo wiele rzeczy powstaje automatycznie na podstawie sygnatur funkcji i modeli Pydantic.

## 3. Pierwsze API

Instalacja:

```bash
pip install fastapi uvicorn[standard]
```

Przykład pliku `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Uruchomienie:

```bash
uvicorn main:app --reload
```

Po uruchomieniu aplikacja jest dostępna domyślnie pod adresem:

```text
http://127.0.0.1:8000
```

Automatyczna dokumentacja:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

## 4. Dokumentacja API

FastAPI generuje dokumentację automatycznie.

Możemy dodać metadane aplikacji:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Moje API",
    description="Przykładowe API stworzone w FastAPI",
    version="1.0.0",
)
```

Endpointy można opisywać tagami i docstringami:

```python
@app.get("/users", tags=["users"])
async def get_users():
    """
    Zwraca listę użytkowników.
    """
    return [{"id": 1, "name": "Anna"}]
```

FastAPI wykorzystuje te informacje w `/docs`.

## 5. Path params i query params

Parametry ścieżki są częścią adresu URL:

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

FastAPI automatycznie:

- odczyta `user_id` z URL,
- przekonwertuje go na `int`,
- zwróci błąd walidacji, jeśli wartość nie pasuje.

Parametry query są przekazywane po znaku `?`:

```python
from typing import Optional
from fastapi import Query


@app.get("/search")
async def search(q: Optional[str] = None, limit: int = Query(default=10, ge=1, le=100)):
    return {
        "q": q,
        "limit": limit,
    }
```

Przykładowy adres:

```text
/search?q=python&limit=5
```

## 6. Routing i metody HTTP

FastAPI używa dekoratorów odpowiadających metodom HTTP:

- `@app.get()` - pobieranie danych,
- `@app.post()` - tworzenie danych,
- `@app.put()` - pełna aktualizacja,
- `@app.patch()` - częściowa aktualizacja,
- `@app.delete()` - usuwanie danych.

Prosty przykład CRUD w pamięci:

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

users_db = {
    1: {"id": 1, "name": "Anna"},
    2: {"id": 2, "name": "Jan"},
}


@app.get("/users")
async def list_users():
    return list(users_db.values())


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: dict):
    new_id = max(users_db.keys()) + 1
    users_db[new_id] = {"id": new_id, **user}
    return users_db[new_id]


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
```

## 7. APIRouter

W większej aplikacji nie trzymamy wszystkich endpointów w jednym pliku.

Przykładowa struktura:

```text
project/
    main.py
    routers/
        users.py
        products.py
```

Plik `routers/users.py`:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Anna"}]
```

Plik `main.py`:

```python
from fastapi import FastAPI
from routers import users

app = FastAPI()

app.include_router(users.router)
```

`APIRouter` pomaga dzielić kod według obszarów aplikacji.

## 8. Dependency Injection

Dependency Injection pozwala wydzielić wspólną logikę, która ma być wykonana przed endpointem.

Przykład sprawdzania tokena:

```python
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return x_token


@app.get("/protected")
async def protected_route(token: str = Depends(verify_token)):
    return {"message": "Access granted"}
```

Dependency może też zwracać wspólne parametry:

```python
async def common_pagination_params(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/items")
async def list_items(pagination: dict = Depends(common_pagination_params)):
    return pagination
```

## 9. Pydantic i walidacja danych

Pydantic służy do definiowania modeli danych.

Przykład:

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str
    age: int = Field(..., ge=0, le=120)
```

FastAPI używa modeli Pydantic do:

- walidacji danych wejściowych,
- generowania dokumentacji,
- opisywania danych wyjściowych przez `response_model`.

Przykład z modelem odpowiedzi:

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    return {"id": 1, **user.model_dump()}
```

Model aktualizacji może mieć pola opcjonalne:

```python
from typing import Optional
from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


@app.patch("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate):
    data = user_update.model_dump(exclude_unset=True)
    return {"id": user_id, **data}
```

## 10. Modele zagnieżdżone

Modele Pydantic mogą zawierać inne modele.

```python
from pydantic import BaseModel, Field


class Address(BaseModel):
    street: str
    city: str
    postal_code: str = Field(..., pattern=r"^\d{2}-\d{3}$")


class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class UserWithAddress(BaseModel):
    name: str
    address: Address
    orders: list[OrderItem] = []
```

## 11. Walidatory

Materiał pokazuje walidatory w stylu Pydantic v1:

```python
from pydantic import BaseModel, Field, root_validator, validator


class Product(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    category: str
    tags: list[str] = []

    @validator("name")
    def validate_name(cls, value):
        if len(value.strip()) < 2:
            raise ValueError("Name is too short")
        return value.strip().title()

    @validator("category")
    def validate_category(cls, value):
        allowed = ["Electronics", "Books", "Clothing"]
        if value not in allowed:
            raise ValueError("Invalid category")
        return value

    @root_validator
    def validate_product(cls, values):
        price = values.get("price")
        category = values.get("category")
        if category == "Electronics" and price < 10:
            raise ValueError("Electronics must cost at least 10")
        return values
```

<p style="color:red"><strong>Komentarz mentora:</strong> To jest styl Pydantic v1. W nowych projektach z Pydantic v2 lepiej używać `@field_validator` i `@model_validator`. Sama idea walidacji zostaje taka sama: model pilnuje poprawności danych.</p>

## 12. FastAPI i baza danych

FastAPI często łączy się z SQLAlchemy.

W wersji asynchronicznej używamy między innymi:

- `create_async_engine`,
- `AsyncSession`,
- `sessionmaker`,
- dependency `get_db`.

Przykładowy plik `database.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

Przykładowy model ORM:

```python
from sqlalchemy import Column, Integer, String

from database import Base


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
```

Schemat Pydantic:

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
```

Endpoint korzystający z sesji bazy:

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = UserORM(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

Ważne zasady:

- oddzielaj modele ORM od schematów Pydantic,
- używaj dependency do sesji bazy,
- przy relacjach unikaj problemu N+1 przez `selectinload()` albo `joinedload()`.

## 13. Middleware

Middleware to kod wykonywany przed i po obsłudze requestu.

Przykład logowania czasu:

```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    return response
```

Przykłady użycia middleware:

- logowanie requestów,
- dodawanie nagłówków,
- sprawdzanie klucza API,
- obsługa CORS.

CORS:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 14. BackgroundTasks

`BackgroundTasks` pozwala uruchomić zadanie po odesłaniu odpowiedzi HTTP.

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def send_email_notification(email: str, message: str):
    print(f"Sending email to {email}: {message}")


@app.post("/users/{user_id}/welcome")
async def send_welcome_email(user_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        send_email_notification,
        "user@example.com",
        "Welcome!",
    )
    return {"message": "Email will be sent in background"}
```

To dobre miejsce na lekkie zadania, na przykład zapis logu albo prostą notyfikację.

<p style="color:red"><strong>Komentarz mentora:</strong> `BackgroundTasks` nie zastępuje kolejki zadań. Dla krytycznych i długich operacji lepiej użyć Celery, RQ albo innego systemu kolejek.</p>

## 15. Event hooks

Materiał pokazuje start i stop aplikacji przez `on_event`:

```python
@app.on_event("startup")
async def startup_event():
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutdown")
```

<p style="color:red"><strong>Komentarz mentora:</strong> W aktualnej dokumentacji FastAPI `on_event` jest oznaczone jako przestarzałe. W nowych projektach zalecany jest mechanizm `lifespan`. W starszych przykładach i materiałach nadal często zobaczysz `on_event`.</p>

## 16. Mini Blog API

W materiale pojawia się projekt mini Blog API.

Przykładowa struktura:

```text
blog_api/
    main.py
    database.py
    models.py
    schemas.py
    routers/
        users.py
        posts.py
        comments.py
```

Projekt łączy:

- modele ORM,
- schematy Pydantic,
- `APIRouter`,
- middleware,
- event hooks,
- dependency injection,
- relacje między użytkownikami, postami i komentarzami.

To dobry przykład większej struktury aplikacji FastAPI.

## 17. FastAPI i AI

FastAPI często służy jako warstwa API dla modeli AI.

Przykładowe zastosowania:

- chatbot jako endpoint HTTP,
- generowanie podsumowań,
- moderacja treści,
- analiza sentymentu,
- rekomendacje w tle.

Materiał pokazuje starszy styl użycia OpenAI:

```python
response = await openai.ChatCompletion.acreate(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Napisz podsumowanie tekstu"}
    ],
)
```

<p style="color:red"><strong>Komentarz mentora:</strong> To jest starszy styl SDK OpenAI. W nowych projektach sprawdzaj aktualną dokumentację i używaj obecnego klienta oraz aktualnych endpointów. Sama architektura zostaje poprawna: FastAPI przyjmuje request, wywołuje model AI i zwraca odpowiedź.</p>

## 18. Podsumowanie

W tej lekcji najważniejsze są:

- tworzenie endpointów FastAPI,
- automatyczna dokumentacja,
- path params i query params,
- metody HTTP i status codes,
- `APIRouter`,
- Dependency Injection,
- modele i walidacja Pydantic,
- integracja z async SQLAlchemy,
- middleware,
- zadania w tle,
- start i zamknięcie aplikacji,
- budowa większego API, na przykład Blog API.

FastAPI jest dobrym wyborem, gdy chcesz szybko zbudować czytelne, walidowane i nowoczesne API w Pythonie.
