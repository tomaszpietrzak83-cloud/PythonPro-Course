# Zadanie 08 — Dokumentacja Swagger

## Zanim przeczytasz kod

Pobierzemy /openapi.json oraz /docs, potem wyślemy książkę. Możesz też otworzyć osobny Swagger i wykonać Try it out.

Dokumentacja pokaże Book Workshop, wersję 1.0.0, tag books i model Book. POST zwróci tytuł Python Basics.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from fastapi import FastAPI
```

Import udostępnia nazwy: FastAPI. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
from pydantic import BaseModel, Field
```

Import udostępnia nazwy: BaseModel, Field. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–8

```python
app = FastAPI(
    title="Book Workshop",
    description="An educational book API",
    version="1.0.0",
)
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 11–11

```python
class Book(BaseModel):
```

Klasa Book dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 12–12

```python
    title: str = Field(examples=["Python Basics"])
```

Pole `title` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 15–17

```python
@app.post(
    "/books", response_model=Book, tags=["books"], summary="Create a book"
)
```

Dekorator `app.post('/books', response_model=Book, tags=['books'], summary='Create a book')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 18–18

```python
async def create_book(book: Book):
```

Definiujemy korutynę. Otrzymuje dane książki; tworzy rekord lub odsyła zwalidowany model, zależnie od tego ćwiczenia. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 19–19

```python
    """Accept a title, for example Python Basics, and echo validated data."""
```

Docstring opisuje działanie endpointu. FastAPI może wykorzystać go w automatycznej dokumentacji; nie jest wykonywalną instrukcją biznesową.

### main.py: 20–20

```python
    return book
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
