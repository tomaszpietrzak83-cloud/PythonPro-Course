# Zadanie 17 — Lifespan i cache

## Zanim przeczytasz kod

Przy starcie przygotujemy PostgreSQL i odczytamy cache.json. GET pokaże source: startup-file. PUT dopisze topic=FastAPI. Przy zamknięciu zapis trafi do pliku.

Po zamknięciu cache.json zawiera topic: FastAPI. Dziennik potwierdzi kolejność load → żądania → save → zamknięcie połączeń.

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
from contextlib import asynccontextmanager
```

Import udostępnia nazwy: asynccontextmanager. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 5–5

```python
from demo_support import database_lifespan, runtime_file
```

Import udostępnia nazwy: database_lifespan, runtime_file. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 6–6

```python
from fastapi import FastAPI, Request
```

Import udostępnia nazwy: FastAPI, Request. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 7–7

```python
from lab_support import event
```

Import udostępnia nazwy: event. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 8–8

```python
from sqlalchemy.orm import DeclarativeBase
```

Import udostępnia nazwy: DeclarativeBase. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 11–11

```python
class Base(DeclarativeBase):
```

Klasa Base dziedziczy po DeclarativeBase. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 12–12

```python
    pass
```

pass to pusta instrukcja wymagana jako ciało klasy Base. Rejestr modeli i metadata pochodzą z klasy bazowej.

### main.py: 15–15

```python
@asynccontextmanager
```

Dekorator pozwala używać funkcji z yield jako menedżera async with. Start i zamknięcie zasobów należą do jednego zakresu.

### main.py: 16–16

```python
async def lifespan(app):
```

Definiujemy korutynę. Kod przed yield uruchamia zasoby; kod w finally zapisuje cache przy zamykaniu aplikacji. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 17–17

```python
    async with database_lifespan(Base)(app):
```

Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady. Pomocnik tworzy osobny schemat PostgreSQL, tabele i fabrykę sesji; po pokazie zamyka je i usuwa schemat.

### main.py: 18–18

```python
        cache_file = runtime_file("cache.json")
```

Obliczamy prawą stronę i przypisujemy wynik do `cache_file`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Zwraca ścieżkę w osobnym katalogu danych tego pokazu. Nie zapisujemy w plikach kursu ani w danych innych lekcji.

### main.py: 19–23

```python
        cached = (
            await asyncio.to_thread(cache_file.read_text, encoding="utf-8")
            if cache_file.exists()
            else "{}"
        )
```

Obliczamy prawą stronę i przypisujemy wynik do `cached`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Wykonuje blokującą operację plikową w osobnym wątku, aby nie blokować event loop. Sprawdza, czy plik cache już istnieje; przy braku zaczynamy od pustego słownika.

### main.py: 24–24

```python
        app.state.cache = json.loads(cached)
```

Obliczamy prawą stronę i przypisujemy wynik do `app.state.cache`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Parsuje tekst JSON do obiektu Pythona.

### main.py: 25–25

```python
        event("log", "cache", "STARTUP: cache loaded")
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Zapisuje rzeczywiste zdarzenie widoczne w panelu pokazu; nie zmienia danych biznesowych.

### main.py: 26–26

```python
        try:
```

try wyznacza zakres pracy aplikacji. finally uruchomi zapis cache także wtedy, gdy aplikacja wyjdzie przez wyjątek podczas normalnego zamykania.

### main.py: 27–27

```python
            yield
```

yield rozdziela lifespan na start i zamknięcie. Przed yield przygotowujemy zasoby; podczas zawieszenia działa aplikacja; finally wykona sprzątanie.

### main.py: 29–33

```python
            await asyncio.to_thread(
                cache_file.write_text,
                json.dumps(app.state.cache),
                encoding="utf-8",
            )
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Wykonuje blokującą operację plikową w osobnym wątku, aby nie blokować event loop. Koduje obiekt Pythona jako tekst JSON do zapisu w pliku.

### main.py: 34–34

```python
            event("log", "cache", "SHUTDOWN: cache saved")
```

Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania. Zapisuje rzeczywiste zdarzenie widoczne w panelu pokazu; nie zmienia danych biznesowych.

### main.py: 37–37

```python
app = FastAPI(lifespan=lifespan)
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 40–40

```python
@app.get("/cache")
```

Dekorator `app.get('/cache')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 41–41

```python
async def get_cache(request: Request):
```

Definiujemy korutynę. Odczytuje współdzielony cache ze stanu tej aplikacji. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 42–42

```python
    return request.app.state.cache
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 45–45

```python
@app.put("/cache/{key}")
```

Dekorator `app.put('/cache/{key}')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 46–46

```python
async def put_cache(key: str, value: str, request: Request):
```

Definiujemy korutynę. Zmienia wartość cache wskazaną przez klucz ze ścieżki. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 47–47

```python
    request.app.state.cache[key] = value
```

Obliczamy prawą stronę i przypisujemy wynik do `request.app.state.cache[key]`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 48–48

```python
    return request.app.state.cache
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
