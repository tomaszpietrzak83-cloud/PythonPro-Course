# Zadanie 01 — Pierwsze API

## Zanim przeczytasz kod

Klient wyśle trzy GET: /, /time i /random. Router wybierze inną funkcję dla każdego adresu. Funkcja przygotuje słownik; FastAPI odeśle JSON.

Zobaczysz Hello, czas UTC i losową liczbę od 1 do 100. Każde żądanie zakończy się HTTP 200.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
import random
```

Import udostępnia nazwy: random. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
from datetime import datetime, timezone
```

Import udostępnia nazwy: datetime, timezone. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
from fastapi import FastAPI
```

Import udostępnia nazwy: FastAPI. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 6–6

```python
app = FastAPI()
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 9–9

```python
@app.get("/")
```

Dekorator `app.get('/')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 10–10

```python
async def root():
```

Definiujemy korutynę. Zwraca stałą wiadomość powitalną. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 11–11

```python
    return {"message": "Hello"}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 14–14

```python
@app.get("/time")
```

Dekorator `app.get('/time')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 15–15

```python
async def current_time():
```

Definiujemy korutynę. Odczytuje czas UTC i zwraca go jako tekst ISO w JSON. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 16–16

```python
    return {"time": datetime.now(timezone.utc).isoformat()}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Zamienia datę na tekst ISO możliwy do zapisania w JSON. Odczytuje czas; timezone.utc nadaje mu jawną strefę UTC.

### main.py: 19–19

```python
@app.get("/random")
```

Dekorator `app.get('/random')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 20–20

```python
async def random_number():
```

Definiujemy korutynę. Losuje liczbę całkowitą 1–100, włącznie z obiema granicami. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 21–21

```python
    return {"number": random.randint(1, 100)}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. Losuje liczbę całkowitą pomiędzy obiema podanymi granicami, włącznie.
