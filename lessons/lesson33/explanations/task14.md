# Zadanie 14 — Autor i wiele książek

## Zanim przeczytasz kod

Utworzymy Annę, przypiszemy jej dwie książki, potem pobierzemy /authors/1/books. Osobno sprawdzimy nieistniejącego autora.

Otrzymasz Python Basics i Async Patterns. Dla autora 99 dostaniesz 404. Relację odczytujemy przed zamknięciem sesji.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from demo_support import database_lifespan, get_db
```

Import udostępnia nazwy: database_lifespan, get_db. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
from fastapi import Depends, FastAPI, HTTPException
```

Import udostępnia nazwy: Depends, FastAPI, HTTPException. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 3–3

```python
from pydantic import BaseModel, ConfigDict, Field
```

Import udostępnia nazwy: BaseModel, ConfigDict, Field. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
from sqlalchemy import ForeignKey, String, select
```

Import udostępnia nazwy: ForeignKey, String, select. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 5–5

```python
from sqlalchemy.ext.asyncio import AsyncSession
```

Import udostępnia nazwy: AsyncSession. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 6–12

```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)
```

Import udostępnia nazwy: DeclarativeBase, Mapped, mapped_column, relationship, selectinload. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 15–15

```python
class Base(DeclarativeBase):
```

Klasa Base dziedziczy po DeclarativeBase. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 16–16

```python
    pass
```

pass to pusta instrukcja wymagana jako ciało klasy Base. Rejestr modeli i metadata pochodzą z klasy bazowej.

### main.py: 19–19

```python
class Author(Base):
```

Klasa Author dziedziczy po Base. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 20–20

```python
    __tablename__ = "authors"
```

Obliczamy prawą stronę i przypisujemy wynik do `__tablename__`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 21–21

```python
    id: Mapped[int] = mapped_column(primary_key=True)
```

Pole `id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny.

### main.py: 22–22

```python
    name: Mapped[str] = mapped_column(String(100))
```

Pole `name` ma deklarowany typ `Mapped[str]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Określa typ tekstowej kolumny i maksymalną długość w bazie.

### main.py: 23–23

```python
    books: Mapped[list["Book"]] = relationship(back_populates="author")
```

Pole `books` ma deklarowany typ `Mapped[list['Book']]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje powiązanie obiektów ORM; back_populates wskazuje drugą stronę relacji.

### main.py: 26–26

```python
class Book(Base):
```

Klasa Book dziedziczy po Base. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 27–27

```python
    __tablename__ = "books"
```

Obliczamy prawą stronę i przypisujemy wynik do `__tablename__`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 28–28

```python
    id: Mapped[int] = mapped_column(primary_key=True)
```

Pole `id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny.

### main.py: 29–29

```python
    title: Mapped[str] = mapped_column(String(100))
```

Pole `title` ma deklarowany typ `Mapped[str]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Określa typ tekstowej kolumny i maksymalną długość w bazie.

### main.py: 30–30

```python
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
```

Pole `author_id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Łączy kolumnę z kluczem innej tabeli; ondelete=CASCADE usuwa zależne rekordy w bazie.

### main.py: 31–31

```python
    author: Mapped[Author] = relationship(back_populates="books")
```

Pole `author` ma deklarowany typ `Mapped[Author]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje powiązanie obiektów ORM; back_populates wskazuje drugą stronę relacji.

### main.py: 34–34

```python
class BookRead(BaseModel):
```

Klasa BookRead dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 35–35

```python
    model_config = ConfigDict(from_attributes=True)
```

Obliczamy prawą stronę i przypisujemy wynik do `model_config`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. from_attributes=True pozwala modelowi odpowiedzi czytać atrybuty obiektu ORM.

### main.py: 36–36

```python
    id: int
```

Pole `id` ma deklarowany typ `int`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. 

### main.py: 37–37

```python
    title: str
```

Pole `title` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. 

### main.py: 40–40

```python
class AuthorCreate(BaseModel):
```

Klasa AuthorCreate dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 41–41

```python
    name: str = Field(min_length=1, max_length=100)
```

Pole `name` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 44–44

```python
class BookCreate(BaseModel):
```

