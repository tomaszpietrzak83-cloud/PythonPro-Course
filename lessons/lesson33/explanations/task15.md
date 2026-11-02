# Zadanie 15 — Zadania po odpowiedzi

## Zanim przeczytasz kod

Po POST dopiszemy symulację powiadomienia do pliku. Po DELETE zapiszemy liczbę książek. Pokaz poczeka na rzeczywiste pliki i odczyta je.

notifications.log zawiera wpis o ID 1; stats.json zawiera books: 0. Żaden prawdziwy email nie zostanie wysłany.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
import json
```

Import udostępnia nazwy: json. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 3–3

```python
from demo_support import runtime_file
```

Import udostępnia nazwy: runtime_file. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
from fastapi import BackgroundTasks, FastAPI, HTTPException, Response
```

Import udostępnia nazwy: BackgroundTasks, FastAPI, HTTPException, Response. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 5–5

```python
from lab_support import event
```

Import udostępnia nazwy: event. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 6–6

```python
from pydantic import BaseModel, Field
```

Import udostępnia nazwy: BaseModel, Field. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 8–8

```python
app = FastAPI()
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 11–11

```python
def append_notification(book_id):
```

Definiujemy zwykłą funkcję. Zapisuje symulację powiadomienia do pliku po wysłaniu odpowiedzi HTTP. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 12–14

```python
    with runtime_file("notifications.log").open(
        "a", encoding="utf-8"
    ) as stream:
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera plik; tryb a dopisuje dane. with dopilnuje zamknięcia uchwytu. Zwraca ścieżkę w osobnym katalogu danych tego pokazu. Nie zapisujemy w plikach kursu ani w danych innych lekcji.

### main.py: 15–15

```python
        stream.write(f"Book {book_id} created; email simulated\n")
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Zapisuje tekst do otwartego pliku; \n oddziela wpisy dziennika.

### main.py: 16–16

```python
    event("log", "background", f"Notification recorded for book {book_id}")
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Zapisuje rzeczywiste zdarzenie widoczne w panelu pokazu; nie zmienia danych biznesowych.

### main.py: 19–19

```python
def update_stats(count):
```

Definiujemy zwykłą funkcję. Zapisuje aktualną liczbę książek do pliku statystyk. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 20–22

```python
    runtime_file("stats.json").write_text(
        json.dumps({"books": count}), encoding="utf-8"
    )
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Zastępuje zawartość pliku podanym tekstem i kodowaniem UTF-8. Zwraca ścieżkę w osobnym katalogu danych tego pokazu. Nie zapisujemy w plikach kursu ani w danych innych lekcji. Koduje obiekt Pythona jako tekst JSON do zapisu w pliku.

### main.py: 23–23

```python
    event("log", "background", f"Book count recorded: {count}")
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Zapisuje rzeczywiste zdarzenie widoczne w panelu pokazu; nie zmienia danych biznesowych.

### main.py: 26–26

```python
books = {}
```

Obliczamy prawą stronę i przypisujemy wynik do `books`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 27–27

```python
next_id = 1
```

Obliczamy prawą stronę i przypisujemy wynik do `next_id`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 30–30

```python
class BookCreate(BaseModel):
```

Klasa BookCreate dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 31–31

```python
    title: str = Field(min_length=1)
```

Pole `title` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 32–32

```python
    price: float = Field(gt=0)
```

Pole `price` ma deklarowany typ `float`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 35–35

```python
@app.get("/books")
```

Dekorator `app.get('/books')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 36–36

```python
async def list_books():
```

Definiujemy korutynę. Zwraca kolekcję książek; zapytanie SQL może ją ograniczać i sortować. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 37–37

```python
    return list(books.values())
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Zbiera elementy do nowej listy, którą FastAPI może zakodować jako JSON. Zwraca wartości słownika books; list(...) zbiera je do listy odpowiedzi.

### main.py: 40–40

```python
@app.get("/books/{book_id}")
```

Dekorator `app.get('/books/{book_id}')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 41–41

```python
async def get_book(book_id: int):
```

Definiujemy korutynę. Wyszukuje książkę po ID i obsługuje brak przez 404. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 42–42

```python
    if book_id not in books:
```

Sprawdzamy warunek `book_id not in books`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 43–43

```python
        raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 44–44

```python
    return books[book_id]
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 47–47

```python
@app.post("/books", status_code=201)
```

Dekorator `app.post('/books', status_code=201)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 48–48

```python
async def create_book(book: BookCreate, background_tasks: BackgroundTasks):
```

Definiujemy korutynę. Otrzymuje dane książki; tworzy rekord lub odsyła zwalidowany model, zależnie od tego ćwiczenia. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 49–49

```python
    global next_id
```

global next_id oznacza, że przypisanie w funkcji zmieni licznik na poziomie modułu, zamiast tworzyć zmienną lokalną. 

### main.py: 50–50

```python
    record = {"id": next_id, **book.model_dump()}
```

Obliczamy prawą stronę i przypisujemy wynik do `record`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zamienia zwalidowany model Pydantic na słownik. ** rozpakowuje jego klucze jako argumenty lub pola nowego słownika.

### main.py: 51–51

```python
    books[next_id] = record
```

Obliczamy prawą stronę i przypisujemy wynik do `books[next_id]`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 52–52

```python
    next_id += 1
```

Aktualizujemy istniejącą wartość. next_id += 1 zwiększa licznik identyfikatorów; usunięcie książki nie cofa licznika, więc ID nie zostanie przypadkowo ponownie użyte. 

### main.py: 53–53

```python
    background_tasks.add_task(append_notification, record["id"])
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Planuje wykonanie funkcji po wysłaniu odpowiedzi. Przekazujemy funkcję bez (), a dalej jej argumenty.

### main.py: 54–54

```python
    return record
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 57–57

```python
@app.delete("/books/{book_id}", status_code=204)
```

Dekorator `app.delete('/books/{book_id}', status_code=204)` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 58–58

```python
async def delete_book(book_id: int, background_tasks: BackgroundTasks):
```

Definiujemy korutynę. Usuwa książkę po sprawdzeniu jej istnienia i zwraca status określony w trasie. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 59–59

```python
    if book_id not in books:
```

Sprawdzamy warunek `book_id not in books`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 60–60

```python
        raise HTTPException(404, "Book not found")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 61–61

```python
    del books[book_id]
```

del usuwa wpis ze słownika books. To zmiana w pamięci tego procesu; restart aplikacji odtworzy pusty słownik. 

### main.py: 62–62

```python
    background_tasks.add_task(update_stats, len(books))
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Planuje wykonanie funkcji po wysłaniu odpowiedzi. Przekazujemy funkcję bez (), a dalej jej argumenty. Zwraca liczbę elementów lub bajtów. W zależności od argumentu jest to liczba książek albo rozmiar body.

### main.py: 63–63

```python
    return Response(status_code=204)
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Tworzy odpowiedź HTTP. Przy 204 body musi pozostać puste.
