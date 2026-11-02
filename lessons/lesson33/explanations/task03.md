# Zadanie 03 — Kalkulator query

## Zanim przeczytasz kod

Wyślemy a=12 i b=3 dla czterech operacji. Endpoint wybierze gałąź obliczenia. Potem spróbujemy dzielić przez zero i przesłać tekst zamiast liczby.

Poprawne wyniki: 15, 9, 36 i 4. Dzielenie przez zero da 400, a niepoprawny int da 422.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from typing import Literal
```

Import udostępnia nazwy: Literal. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 3–3

```python
from fastapi import FastAPI, HTTPException
```

Import udostępnia nazwy: FastAPI, HTTPException. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 5–5

```python
app = FastAPI()
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 8–8

```python
@app.get("/calculate")
```

Dekorator `app.get('/calculate')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 9–13

```python
async def calculate(
    a: int,
    b: int,
    operation: Literal["add", "subtract", "multiply", "divide"] = "add",
):
```

Definiujemy korutynę. Wybiera działanie według operation i odrzuca dzielenie przez zero. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 14–14

```python
    if operation == "divide" and b == 0:
```

Sprawdzamy warunek `operation == 'divide' and b == 0`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 15–15

```python
        raise HTTPException(400, "Cannot divide by zero")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.

### main.py: 16–16

```python
    if operation == "add":
```

Sprawdzamy warunek `operation == 'add'`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 17–17

```python
        result = a + b
```

Obliczamy prawą stronę i przypisujemy wynik do `result`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 18–18

```python
    elif operation == "subtract":
```

Sprawdzamy warunek `operation == 'subtract'`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 19–19

```python
        result = a - b
```

Obliczamy prawą stronę i przypisujemy wynik do `result`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 20–20

```python
    elif operation == "multiply":
```

Sprawdzamy warunek `operation == 'multiply'`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. 

### main.py: 21–21

```python
        result = a * b
```

Obliczamy prawą stronę i przypisujemy wynik do `result`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 23–23

```python
        result = a / b
```

Obliczamy prawą stronę i przypisujemy wynik do `result`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. 

### main.py: 24–24

```python
    return {"result": result}
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
