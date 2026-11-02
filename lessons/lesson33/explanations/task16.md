# Zadanie 16 — Middleware i dziennik

## Zanim przeczytasz kod

Wyślemy poprawny /books i nieistniejący /missing. Oba przejdą przez middleware. Log zostanie dopisany bez blokowania pętli zapisem pliku.

Zobaczysz 200 i 404, nagłówki X-Request-ID oraz dwa wiersze requests.log z czasem i identyfikatorem.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
import asyncio
```

Import udostępnia nazwy: asyncio. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
import json
```

Import udostępnia nazwy: json. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 3–3

```python
import time
```

Import udostępnia nazwy: time. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
import uuid
```

Import udostępnia nazwy: uuid. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 6–6

```python
from demo_support import runtime_file
```

Import udostępnia nazwy: runtime_file. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 7–7

```python
from fastapi import FastAPI, Request
```

Import udostępnia nazwy: FastAPI, Request. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 9–9

```python
app = FastAPI()
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 10–10

```python
log_lock = asyncio.Lock()
```

Obliczamy prawą stronę i przypisujemy wynik do `log_lock`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy blokadę dla korutyn; zabezpiecza wspólne dopisywanie do pliku dziennika.

### main.py: 13–13

```python
@app.middleware("http")
```

Rejestrujemy middleware HTTP. Wykona kod przed endpointem, a po await call_next może zmienić nagłówki i zapisać pomiar.

### main.py: 14–14

```python
async def log_request(request: Request, call_next):
```

Definiujemy korutynę. Middleware otacza obsługę żądania: mierzy czas, nadaje ID i zapisuje log. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 15–15

```python
    request_id = uuid.uuid4().hex
```

Obliczamy prawą stronę i przypisujemy wynik do `request_id`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy losowy identyfikator żądania; hex zamienia go na tekst.

### main.py: 16–16

```python
    started = time.perf_counter()
```

Obliczamy prawą stronę i przypisujemy wynik do `started`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Odczytuje zegar monotoniczny do pomiaru czasu trwania; różnica dwóch odczytów daje sekundy.

### main.py: 17–17

```python
    response = await call_next(request)
```

Obliczamy prawą stronę i przypisujemy wynik do `response`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Przekazuje żądanie do kolejnego middleware lub endpointu i czeka na odpowiedź.

### main.py: 18–18

```python
    response.headers["X-Request-ID"] = request_id
```

Obliczamy prawą stronę i przypisujemy wynik do `response.headers['X-Request-ID']`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 19–24

```python
    entry = {
        "method": request.method,
        "path": request.url.path,
        "seconds": time.perf_counter() - started,
        "request_id": request_id,
    }
```

Obliczamy prawą stronę i przypisujemy wynik do `entry`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Odczytuje zegar monotoniczny do pomiaru czasu trwania; różnica dwóch odczytów daje sekundy.

### main.py: 25–25

```python
    async with log_lock:
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. 

### main.py: 26–26

```python
        await asyncio.to_thread(append_log, entry)
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Wykonuje blokującą operację plikową w osobnym wątku, aby nie blokować event loop.

### main.py: 27–27

```python
    return response
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 30–30

```python
def append_log(entry):
```

Definiujemy zwykłą funkcję. Dopisuje jeden wiersz JSON do pliku dziennika. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 31–31

```python
    with runtime_file("requests.log").open("a", encoding="utf-8") as stream:
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Otwiera plik; tryb a dopisuje dane. with dopilnuje zamknięcia uchwytu. Zwraca ścieżkę w osobnym katalogu danych tego pokazu. Nie zapisujemy w plikach kursu ani w danych innych lekcji.

### main.py: 32–32

```python
        stream.write(json.dumps(entry) + "\n")
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Zapisuje tekst do otwartego pliku; \n oddziela wpisy dziennika. Koduje obiekt Pythona jako tekst JSON do zapisu w pliku.

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
    return {"books": []}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