Klasa BookCreate dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 45–45

```python
    title: str = Field(min_length=1, max_length=100)
```

Pole `title` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 46–46

```python
    author_id: int
```

Pole `author_id` ma deklarowany typ `int`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. 

### main.py: 49–49

```python
app = FastAPI(lifespan=database_lifespan(Base))
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację. Pomocnik tworzy osobny schemat PostgreSQL, tabele i fabrykę sesji; po pokazie zamyka je i usuwa schemat.

### main.py: 52–52

```python
@app.post("/authors", status_code=201)
```

Dekorator `app.post('/authors', status_code=201)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 53–53

```python
async def create_author(data: AuthorCreate, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Zapisuje nowego autora i odbiera ID nadane przez bazę. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 54–54

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### main.py: 55–55

```python
        author = Author(**data.model_dump())
```

Obliczamy prawą stronę i przypisujemy wynik do `author`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zamienia zwalidowany model Pydantic na słownik. ** rozpakowuje jego klucze jako argumenty lub pola nowego słownika.

### main.py: 56–56

```python
        db.add(author)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Dołącza obiekt ORM do sesji. Nie wykonuje jeszcze INSERT i nie potrzebuje await.

### main.py: 57–57

```python
        await db.flush()
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Wysyła oczekujące INSERT/UPDATE i pobiera wygenerowane ID. To jeszcze nie commit; wyjątek nadal może wycofać zapis.

### main.py: 58–58

```python
    return {"id": author.id, "name": author.name}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 61–61

```python
@app.post("/books", status_code=201)
```

Dekorator `app.post('/books', status_code=201)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 62–62

```python
async def create_book(data: BookCreate, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Otrzymuje dane książki; tworzy rekord lub odsyła zwalidowany model, zależnie od tego ćwiczenia. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 63–63

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### main.py: 64–64

```python
        if await db.get(Author, data.author_id) is None:
```

Sprawdzamy warunek `await db.get(Author, data.author_id) is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### main.py: 65–65

```python
            raise HTTPException(404, "Author not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 66–66

```python
        book = Book(**data.model_dump())
```

Obliczamy prawą stronę i przypisujemy wynik do `book`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zamienia zwalidowany model Pydantic na słownik. ** rozpakowuje jego klucze jako argumenty lub pola nowego słownika.

### main.py: 67–67

```python
        db.add(book)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Dołącza obiekt ORM do sesji. Nie wykonuje jeszcze INSERT i nie potrzebuje await.

### main.py: 68–68

```python
        await db.flush()
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Wysyła oczekujące INSERT/UPDATE i pobiera wygenerowane ID. To jeszcze nie commit; wyjątek nadal może wycofać zapis.

### main.py: 69–69

```python
    return {"id": book.id, "title": book.title}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 72–72

```python
@app.get("/authors/{author_id}/books", response_model=list[BookRead])
```

Dekorator `app.get('/authors/{author_id}/books', response_model=list[BookRead])` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 73–73

```python
async def author_books(author_id: int, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Odczytuje autora i jego książki przez eager loading, zanim sesja zostanie zamknięta. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 74–78

```python
    statement = (
        select(Author)
        .options(selectinload(Author.books))
        .where(Author.id == author_id)
    )
```

Obliczamy prawą stronę i przypisujemy wynik do `statement`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Dodaje warunek SQL. Wartości są przekazywane jako parametry, bez składania SQL z wejścia klienta. Buduje opis SELECT, jeszcze bez komunikacji z bazą. Pobiera relację osobnym zbiorczym SELECT; zapobiega leniwemu I/O przy późniejszym czytaniu kolekcji.

### main.py: 79–79

```python
    author = (await db.execute(statement)).scalar_one_or_none()
```

Obliczamy prawą stronę i przypisujemy wynik do `author`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zwraca jeden obiekt albo None. Więcej niż jeden wynik jest błędem. Wysyła zapytanie do bazy; await czeka na wynik, oddając sterowanie pętli zdarzeń.

### main.py: 80–80

```python
    if author is None:
```

Sprawdzamy warunek `author is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 81–81

```python
        raise HTTPException(404, "Author not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 82–82

```python
    return author.books
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
