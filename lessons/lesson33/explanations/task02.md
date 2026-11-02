# Zadanie 02 — Parametr ścieżki i walidacja

## Zanim przeczytasz kod

Najpierw wyślemy /greet/Anna, potem /greet/A. FastAPI wyciągnie name ze ścieżki i sprawdzi długość. Tylko poprawne imię dotrze do greet.

Anna dostanie Hello, Anna! i 200. Jedna litera da 422 z opisem pola; funkcja powitania nie wykona się dla tego wejścia.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from typing import Annotated
```

Import udostępnia nazwy: Annotated. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 3–3

```python
from fastapi import FastAPI, Path
```

Import udostępnia nazwy: FastAPI, Path. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 5–5

```python
app = FastAPI()
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 8–8

```python
@app.get("/greet/{name}")
```

Dekorator `app.get('/greet/{name}')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 9–9

```python
async def greet(name: Annotated[str, Path(min_length=2)]):
```

Definiujemy korutynę. Otrzymuje imię ze ścieżki, już po walidacji minimum dwóch znaków. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Definiuje walidację parametru pochodzącego z fragmentu URL.

### main.py: 10–10

```python
    return {"message": f"Hello, {name}!"}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
