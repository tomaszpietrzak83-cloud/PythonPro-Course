# Zadanie 19 — Projekt: Mini Blog

## Zanim przeczytasz kod

Dodamy Annę i Jana. Anna utworzy post. Jan spróbuje go edytować, potem doda komentarz. Odczyt pobierze post z komentarzami; zadanie w tle zapisze powiadomienie.

Edycja Jana da 403, edycja Anny 200. Komentarz trafi do zagnieżdżonej odpowiedzi i email.log. Końcowe DELETE i GET potwierdzą usunięcie. Klucze są wyłącznie demonstracyjne.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from demo_support import database_lifespan
```

Import udostępnia nazwy: database_lifespan. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
from fastapi import FastAPI, Request
```

Import udostępnia nazwy: FastAPI, Request. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 3–3

```python
from fastapi.responses import JSONResponse
```

Import udostępnia nazwy: JSONResponse. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
from models import Base
```

Import udostępnia nazwy: Base. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 5–5

```python
from routers import posts, users
```

Import udostępnia nazwy: posts, users. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 6–6

```python
from sqlalchemy.exc import IntegrityError
```

Import udostępnia nazwy: IntegrityError. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 8–8

```python
app = FastAPI(lifespan=database_lifespan(Base), title="Mini Blog API")
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację. Pomocnik tworzy osobny schemat PostgreSQL, tabele i fabrykę sesji; po pokazie zamyka je i usuwa schemat.

### main.py: 9–9

```python
app.include_router(users.router)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Rejestruje trasy osobnego routera w aplikacji. Funkcje endpointów nie są jeszcze wywoływane.

### main.py: 10–10

```python
app.include_router(posts.router)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Rejestruje trasy osobnego routera w aplikacji. Funkcje endpointów nie są jeszcze wywoływane.

### main.py: 13–13

```python
@app.exception_handler(IntegrityError)
```

Rejestrujemy zamianę wskazanego wyjątku na czytelną odpowiedź HTTP zamiast nieobsłużonego błędu serwera.

### main.py: 14–14

```python
async def conflict(request: Request, error: IntegrityError):
```

Definiujemy korutynę. Zamienia konflikt ograniczeń bazy, np. powtórzoną nazwę, na odpowiedź 409. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 15–15

```python
    return JSONResponse({"detail": "Conflicting data"}, status_code=409)
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Tworzy odpowiedź JSON z jawnie ustawionym statusem, np. 409 przy konflikcie.

### auth.py: 1–1

```python
from typing import Annotated
```

Import udostępnia nazwy: Annotated. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### auth.py: 3–3

```python
from fastapi import Header, HTTPException, Request
```

Import udostępnia nazwy: Header, HTTPException, Request. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### auth.py: 4–4

```python
from models import User
```

Import udostępnia nazwy: User. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### auth.py: 6–6

```python
DEMO_KEYS = {"demo-anna-key": 1, "demo-jan-key": 2}
```

Obliczamy prawą stronę i przypisujemy wynik do `DEMO_KEYS`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### auth.py: 9–11

```python
async def get_actor(
    request: Request, x_api_key: Annotated[str | None, Header()] = None
):
```

Definiujemy korutynę. Rozpoznaje użytkownika przez jawny klucz demonstracyjny i osobną sesję odczytu. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Pobiera nagłówek HTTP; x_api_key odpowiada nazwie X-API-Key.

### auth.py: 12–12

```python
    user_id = DEMO_KEYS.get(x_api_key)
```

Obliczamy prawą stronę i przypisujemy wynik do `user_id`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### auth.py: 13–13

```python
    if user_id is None:
```

Sprawdzamy warunek `user_id is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### auth.py: 14–14

```python
        raise HTTPException(401, "Use a demonstration API key")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### auth.py: 15–15

```python
    async with request.app.state.sessions() as session:
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. 

### auth.py: 16–16

```python
        user = await session.get(User, user_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `user`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### auth.py: 17–17

```python
        if user is None:
```

Sprawdzamy warunek `user is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### auth.py: 18–18

```python
            raise HTTPException(401, "Demo user does not exist")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### auth.py: 19–19

```python
        return user.id
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### models.py: 1–1

