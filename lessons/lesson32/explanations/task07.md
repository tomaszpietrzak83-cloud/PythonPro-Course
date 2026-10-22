# Zadanie 07: Model Product i tabela

DeclarativeBase rejestruje modele; Mapped opisuje typy, a mapped_column kolumny SQL.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

PostgreSQL tworzy tabelę products z id, name, price. Cena ma jednostkę groszy.

## Pełny kod

```python
import asyncio
from lab_support import launch, metric

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from api_support import database

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

async def main():
    async with database(Base) as factory:
        metric("Columns", str(list(Product.__table__.columns.keys())))
        metric("Price unit", "integer cents")

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
```

## Linijka po linijce

### L1

```python
import asyncio
```

Import z asyncio udostępnia narzędzia związane z pętlą zdarzeń, korutynami, sleep i gather. Import nie uruchamia main ani nie wysyła żądania.

### L2

```python
from lab_support import launch, metric
```

Import z lab_support udostępnia narzędzia związane z zdarzeniami i pomiarem czasu pokazu, niezależnymi od logiki API. Import nie uruchamia main ani nie wysyła żądania.

### L4

```python
from sqlalchemy import Integer, String
```

Import z sqlalchemy udostępnia narzędzia związane z typami kolumn i budowaniem zapytań SQL. Import nie uruchamia main ani nie wysyła żądania.

### L5

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
```

Import z sqlalchemy.orm udostępnia narzędzia związane z bazą modeli, adnotacjami Mapped i definicjami kolumn mapped_column. Import nie uruchamia main ani nie wysyła żądania.

### L6

```python
from api_support import database
```

Import z api_support udostępnia narzędzia związane z lokalnym serwerem testowym, walidacją i izolowaną bazą; pełny kod jest w osobnym pliku. Import nie uruchamia main ani nie wysyła żądania.

### L8

```python
class Base(DeclarativeBase):
```

Definiujemy klasę Base. Dziedziczenie po DeclarativeBase tworzy rejestr modeli i metadata. To nie tabela biznesowa.

### L9

```python
    pass
```

Pusta instrukcja w ciele Base. Nie potrzebujemy dodatkowych metod; zachowanie dostajemy przez dziedziczenie.

### L11

```python
class Product(Base):
```

Definiujemy klasę Product. Dziedziczy po Base, więc SQLAlchemy zarejestruje jej tabelę. Sama definicja klasy jeszcze nie tworzy tabeli w PostgreSQL.

### L12

```python
    __tablename__ = "products"
```

Określamy nazwę tabeli SQL jako "products". To nazwa w bazie, która może różnić się od nazwy klasy Pythona.

### L13

```python
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

Pole id: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Klucz główny jednoznacznie identyfikuje rekord; PostgreSQL wygeneruje ID podczas INSERT.

### L14

```python
    name: Mapped[str] = mapped_column(String(100))
```

Pole name: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. String(100) ogranicza tekst do 100 znaków.

### L15

```python
    price: Mapped[int] = mapped_column(Integer)
```

Pole price: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Integer przechowuje liczbę całkowitą; ceny i salda wyrażamy w groszach, żeby uniknąć błędów float.

### L17

```python
    def to_dict(self):
```

Zwykła metoda modelu, bez async: zamieni już dostępne atrybuty self na słownik. Nie wykonuje zapytania SQL.

### L18

```python
        return {"id": self.id, "name": self.name, "price": self.price}
```

self oznacza bieżący produkt. Tworzymy słownik z trzema wartościami, które można zapisać jako JSON. return oddaje go wywołującej funkcji i kończy metodę.

### L20

```python
async def main():
```

Przy ładowaniu pliku SQLAlchemy rejestruje Base i Product. Potem __main__ → asyncio.run(main()) → database(Base) → utworzenie tabel → odczyt definicji kolumn → metric → usunięcie schematu pokazu. W tym zadaniu nie ma jeszcze handlera HTTP.

### L20

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L21

```python
    async with database(Base) as factory:
```

Wchodzimy do pomocnika database z api_support.py. Tworzy osobny schemat w bazie lesson32, tabele z Base.metadata i fabrykę AsyncSession. Przy wyjściu usuwa tylko schemat tego pokazu i zamyka silniki. To przygotowanie demonstracji, a nie kod handlera.

### L22

```python
        metric("Columns", str(list(Product.__table__.columns.keys())))
```

Publikujemy wskazaną wartość w panelu wyników i terminalu jako zdarzenie JSON. Argument pierwszy jest etykietą, drugi wynikiem. Nie zmieniamy danych w bazie; str zamienia listę na czytelny tekst, a data["data"]["amount"] odczytuje cenę z zagnieżdżonego JSON.

### L23

```python
        metric("Price unit", "integer cents")
```

Publikujemy wskazaną wartość w panelu wyników i terminalu jako zdarzenie JSON. Argument pierwszy jest etykietą, drugi wynikiem. Nie zmieniamy danych w bazie; str zamienia listę na czytelny tekst, a data["data"]["amount"] odczytuje cenę z zagnieżdżonego JSON.

### L25

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L26

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Dlaczego price jest Integer?

<details><summary>Odpowiedź</summary>

1299 groszy reprezentuje 12,99 zł bez błędów zaokrągleń float.

</details>
