# Zadanie 07 — Walidacja emaila

## Zanim przeczytasz kod

Wyślemy poprawny email i tekst not-an-email. Pydantic spróbuje utworzyć model User. Tylko poprawny model dotrze do endpointu.

anna@example.com wróci jako JSON z 200. Niepoprawna składnia da 422 z lokalizacją body.email.

## Dokładne wyjaśnienie

### main.py: 1–1

```python
from fastapi import FastAPI
```

Import udostępnia nazwy: FastAPI. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 2–2

```python
from pydantic import BaseModel, EmailStr
```

Import udostępnia nazwy: BaseModel, EmailStr. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.

### main.py: 4–4

```python
app = FastAPI()
```

Obliczamy prawą stronę i przypisujemy wynik do `app`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję. Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.

### main.py: 7–7

```python
class User(BaseModel):
```

Klasa User dziedziczy po BaseModel. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.

### main.py: 8–8

```python
    email: EmailStr
```

Pole `email` ma deklarowany typ `EmailStr`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane. 

### main.py: 11–11

```python
@app.post("/users")
```

Dekorator `app.post('/users')` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.

### main.py: 12–12

```python
async def create_user(user: User):
```

Definiujemy korutynę. Otrzymuje model użytkownika zwalidowany przez Pydantic. Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. 

### main.py: 13–13

```python
    return user
```

return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku. 