```python
from sqlalchemy import ForeignKey, String
```

Import udostępnia nazwy: ForeignKey, String. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### models.py: 2–2

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
```

Import udostępnia nazwy: DeclarativeBase, Mapped, mapped_column, relationship. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### models.py: 5–5

```python
class Base(DeclarativeBase):
```

Klasa Base dziedziczy po DeclarativeBase. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### models.py: 6–6

```python
    pass
```

pass to pusta instrukcja wymagana jako ciało klasy Base. Rejestr modeli i metadata pochodzą z klasy bazowej.

### models.py: 9–9

```python
class User(Base):
```

Klasa User dziedziczy po Base. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### models.py: 10–10

```python
    __tablename__ = "users"
```

Obliczamy prawą stronę i przypisujemy wynik do `__tablename__`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### models.py: 11–11

```python
    id: Mapped[int] = mapped_column(primary_key=True)
```

Pole `id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny.

### models.py: 12–12

```python
    name: Mapped[str] = mapped_column(String(50), unique=True)
```

Pole `name` ma deklarowany typ `Mapped[str]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Określa typ tekstowej kolumny i maksymalną długość w bazie.

### models.py: 15–15

```python
class Post(Base):
```

Klasa Post dziedziczy po Base. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### models.py: 16–16

```python
    __tablename__ = "posts"
```

Obliczamy prawą stronę i przypisujemy wynik do `__tablename__`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### models.py: 17–17

```python
    id: Mapped[int] = mapped_column(primary_key=True)
```

Pole `id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny.

### models.py: 18–18

```python
    title: Mapped[str] = mapped_column(String(100))
```

Pole `title` ma deklarowany typ `Mapped[str]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Określa typ tekstowej kolumny i maksymalną długość w bazie.

### models.py: 19–19

```python
    body: Mapped[str] = mapped_column(String(5000))
```

Pole `body` ma deklarowany typ `Mapped[str]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Określa typ tekstowej kolumny i maksymalną długość w bazie.

### models.py: 20–22

```python
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
```

Pole `user_id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Łączy kolumnę z kluczem innej tabeli; ondelete=CASCADE usuwa zależne rekordy w bazie.

### models.py: 23–25

```python
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post", passive_deletes=True
    )
```

Pole `comments` ma deklarowany typ `Mapped[list['Comment']]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje powiązanie obiektów ORM; back_populates wskazuje drugą stronę relacji.

### models.py: 28–28

```python
class Comment(Base):
```

Klasa Comment dziedziczy po Base. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### models.py: 29–29

```python
    __tablename__ = "comments"
```

Obliczamy prawą stronę i przypisujemy wynik do `__tablename__`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### models.py: 30–30

```python
    id: Mapped[int] = mapped_column(primary_key=True)
```

Pole `id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny.

### models.py: 31–31

```python
    body: Mapped[str] = mapped_column(String(1000))
```

Pole `body` ma deklarowany typ `Mapped[str]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Określa typ tekstowej kolumny i maksymalną długość w bazie.

### models.py: 32–34

```python
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
```

Pole `user_id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Łączy kolumnę z kluczem innej tabeli; ondelete=CASCADE usuwa zależne rekordy w bazie.

### models.py: 35–37

```python
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE")
    )
```

Pole `post_id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Łączy kolumnę z kluczem innej tabeli; ondelete=CASCADE usuwa zależne rekordy w bazie.

### models.py: 38–38

```python
    post: Mapped[Post] = relationship(back_populates="comments")
```

