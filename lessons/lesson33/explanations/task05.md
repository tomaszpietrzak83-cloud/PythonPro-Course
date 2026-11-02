# Zadanie 05 — CRUD w pamięci

## Zanim przeczytasz kod

Dodamy książkę, odczytamy listę i szczegóły, usuniemy rekord, potem zapytamy o niego ponownie. Każdy krok korzysta z tego samego słownika.

Pierwszy rekord ma ID 1. Po DELETE GET zwróci 404. Tutaj sukces tworzenia i usuwania ma 200; zadanie 6 zmieni te statusy.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from fastapi import FastAPI, HTTPException
```

Import udostępnia nazwy: FastAPI, HTTPException. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
from pydantic import BaseModel, Field
```

Import udostępnia nazwy: BaseModel, Field. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
app = FastAPI()
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 5–5

```python
books = {}
```

Obliczamy prawą stronę i przypisujemy wynik do `books`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 6–6

```python
next_id = 1
```

Obliczamy prawą stronę i przypisujemy wynik do `next_id`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 9–9

```python
class BookCreate(BaseModel):
```

Klasa BookCreate dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 10–10

```python
    title: str = Field(min_length=1)
```

Pole `title` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 11–11

```python
    price: float = Field(gt=0)
```

Pole `price` ma deklarowany typ `float`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 14–14

```python
@app.get("/books")
```

Dekorator `app.get('/books')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 15–15

```python
async def list_books():
```

Definiujemy korutynę. Zwraca kolekcję książek; zapytanie SQL może ją ograniczać i sortować. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 16–16

```python
    return list(books.values())
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Zbiera elementy do nowej listy, którą FastAPI może zakodować jako JSON. Zwraca wartości słownika books; list(...) zbiera je do listy odpowiedzi.

### main.py: 19–19

```python
@app.get("/books/{book_id}")
```

Dekorator `app.get('/books/{book_id}')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 20–20

```python
async def get_book(book_id: int):
```

Definiujemy korutynę. Wyszukuje książkę po ID i obsługuje brak przez 404. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 21–21

```python
    if book_id not in books:
```

Sprawdzamy warunek `book_id not in books`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 22–22

```python
        raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 23–23

```python
    return books[book_id]
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 26–26

```python
@app.post("/books")
```

Dekorator `app.post('/books')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 27–27

```python
async def create_book(book: BookCreate):
```

Definiujemy korutynę. Otrzymuje dane książki; tworzy rekord lub odsyła zwalidowany model, zależnie od tego ćwiczenia. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 28–28

```python
    global next_id
```

global next_id oznacza, że przypisanie w funkcji zmieni licznik na poziomie modułu, zamiast tworzyć zmienną lokalną. 

### main.py: 29–29

```python
    record = {"id": next_id, **book.model_dump()}
```

Obliczamy prawą stronę i przypisujemy wynik do `record`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zamienia zwalidowany model Pydantic na słownik. ** rozpakowuje jego klucze jako argumenty lub pola nowego słownika.

### main.py: 30–30

```python
    books[next_id] = record
```

Obliczamy prawą stronę i przypisujemy wynik do `books[next_id]`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 31–31

```python
    next_id += 1
```

Aktualizujemy istniejącą wartość. next_id += 1 zwiększa licznik identyfikatorów; usunięcie książki nie cofa licznika, więc ID nie zostanie przypadkowo ponownie użyte. 

### main.py: 32–32

```python
    return record
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 35–35

```python
@app.delete("/books/{book_id}")
```

Dekorator `app.delete('/books/{book_id}')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 36–36

```python
async def delete_book(book_id: int):
```

Definiujemy korutynę. Usuwa książkę po sprawdzeniu jej istnienia i zwraca status określony w trasie. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 37–37

```python
    if book_id not in books:
```

Sprawdzamy warunek `book_id not in books`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 38–38

```python
        raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 39–39

```python
    del books[book_id]
```

del usuwa wpis ze słownika books. To zmiana w pamięci tego procesu; restart aplikacji odtworzy pusty słownik. 

### main.py: 40–40

```python
    return {"deleted": book_id}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
