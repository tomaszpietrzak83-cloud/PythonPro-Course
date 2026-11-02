# Zadanie 10 — Dependency i klucz API

## Zanim przeczytasz kod

Najpierw wyślemy GET bez klucza. Potem użyjemy lesson-demo-key dla trzech tras i sprawdzimy błędny klucz.

Brak lub zły klucz da 401. Poprawny klucz dopuści /books, /authors i /stats. To jawny klucz demonstracyjny.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
import secrets
```

Import udostępnia nazwy: secrets. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
from typing import Annotated
```

Import udostępnia nazwy: Annotated. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
from fastapi import Depends, FastAPI, Header, HTTPException
```

Import udostępnia nazwy: Depends, FastAPI, Header, HTTPException. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 6–6

```python
app = FastAPI()
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 9–9

```python
async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None):
```

Definiujemy korutynę. Dependency sprawdza nagłówek X-API-Key przed uruchomieniem endpointu. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. Pobiera nagłówek HTTP; x_api_key odpowiada nazwie X-API-Key.

### main.py: 10–12

```python
    if x_api_key is None or not secrets.compare_digest(
        x_api_key, "lesson-demo-key"
    ):
```

Sprawdzamy warunek `x_api_key is None or not secrets.compare_digest(x_api_key, 'lesson-demo-key')`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. Porównuje klucz z wartością demonstracyjną metodą przeznaczoną do porównań sekretów.

### main.py: 13–13

```python
        raise HTTPException(401, "Invalid API key")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 14–14

```python
    return x_api_key
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 17–17

```python
@app.get("/books", dependencies=[Depends(verify_api_key)])
```

Dekorator `app.get('/books', dependencies=[Depends(verify_api_key)])` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 18–18

```python
async def list_books():
```

Definiujemy korutynę. Zwraca kolekcję książek; zapytanie SQL może ją ograniczać i sortować. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 19–19

```python
    return {"books": []}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 22–22

```python
@app.get("/authors", dependencies=[Depends(verify_api_key)])
```

Dekorator `app.get('/authors', dependencies=[Depends(verify_api_key)])` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 23–23

```python
async def list_authors():
```

Definiujemy korutynę. Zwraca listę autorów z tego modułu routera. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 24–24

```python
    return {"authors": []}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 27–27

```python
@app.get("/stats", dependencies=[Depends(verify_api_key)])
```

Dekorator `app.get('/stats', dependencies=[Depends(verify_api_key)])` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 28–28

```python
async def stats():
```

Definiujemy korutynę. Zwraca demonstracyjne statystyki po pomyślnym sprawdzeniu klucza. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 29–29

```python
    return {"count": 0}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