Pole `post` ma deklarowany typ `Mapped[Post]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje powiązanie obiektów ORM; back_populates wskazuje drugą stronę relacji.

### routers/posts.py: 1–1

```python
from auth import get_actor
```

Import udostępnia nazwy: get_actor. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/posts.py: 2–2

```python
from demo_support import get_db, runtime_file
```

Import udostępnia nazwy: get_db, runtime_file. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/posts.py: 3–3

```python
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response
```

Import udostępnia nazwy: APIRouter, BackgroundTasks, Depends, HTTPException, Response. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/posts.py: 4–4

```python
from lab_support import event
```

Import udostępnia nazwy: event. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/posts.py: 5–5

```python
from models import Comment, Post
```

Import udostępnia nazwy: Comment, Post. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/posts.py: 6–6

```python
from schemas import CommentCreate, PostCreate
```

Import udostępnia nazwy: CommentCreate, PostCreate. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/posts.py: 7–7

```python
from sqlalchemy import select
```

Import udostępnia nazwy: select. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/posts.py: 8–8

```python
from sqlalchemy.ext.asyncio import AsyncSession
```

Import udostępnia nazwy: AsyncSession. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/posts.py: 9–9

```python
from sqlalchemy.orm import selectinload
```

Import udostępnia nazwy: selectinload. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/posts.py: 11–11

```python
router = APIRouter(prefix="/posts", tags=["posts"])
```

Obliczamy prawą stronę i przypisujemy wynik do `router`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy grupę tras ze wspólnym prefiksem i tagiem.

### routers/posts.py: 14–14

```python
def post_data(post):
```

Definiujemy zwykłą funkcję. Zamienia obiekt Post na zwykły słownik gotowy do JSON. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### routers/posts.py: 15–20

```python
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "user_id": post.user_id,
    }
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/posts.py: 23–23

```python
def notify_author(post_id):
```

Definiujemy zwykłą funkcję. Zapisuje lokalny ślad powiadomienia zamiast wysyłać prawdziwy email. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### routers/posts.py: 24–24

```python
    with runtime_file("email.log").open("a", encoding="utf-8") as stream:
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera plik; tryb a dopisuje dane. with dopilnuje zamknięcia uchwytu. Zwraca ścieżkę w osobnym katalogu danych tego pokazu. Nie zapisujemy w plikach kursu ani w danych innych lekcji.

### routers/posts.py: 25–25

```python
        stream.write(f"New comment on post {post_id}; email simulated\n")
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Zapisuje tekst do otwartego pliku; \n oddziela wpisy dziennika.

### routers/posts.py: 26–26

```python
    event("log", "background", "Author notification recorded")
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Zapisuje rzeczywiste zdarzenie widoczne w panelu pokazu; nie zmienia danych biznesowych.

### routers/posts.py: 29–29

```python
@router.post("", status_code=201)
```

Dekorator `router.post('', status_code=201)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/posts.py: 30–34

```python
async def create_post(
    data: PostCreate,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
```

Definiujemy korutynę. Przypisuje nowy post do użytkownika ustalonego przez dependency. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/posts.py: 35–35

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### routers/posts.py: 36–36

```python
        post = Post(**data.model_dump(), user_id=actor)
```

Obliczamy prawą stronę i przypisujemy wynik do `post`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zamienia zwalidowany model Pydantic na słownik. ** rozpakowuje jego klucze jako argumenty lub pola nowego słownika.

### routers/posts.py: 37–37

```python
        db.add(post)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Dołącza obiekt ORM do sesji. Nie wykonuje jeszcze INSERT i nie potrzebuje await.

### routers/posts.py: 38–38

```python
        await db.flush()
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Wysyła oczekujące INSERT/UPDATE i pobiera wygenerowane ID. To jeszcze nie commit; wyjątek nadal może wycofać zapis.

### routers/posts.py: 39–39

```python
    return post_data(post)
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/posts.py: 42–42

```python
@router.get("")
```

Dekorator `router.get('')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/posts.py: 43–43

```python
async def list_posts(db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Odczytuje posty w stabilnej kolejności ID. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/posts.py: 44–44

```python
    posts = (await db.execute(select(Post).order_by(Post.id))).scalars().all()
```

Obliczamy prawą stronę i przypisujemy wynik do `posts`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zbiera dostępne elementy wyniku do listy. Wyciąga obiekty modelu z wierszy wyniku SELECT. Wysyła zapytanie do bazy; await czeka na wynik, oddając sterowanie pętli zdarzeń. Ustala kolejność; dodatkowe ID rozstrzyga remisy przy sortowaniu i paginacji. Buduje opis SELECT, jeszcze bez komunikacji z bazą.

### routers/posts.py: 45–45

```python
    return [post_data(post) for post in posts]
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/posts.py: 48–48

```python
@router.get("/{post_id}")
```

