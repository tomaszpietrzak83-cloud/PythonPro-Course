# Zadanie 13 — CRUD z PostgreSQL

## Zanim przeczytasz kod

lifespan utworzy tabele. Dodamy książkę, odczytamy ją, zastąpimy dane przez PUT i usuniemy. Każdy zapis przejdzie przez transakcję.

ID pochodzi z PostgreSQL. PUT zmieni tytuł na Advanced Python, a po DELETE odczyt da 404. Od tego zadania ceny w bazie są w groszach.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from demo_support import database_lifespan, get_db
```

Import udostępnia nazwy: database_lifespan, get_db. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
from fastapi import Depends, FastAPI, HTTPException, Response
```

Import udostępnia nazwy: Depends, FastAPI, HTTPException, Response. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

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

### main.py: 45–45

```python
async def list_books(db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Zwraca kolekcję książek; zapytanie SQL może ją ograniczać i sortować. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 46–46

```python
    result = await db.execute(select(Book).order_by(Book.id))
```

Obliczamy prawą stronę i przypisujemy wynik do `result`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Wysyła zapytanie do bazy; await czeka na wynik, oddając sterowanie pętli zdarzeń. Ustala kolejność; dodatkowe ID rozstrzyga remisy przy sortowaniu i paginacji. Buduje opis SELECT, jeszcze bez komunikacji z bazą.

### main.py: 47–47

```python
    return result.scalars().all()
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Zbiera dostępne elementy wyniku do listy. Wyciąga obiekty modelu z wierszy wyniku SELECT.

### main.py: 50–50

```python
@app.get("/books/{book_id}", response_model=BookRead)
```

Dekorator `app.get('/books/{book_id}', response_model=BookRead)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 51–51

```python
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Wyszukuje książkę po ID i obsługuje brak przez 404. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 52–52

```python
    book = await db.get(Book, book_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `book`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### main.py: 53–53

```python
    if book is None:
```

Sprawdzamy warunek `book is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 54–54

```python
        raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 55–55

```python
    return book
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 58–58

```python
@app.put("/books/{book_id}", response_model=BookRead)
```

Dekorator `app.put('/books/{book_id}', response_model=BookRead)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 59–61

```python
async def replace_book(
    book_id: int, data: BookCreate, db: AsyncSession = Depends(get_db)
):
```

Definiujemy korutynę. Pełna aktualizacja PUT zastępuje pola książki danymi z modelu wejściowego. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 62–62

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### main.py: 63–63

```python
        book = await db.get(Book, book_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `book`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### main.py: 64–64

```python
        if book is None:
```

Sprawdzamy warunek `book is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 65–65

```python
            raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 66–66

```python
        book.title = data.title
```

Obliczamy prawą stronę i przypisujemy wynik do `book.title`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 67–67

```python
        book.price = data.price
```

Obliczamy prawą stronę i przypisujemy wynik do `book.price`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 68–68

```python
        book.category = data.category
```

Obliczamy prawą stronę i przypisujemy wynik do `book.category`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 69–69

```python
    return book
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 72–72

```python
@app.delete("/books/{book_id}", status_code=204)
```

Dekorator `app.delete('/books/{book_id}', status_code=204)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 73–73

```python
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
```

Definiujemy korutynę. Usuwa książkę po sprawdzeniu jej istnienia i zwraca status określony w trasie. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.

### main.py: 74–74

```python
    async with db.begin():
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.

### main.py: 75–75

```python
        book = await db.get(Book, book_id)
```

Obliczamy prawą stronę i przypisujemy wynik do `book`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.

### main.py: 76–76

```python
        if book is None:
```

Sprawdzamy warunek `book is None`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 77–77

```python
            raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 78–78

```python
        await db.delete(book)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Oznacza obiekt ORM do usunięcia; transakcja zatwierdzi DELETE przy poprawnym wyjściu.

### main.py: 79–79

```python
    return Response(status_code=204)
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Tworzy odpowiedź HTTP. Przy 204 body musi pozostać puste.
