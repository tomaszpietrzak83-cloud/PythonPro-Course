# Zadanie 12 — Własny walidator

## Zanim przeczytasz kod

Wyślemy Book123 z ceną 40 i kategorią Books, potem osobno zepsujemy nazwę, zakres ceny i kategorię.

Poprawny produkt da 200. Spacje/interpunkcja w nazwie, cena 10001 i kategoria Other dadzą 422.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from typing import Literal
```

Import udostępnia nazwy: Literal. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 3–3

```python
from fastapi import FastAPI
```

Import udostępnia nazwy: FastAPI. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
from pydantic import BaseModel, Field, field_validator
```

Import udostępnia nazwy: BaseModel, Field, field_validator. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 6–6

```python
app = FastAPI()
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 9–9

```python
class Product(BaseModel):
```

Klasa Product dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 10–10

```python
    name: str
```

Pole `name` ma deklarowany typ `str`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. 

### main.py: 11–11

```python
    price: float = Field(gt=0, le=10000)
```

Pole `price` ma deklarowany typ `float`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.

### main.py: 12–12

```python
    category: Literal["Electronics", "Books", "Clothing"]
```

Pole `category` ma deklarowany typ `Literal['Electronics', 'Books', 'Clothing']`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. 

### main.py: 14–14

```python
    @field_validator("name")
```

Rejestrujemy własną regułę dla pola name. FastAPI uruchomi ją podczas walidacji modelu, zanim wywoła endpoint.

### main.py: 15–15

```python
    @classmethod
```

classmethod przekazuje klasę jako cls do walidatora; walidacja nie potrzebuje jeszcze gotowego obiektu modelu.

### main.py: 16–16

```python
    def validate_name(cls, value):
```

Definiujemy zwykłą funkcję. Walidator pola odrzuca nazwy zawierające inne znaki niż litery i cyfry. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 17–17

```python
        if not value.isalnum():
```

Sprawdzamy warunek `not value.isalnum()`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych. Sprawdza niepusty tekst złożony tylko z liter i cyfr; spacje i interpunkcja są odrzucane.

### main.py: 18–18

```python
            raise ValueError("Use letters and digits only")
```

raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback. 

### main.py: 19–19

```python
        return value
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 

### main.py: 22–22

```python
@app.post("/products")
```

Dekorator `app.post('/products')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 23–23

```python
async def create_product(product: Product):
```

Definiujemy korutynę. Otrzymuje Product po wykonaniu wszystkich reguł walidacji. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 24–24

```python
    return product
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