Dekorator `router.get('/{post_id}')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/posts.py: 49–49

```python
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Odczytuje post po ID lub zwraca 404. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/posts.py: 50–50

```python
    post = await db.get(Post, post_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `post`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### routers/posts.py: 51–51

```python
    if post is None:
```

Sprawdzamy warunek `post is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### routers/posts.py: 52–52

```python
        raise HTTPException(404, "Post not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/posts.py: 53–53

```python
    return post_data(post)
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/posts.py: 56–56

```python
@router.put("/{post_id}")
```

Dekorator `router.put('/{post_id}')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/posts.py: 57–62

```python
async def replace_post(
    post_id: int,
    data: PostCreate,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
```

Definiujemy korutynę. Przed zmianą posta porównuje ID autora z ID rozpoznanego użytkownika. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/posts.py: 63–63

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### routers/posts.py: 64–64

```python
        post = await db.get(Post, post_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `post`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### routers/posts.py: 65–65

```python
        if post is None:
```

Sprawdzamy warunek `post is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### routers/posts.py: 66–66

```python
            raise HTTPException(404, "Post not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/posts.py: 67–67

```python
        if post.user_id != actor:
```

Sprawdzamy warunek `post.user_id != actor`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### routers/posts.py: 68–68

```python
            raise HTTPException(403, "Only the author may edit")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/posts.py: 69–69

```python
        post.title = data.title
```

Obliczamy prawą stronę i przypisujemy wynik do `post.title`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### routers/posts.py: 70–70

```python
        post.body = data.body
```

Obliczamy prawą stronę i przypisujemy wynik do `post.body`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### routers/posts.py: 71–71

```python
    return post_data(post)
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/posts.py: 74–74

```python
@router.delete("/{post_id}", status_code=204)
```

Dekorator `router.delete('/{post_id}', status_code=204)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/posts.py: 75–79

```python
async def delete_post(
    post_id: int,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
```

Definiujemy korutynę. Usuwa post wyłącznie na żądanie jego autora. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/posts.py: 80–80

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### routers/posts.py: 81–81

```python
        post = await db.get(Post, post_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `post`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### routers/posts.py: 82–82

```python
        if post is None:
```

Sprawdzamy warunek `post is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### routers/posts.py: 83–83

```python
            raise HTTPException(404, "Post not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/posts.py: 84–84

```python
        if post.user_id != actor:
```

Sprawdzamy warunek `post.user_id != actor`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### routers/posts.py: 85–85

```python
            raise HTTPException(403, "Only the author may delete")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/posts.py: 86–86

```python
        await db.delete(post)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Oznacza obiekt ORM do usunięcia; transakcja zatwierdzi DELETE przy poprawnym wyjściu.

### routers/posts.py: 87–87

```python
    return Response(status_code=204)
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Tworzy odpowiedź HTTP. Przy 204 body musi pozostać puste.

### routers/posts.py: 90–90

```python
@router.post("/{post_id}/comments", status_code=201)
```

Dekorator `router.post('/{post_id}/comments', status_code=201)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/posts.py: 91–97

```python
async def add_comment(
    post_id: int,
    data: CommentCreate,
    background_tasks: BackgroundTasks,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
```

Definiujemy korutynę. Zapisuje komentarz, następnie planuje powiadomienie i ewentualną analizę w tle. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/posts.py: 98–98

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### routers/posts.py: 99–99

```python
        if await db.get(Post, post_id) is None:
```

Sprawdzamy warunek `await db.get(Post, post_id) is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### routers/posts.py: 100–100

```python
            raise HTTPException(404, "Post not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/posts.py: 101–101

```python
        comment = Comment(body=data.body, post_id=post_id, user_id=actor)
```

Obliczamy prawą stronę i przypisujemy wynik do `comment`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### routers/posts.py: 102–102

```python
        db.add(comment)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Dołącza obiekt ORM do sesji. Nie wykonuje jeszcze INSERT i nie potrzebuje await.

### routers/posts.py: 103–103

```python
        await db.flush()
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Wysyła oczekujące INSERT/UPDATE i pobiera wygenerowane ID. To jeszcze nie commit; wyjątek nadal może wycofać zapis.

### routers/posts.py: 104–104

```python
    background_tasks.add_task(notify_author, post_id)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Planuje wykonanie funkcji po wysłaniu odpowiedzi. Przekazujemy funkcję bez (), a dalej jej argumenty.

### routers/posts.py: 105–105

```python
    return {"id": comment.id, "body": comment.body}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/posts.py: 108–108

```python
@router.get("/{post_id}/with-comments")
```

Dekorator `router.get('/{post_id}/with-comments')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/posts.py: 109–109

```python
async def post_with_comments(post_id: int, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Pobiera post wraz z komentarzami przez selectinload i zwraca zagnieżdżony JSON. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/posts.py: 110–114

```python
    statement = (
        select(Post)
        .options(selectinload(Post.comments))
        .where(Post.id == post_id)
    )
```

Obliczamy prawą stronę i przypisujemy wynik do `statement`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Dodaje warunek SQL. Wartości są przekazywane jako parametry, bez składania SQL z wejścia klienta. Buduje opis SELECT, jeszcze bez komunikacji z bazą. Pobiera relację osobnym zbiorczym SELECT; zapobiega leniwemu I/O przy późniejszym czytaniu kolekcji.

### routers/posts.py: 115–115

```python
    post = (await db.execute(statement)).scalar_one_or_none()
```

Obliczamy prawą stronę i przypisujemy wynik do `post`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zwraca jeden obiekt albo None. Więcej niż jeden wynik jest błędem. Wysyła zapytanie do bazy; await czeka na wynik, oddając sterowanie pętli zdarzeń.

### routers/posts.py: 116–116

```python
    if post is None:
```

Sprawdzamy warunek `post is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### routers/posts.py: 117–117

```python
        raise HTTPException(404, "Post not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/posts.py: 118–121

```python
    return {
        **post_data(post),
        "comments": [{"id": c.id, "body": c.body} for c in post.comments],
    }
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/users.py: 1–1

```python
from auth import get_actor
```

Import udostępnia nazwy: get_actor. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/users.py: 2–2

```python
from demo_support import get_db
```

Import udostępnia nazwy: get_db. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/users.py: 3–3

```python
from fastapi import APIRouter, Depends, HTTPException, Response
```

Import udostępnia nazwy: APIRouter, Depends, HTTPException, Response. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/users.py: 4–4

```python
from models import User
```

Import udostępnia nazwy: User. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/users.py: 5–5

```python
from schemas import UserCreate
```

Import udostępnia nazwy: UserCreate. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/users.py: 6–6

```python
from sqlalchemy import select
```

Import udostępnia nazwy: select. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/users.py: 7–7

```python
from sqlalchemy.ext.asyncio import AsyncSession
```

Import udostępnia nazwy: AsyncSession. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### routers/users.py: 9–9

```python
router = APIRouter(prefix="/users", tags=["users"])
```

Obliczamy prawą stronę i przypisujemy wynik do `router`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy grupę tras ze wspólnym prefiksem i tagiem.

### routers/users.py: 12–12

```python
@router.post("", status_code=201)
```

Dekorator `router.post('', status_code=201)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/users.py: 13–13

```python
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Otrzymuje model użytkownika zwalidowany przez Pydantic. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/users.py: 14–14

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### routers/users.py: 15–15

```python
        user = User(**data.model_dump())
```

Obliczamy prawą stronę i przypisujemy wynik do `user`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zamienia zwalidowany model Pydantic na słownik. ** rozpakowuje jego klucze jako argumenty lub pola nowego słownika.

### routers/users.py: 16–16

```python
        db.add(user)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Dołącza obiekt ORM do sesji. Nie wykonuje jeszcze INSERT i nie potrzebuje await.

### routers/users.py: 17–17

```python
        await db.flush()
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Wysyła oczekujące INSERT/UPDATE i pobiera wygenerowane ID. To jeszcze nie commit; wyjątek nadal może wycofać zapis.

### routers/users.py: 18–18

```python
    return {"id": user.id, "name": user.name}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/users.py: 21–21

```python
@router.get("")
```

Dekorator `router.get('')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/users.py: 22–22

```python
async def list_users(db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Odczytuje użytkowników i przygotowuje ich publiczne ID oraz nazwy. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/users.py: 23–23

```python
    users = (await db.execute(select(User).order_by(User.id))).scalars().all()
```

Obliczamy prawą stronę i przypisujemy wynik do `users`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zbiera dostępne elementy wyniku do listy. Wyciąga obiekty modelu z wierszy wyniku SELECT. Wysyła zapytanie do bazy; await czeka na wynik, oddając sterowanie pętli zdarzeń. Ustala kolejność; dodatkowe ID rozstrzyga remisy przy sortowaniu i paginacji. Buduje opis SELECT, jeszcze bez komunikacji z bazą.

### routers/users.py: 24–24

```python
    return [{"id": user.id, "name": user.name} for user in users]
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/users.py: 27–27

```python
@router.get("/{user_id}")
```

Dekorator `router.get('/{user_id}')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/users.py: 28–28

```python
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Odczytuje jednego użytkownika albo zwraca 404. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/users.py: 29–29

```python
    user = await db.get(User, user_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `user`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### routers/users.py: 30–30

```python
    if user is None:
```

Sprawdzamy warunek `user is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### routers/users.py: 31–31

```python
        raise HTTPException(404, "User not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/users.py: 32–32

```python
    return {"id": user.id, "name": user.name}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/users.py: 35–35

```python
@router.put("/{user_id}")
```

Dekorator `router.put('/{user_id}')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/users.py: 36–41

```python
async def replace_user(
    user_id: int,
    data: UserCreate,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
```

Definiujemy korutynę. Sprawdza właściciela konta i zapisuje nową nazwę użytkownika. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/users.py: 42–42

```python
    if actor != user_id:
```

Sprawdzamy warunek `actor != user_id`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### routers/users.py: 43–43

```python
        raise HTTPException(403, "Only the account owner may edit")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/users.py: 44–44

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### routers/users.py: 45–45

```python
        user = await db.get(User, user_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `user`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### routers/users.py: 46–46

```python
        user.name = data.name
```

Obliczamy prawą stronę i przypisujemy wynik do `user.name`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### routers/users.py: 47–47

```python
    return {"id": user.id, "name": user.name}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### routers/users.py: 50–50

```python
@router.delete("/{user_id}", status_code=204)
```

Dekorator `router.delete('/{user_id}', status_code=204)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### routers/users.py: 51–55

```python
async def delete_user(
    user_id: int,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
```

Definiujemy korutynę. Sprawdza właściciela i usuwa konto; klucze obce obsługują usuwanie zależnych danych. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### routers/users.py: 56–56

```python
    if actor != user_id:
```

Sprawdzamy warunek `actor != user_id`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### routers/users.py: 57–57

```python
        raise HTTPException(403, "Only the account owner may delete")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### routers/users.py: 58–58

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### routers/users.py: 59–59

```python
        user = await db.get(User, user_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `user`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### routers/users.py: 60–60

```python
        await db.delete(user)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Oznacza obiekt ORM do usunięcia; transakcja zatwierdzi DELETE przy poprawnym wyjściu.

### routers/users.py: 61–61

```python
    return Response(status_code=204)
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Tworzy odpowiedź HTTP. Przy 204 body musi pozostać puste.

### schemas.py: 1–1

```python
from pydantic import BaseModel, Field
```

Import udostępnia nazwy: BaseModel, Field. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### schemas.py: 4–4

```python
class UserCreate(BaseModel):
```

Klasa UserCreate dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### schemas.py: 5–5

```python
    name: str = Field(min_length=2, max_length=50)
```

Pole `name` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### schemas.py: 8–8

```python
class PostCreate(BaseModel):
```

Klasa PostCreate dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### schemas.py: 9–9

```python
    title: str = Field(min_length=1, max_length=100)
```

Pole `title` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### schemas.py: 10–10

```python
    body: str = Field(min_length=1, max_length=5000)
```

Pole `body` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### schemas.py: 13–13

```python
class CommentCreate(BaseModel):
```

Klasa CommentCreate dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### schemas.py: 14–14

```python
    body: str = Field(min_length=1, max_length=1000)
```

Pole `body` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.
