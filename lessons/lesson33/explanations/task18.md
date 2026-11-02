# Zadanie 18 — Filtrowanie i paginacja

## Zanim przeczytasz kod

Zapiszemy dwie książki. Potem wybierzemy Technology, cenę 1000–2000 groszy i sortowanie po tytule. Pokażemy również ujemny skip i nieznane sortowanie.

Filtr zwróci wyłącznie Async Patterns. skip=-1 da 422; sort_by=unknown da 400. Lista dozwolonych pól chroni sposób budowania sortowania.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from demo_support import database_lifespan, get_db
```

Import udostępnia nazwy: database_lifespan, get_db. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
from fastapi import Depends, FastAPI, HTTPException, Query, Response
```

Import udostępnia nazwy: Depends, FastAPI, HTTPException, Query, Response. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 3–3

```python
from pydantic import BaseModel, ConfigDict, Field
```

Import udostępnia nazwy: BaseModel, ConfigDict, Field. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
from sqlalchemy import Integer, String, select
```

Import udostępnia nazwy: Integer, String, select. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 5–5

```python
from sqlalchemy.ext.asyncio import AsyncSession
```

Import udostępnia nazwy: AsyncSession. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 6–6

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
```

Import udostępnia nazwy: DeclarativeBase, Mapped, mapped_column. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 9–9

```python
class Base(DeclarativeBase):
```

Klasa Base dziedziczy po DeclarativeBase. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 10–10

```python
    pass
```

pass to pusta instrukcja wymagana jako ciało klasy Base. Rejestr modeli i metadata pochodzą z klasy bazowej.

### main.py: 13–13

```python
class Book(Base):
```

Klasa Book dziedziczy po Base. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 14–14

```python
    __tablename__ = "books"
```

Obliczamy prawą stronę i przypisujemy wynik do `__tablename__`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 15–15

```python
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

Pole `id` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny.

### main.py: 16–16

```python
    title: Mapped[str] = mapped_column(String(100))
```

Pole `title` ma deklarowany typ `Mapped[str]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Określa typ tekstowej kolumny i maksymalną długość w bazie.

### main.py: 17–17

```python
    price: Mapped[int] = mapped_column(Integer)
```

Pole `price` ma deklarowany typ `Mapped[int]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny.

### main.py: 18–18

```python
    category: Mapped[str] = mapped_column(String(40), default="Books")
```

Pole `category` ma deklarowany typ `Mapped[str]`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny. Określa typ tekstowej kolumny i maksymalną długość w bazie.

### main.py: 21–21

```python
class BookCreate(BaseModel):
```

Klasa BookCreate dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 22–22

```python
    title: str = Field(min_length=1, max_length=100)
```

Pole `title` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 23–23

```python
    price: int = Field(gt=0, le=1000000)
```

Pole `price` ma deklarowany typ `int`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 24–24

```python
    category: str = Field(default="Books", max_length=40)
```

Pole `category` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 27–27

```python
class BookRead(BookCreate):
```

Klasa BookRead dziedziczy po BookCreate. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 28–28

```python
    model_config = ConfigDict(from_attributes=True)
```

Obliczamy prawą stronę i przypisujemy wynik do `model_config`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. from_attributes=True pozwala modelowi odpowiedzi czytać atrybuty obiektu ORM.

### main.py: 29–29

```python
    id: int
```

Pole `id` ma deklarowany typ `int`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. 

### main.py: 32–32

```python
app = FastAPI(lifespan=database_lifespan(Base))
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację. Pomocnik tworzy osobny schemat PostgreSQL, tabele i fabrykę sesji; po pokazie zamyka je i usuwa schemat.

### main.py: 35–35

```python
@app.post("/books", response_model=BookRead, status_code=201)
```

Dekorator `app.post('/books', response_model=BookRead, status_code=201)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 36–36

```python
async def create_book(data: BookCreate, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Otrzymuje dane książki; tworzy rekord lub odsyła zwalidowany model, zależnie od tego ćwiczenia. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 37–37

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### main.py: 38–38

```python
        book = Book(**data.model_dump())
```

Obliczamy prawą stronę i przypisujemy wynik do `book`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zamienia zwalidowany model Pydantic na słownik. ** rozpakowuje jego klucze jako argumenty lub pola nowego słownika.

### main.py: 39–39

```python
        db.add(book)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Dołącza obiekt ORM do sesji. Nie wykonuje jeszcze INSERT i nie potrzebuje await.

### main.py: 40–40

```python
        await db.flush()
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Wysyła oczekujące INSERT/UPDATE i pobiera wygenerowane ID. To jeszcze nie commit; wyjątek nadal może wycofać zapis.

### main.py: 41–41

```python
    return book
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 44–44

```python
@app.get("/books", response_model=list[BookRead])
```

Dekorator `app.get('/books', response_model=list[BookRead])` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 45–53

```python
async def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: str | None = None,
    min_price: int = Query(0, ge=0),
    max_price: int | None = Query(None, ge=0),
    sort_by: str = "price",
    db: AsyncSession = Depends(get_db),
):
```

Definiujemy korutynę. Zwraca kolekcję książek; zapytanie SQL może ją ograniczać i sortować. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Pobiera parametr query i ustala wartość domyślną oraz granice walidacji. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 54–54

```python
    if max_price is not None and min_price > max_price:
```

Sprawdzamy warunek `max_price is not None and min_price > max_price`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 55–55

```python
        raise HTTPException(400, "Invalid price range")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 56–56

```python
    if sort_by not in {"price", "title"}:
```

Sprawdzamy warunek `sort_by not in {'price', 'title'}`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 57–57

```python
        raise HTTPException(400, "Unknown sort field")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 58–58

```python
    statement = select(Book).where(Book.price >= min_price)
```

Obliczamy prawą stronę i przypisujemy wynik do `statement`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Dodaje warunek SQL. Wartości są przekazywane jako parametry, bez składania SQL z wejścia klienta. Buduje opis SELECT, jeszcze bez komunikacji z bazą.

### main.py: 59–59

```python
    if max_price is not None:
```

Sprawdzamy warunek `max_price is not None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 60–60

```python
        statement = statement.where(Book.price <= max_price)
```

Obliczamy prawą stronę i przypisujemy wynik do `statement`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Dodaje warunek SQL. Wartości są przekazywane jako parametry, bez składania SQL z wejścia klienta.

### main.py: 61–61

```python
    if category is not None:
```

Sprawdzamy warunek `category is not None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 62–62

```python
        statement = statement.where(Book.category == category)
```

Obliczamy prawą stronę i przypisujemy wynik do `statement`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Dodaje warunek SQL. Wartości są przekazywane jako parametry, bez składania SQL z wejścia klienta.

### main.py: 63–63

```python
    order = Book.price if sort_by == "price" else Book.title
```

Obliczamy prawą stronę i przypisujemy wynik do `order`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 64–64

```python
    statement = statement.order_by(order, Book.id).offset(skip).limit(limit)
```

Obliczamy prawą stronę i przypisujemy wynik do `statement`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Ogranicza maksymalną liczbę pobranych rekordów. Określa liczbę rekordów pomijanych przed stroną wyników. Ustala kolejność; dodatkowe ID rozstrzyga remisy przy sortowaniu i paginacji.

### main.py: 65–65

```python
    result = await db.execute(statement)
```

Obliczamy prawą stronę i przypisujemy wynik do `result`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Wysyła zapytanie do bazy; await czeka na wynik, oddając sterowanie pętli zdarzeń.

### main.py: 66–66

```python
    return result.scalars().all()
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Zbiera dostępne elementy wyniku do listy. Wyciąga obiekty modelu z wierszy wyniku SELECT.

### main.py: 69–69

```python
@app.get("/books/{book_id}", response_model=BookRead)
```

Dekorator `app.get('/books/{book_id}', response_model=BookRead)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 70–70

```python
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Wyszukuje książkę po ID i obsługuje brak przez 404. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 71–71

```python
    book = await db.get(Book, book_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `book`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### main.py: 72–72

```python
    if book is None:
```

Sprawdzamy warunek `book is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 73–73

```python
        raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 74–74

```python
    return book
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 77–77

```python
@app.put("/books/{book_id}", response_model=BookRead)
```

Dekorator `app.put('/books/{book_id}', response_model=BookRead)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 78–80

```python
async def replace_book(
    book_id: int, data: BookCreate, db: AsyncSession = Depends(get_db)
):
```

Definiujemy korutynę. Pełna aktualizacja PUT zastępuje pola książki danymi z modelu wejściowego. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 81–81

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### main.py: 82–82

```python
        book = await db.get(Book, book_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `book`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### main.py: 83–83

```python
        if book is None:
```

Sprawdzamy warunek `book is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 84–84

```python
            raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 85–85

```python
        book.title = data.title
```

Obliczamy prawą stronę i przypisujemy wynik do `book.title`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 86–86

```python
        book.price = data.price
```

Obliczamy prawą stronę i przypisujemy wynik do `book.price`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 87–87

```python
        book.category = data.category
```

Obliczamy prawą stronę i przypisujemy wynik do `book.category`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 88–88

```python
    return book
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 91–91

```python
@app.delete("/books/{book_id}", status_code=204)
```

Dekorator `app.delete('/books/{book_id}', status_code=204)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 92–92

```python
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Usuwa książkę po sprawdzeniu jej istnienia i zwraca status określony w trasie. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 93–93

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### main.py: 94–94

```python
        book = await db.get(Book, book_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `book`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### main.py: 95–95

```python
        if book is None:
```

Sprawdzamy warunek `book is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 96–96

```python
            raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 97–97

```python
        await db.delete(book)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Oznacza obiekt ORM do usunięcia; transakcja zatwierdzi DELETE przy poprawnym wyjściu.

### main.py: 98–98

```python
    return Response(status_code=204)
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Tworzy odpowiedź HTTP. Przy 204 body musi pozostać puste.
