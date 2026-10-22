# Zadanie 20: JOIN produktu i twórcy

Klucz obcy user_id łączy tabele. Jeden SELECT z JOIN pobiera produkt i użytkownika.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

/products/1 zwraca Notebook i creator: Anna. Brak produktu daje 404.

## Pełny kod

```python
import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from api_support import SESSION, database, positive_id

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

async def get_product(request):
    product_id = positive_id(request.match_info["id"])
    async with request.app[SESSION]() as session:
        statement = select(Product, User).join(User).where(Product.id == product_id)
        result = await session.execute(statement)
        row = result.one_or_none()
        if row is None:
            raise web.HTTPNotFound(text="Product not found")
        product, user = row
        return web.json_response({"id": product.id, "name": product.name, "price": product.price, "creator": user.username})

async def main():
    async with database(Base) as factory:
        async with factory.begin() as session:
            user = User(username="Anna")
            session.add(user)
            await session.flush()
            session.add(Product(name="Notebook", price=1299, user_id=user.id))
        app = web.Application()
        app[SESSION] = factory
        app.router.add_get("/products/{id}", get_product)
        await demo(app, [
            ('GET', '/products/1', None, 200),
            ('GET', '/products/99', None, 404),
        ])

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
from aiohttp import web
```

Import z aiohttp udostępnia narzędzia związane z asynchronicznym HTTP: web buduje serwer, ClientSession wysyła żądania. Import nie uruchamia main ani nie wysyła żądania.

### L3

```python
from lab_support import launch
```

Import z lab_support udostępnia narzędzia związane z zdarzeniami i pomiarem czasu pokazu, niezależnymi od logiki API. Import nie uruchamia main ani nie wysyła żądania.

### L4

```python
from api_support import demo
```

Import z api_support udostępnia narzędzia związane z lokalnym serwerem testowym, walidacją i izolowaną bazą; pełny kod jest w osobnym pliku. Import nie uruchamia main ani nie wysyła żądania.

### L6

```python
from sqlalchemy import ForeignKey, Integer, String, select
```

Import z sqlalchemy udostępnia narzędzia związane z typami kolumn i budowaniem zapytań SQL. Import nie uruchamia main ani nie wysyła żądania.

### L7

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
```

Import z sqlalchemy.orm udostępnia narzędzia związane z bazą modeli, adnotacjami Mapped i definicjami kolumn mapped_column. Import nie uruchamia main ani nie wysyła żądania.

### L8

```python
from api_support import SESSION, database, positive_id
```

Import z api_support udostępnia narzędzia związane z lokalnym serwerem testowym, walidacją i izolowaną bazą; pełny kod jest w osobnym pliku. Import nie uruchamia main ani nie wysyła żądania.

### L10

```python
class Base(DeclarativeBase):
```

Definiujemy klasę Base. Dziedziczenie po DeclarativeBase tworzy rejestr modeli i metadata. To nie tabela biznesowa.

### L11

```python
    pass
```

Pusta instrukcja w ciele Base. Nie potrzebujemy dodatkowych metod; zachowanie dostajemy przez dziedziczenie.

### L13

```python
class User(Base):
```

Definiujemy klasę User. Dziedziczy po Base, więc SQLAlchemy zarejestruje jej tabelę. Sama definicja klasy jeszcze nie tworzy tabeli w PostgreSQL.

### L14

```python
    __tablename__ = "users"
```

Określamy nazwę tabeli SQL jako "users". To nazwa w bazie, która może różnić się od nazwy klasy Pythona.

### L15

```python
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

Pole id: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Klucz główny jednoznacznie identyfikuje rekord; PostgreSQL wygeneruje ID podczas INSERT.

### L16

```python
    username: Mapped[str] = mapped_column(String(50))
```

Pole username: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. String(50) ogranicza tekst do 50 znaków.

### L18

```python
class Product(Base):
```

Definiujemy klasę Product. Dziedziczy po Base, więc SQLAlchemy zarejestruje jej tabelę. Sama definicja klasy jeszcze nie tworzy tabeli w PostgreSQL.

### L19

```python
    __tablename__ = "products"
```

Określamy nazwę tabeli SQL jako "products". To nazwa w bazie, która może różnić się od nazwy klasy Pythona.

### L20

```python
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

Pole id: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Klucz główny jednoznacznie identyfikuje rekord; PostgreSQL wygeneruje ID podczas INSERT.

### L21

```python
    name: Mapped[str] = mapped_column(String(100))
```

Pole name: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. String(100) ogranicza tekst do 100 znaków.

### L22

```python
    price: Mapped[int] = mapped_column(Integer)
```

Pole price: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Integer przechowuje liczbę całkowitą; ceny i salda wyrażamy w groszach, żeby uniknąć błędów float.

### L23

```python
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
```

Pole user_id: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. ForeignKey("users.id") łączy produkt z istniejącym użytkownikiem i pozwala JOIN ustalić warunek połączenia.

### L25

```python
async def get_product(request):
```

Handler otrzyma ID z URL i pobierze produkt. Brak rekordu zostanie zamieniony na odpowiedź 404, zamiast błędu atrybutu None.

### L26

```python
    product_id = positive_id(request.match_info["id"])
```

Router zapisał fragment {id} jako tekst, np. "1". positive_id zamienia go na dodatni int i odrzuca błędne dane statusem 400. product_id będzie użyty w zapytaniu do bazy.

### L27

```python
    async with request.app[SESSION]() as session:
```

request.app to aplikacja, która odebrała żądanie. [SESSION] pobiera fabrykę; () tworzy nową sesję. async with dopilnuje jej zamknięcia i zwrotu połączenia. Samo wejście nie oznacza zapisu danych.

### L28

```python
        statement = select(Product, User).join(User).where(Product.id == product_id)
```

SELECT pobiera pary Product i User. JOIN korzysta z ForeignKey products.user_id → users.id, a where ogranicza wynik do wskazanego produktu. To opis jednego zapytania, jeszcze bez wysyłania do bazy.

### L29

```python
        result = await session.execute(statement)
```

Dopiero execute wysyła przygotowane statement do bazy. await odbiera wynik. result opakowuje wiersze; nie jest jeszcze listą słowników JSON.

### L30

```python
        row = result.one_or_none()
```

Odbieramy jeden wiersz albo None. Ponieważ SELECT obejmuje dwa modele, wiersz zawiera parę obiektów, a nie sam produkt. Więcej niż jeden wiersz zgłosi wyjątek.

### L31

```python
        if row is None:
```

JOIN nie znalazł pasującego rekordu. Zwrócimy 404 przed rozpakowaniem wiersza.

### L32

```python
            raise web.HTTPNotFound(text="Product not found")
```

Przerywamy handler wyjątkiem HTTPNotFound. aiohttp zamieni go na odpowiedź HTTP 404 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L33

```python
        product, user = row
```

Rozpakowujemy dwuelementowy wiersz: pierwszy obiekt trafia do product, drugi do user. Kolejność odpowiada select(Product, User).

### L34

```python
        return web.json_response({"id": product.id, "name": product.name, "price": product.price, "creator": user.username})
```

Zwracamy odpowiedź JSON z wyrażenia {"id": product.id, "name": product.name, "price": product.price, "creator": user.username}. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L36

```python
async def main():
```

Czytaj przebieg: __main__ → launch → asyncio.run(main()) → przygotowanie aplikacji i tras → demo → klient HTTP → router → handler → odpowiedź → dziennik klienta. W zadaniach z bazą database(Base) przygotowuje fabrykę; handler tworzy własną sesję. Definicja handlera pojawia się wcześniej w pliku, ale jego ciało rusza dopiero po żądaniu. W zadaniu 18 main sam wysyła dwa żądania, aby pokazać ich nakładanie.

### L36

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L37

```python
    async with database(Base) as factory:
```

Wchodzimy do pomocnika database z api_support.py. Tworzy osobny schemat w bazie lesson32, tabele z Base.metadata i fabrykę AsyncSession. Przy wyjściu usuwa tylko schemat tego pokazu i zamyka silniki. To przygotowanie demonstracji, a nie kod handlera.

### L38

```python
        async with factory.begin() as session:
```

Fabryka tworzy sesję i rozpoczyna transakcję do przygotowania danych. Przy poprawnym wyjściu zapisze rekordy, a następnie zamknie sesję; wyjątek spowoduje rollback.

### L39

```python
            user = User(username="Anna")
```

Tworzymy użytkownika Anna w pamięci. Kolejne add i flush zapiszą go i pobiorą ID potrzebne jako klucz obcy produktu.

### L40

```python
            session.add(user)
```

Rejestrujemy nowego użytkownika w sesji. Jeszcze nie znamy ID z bazy; uzyskamy je po flush.

### L41

```python
            await session.flush()
```

flush wysyła oczekujące INSERT/UPDATE do PostgreSQL i czeka na odpowiedź. Nowy obiekt otrzymuje ID. To jeszcze nie COMMIT: późniejszy wyjątek nadal może wycofać tę zmianę.

### L42

```python
            session.add(Product(name="Notebook", price=1299, user_id=user.id))
```

Przygotowujemy produkt Notebook za 1299 groszy. user.id znamy po flush użytkownika. user_id łączy produkt z jego twórcą; COMMIT nastąpi przy wyjściu z transakcji.

### L43

```python
        app = web.Application()
```

Tworzymy aplikację aiohttp. Przechowa router i stan; ta linia jeszcze nie otwiera portu ani nie obsługuje żądania.

### L44

```python
        app[SESSION] = factory
```

Pod kluczem SESSION zapisujemy fabrykę sesji, nie jedną wspólną sesję. Każdy handler utworzy własną AsyncSession, więc równoległe żądania nie dzielą transakcji.

### L45

```python
        app.router.add_get("/products/{id}", get_product)
```

Rejestrujemy GET /products/{id} → get_product. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L46

```python
        await demo(app, [
```

Uruchamiamy pomocnika pokazu: startuje prawdziwy serwer na wolnym porcie, klient wysyła wymienione żądania po kolei i porównuje statusy z oczekiwaniami. Każda krotka to (metoda, ścieżka, JSON, oczekiwany status). Dziennik pokazuje również body. Po pokazie serwer jest zamykany.

### L47

```python
            ('GET', '/products/1', None, 200),
```

Przypadek pokazu: GET /products/1. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L48

```python
            ('GET', '/products/99', None, 404),
```

Przypadek pokazu: GET /products/99. Body: None; None oznacza brak danych. Oczekujemy statusu 404. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L49

```python
        ])
```

Zamykamy listę przypadków ] i wywołanie demo ). To kontynuacja poprzedniej instrukcji, a nie osobne działanie. await zaczeka na cały pokaz.

### L51

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L52

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Co zawiera wiersz z select(Product, User)?

<details><summary>Odpowiedź</summary>

Dwa obiekty w kolejności SELECT: Product, potem User.

</details>
