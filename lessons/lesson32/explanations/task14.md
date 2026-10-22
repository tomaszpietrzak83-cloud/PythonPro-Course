# Zadanie 14: Częściowa aktualizacja PATCH

PATCH zmienia tylko przesłane pola. ORM śledzi zmiany atrybutów i zapisuje je w transakcji.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

Cena Notebook zmienia się z 1299 na 999; GET potwierdza zapis. Nazwa pozostaje Notebook.

## Pełny kod

```python
import asyncio
from aiohttp import web
from lab_support import event, launch
from api_support import demo

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from api_support import SESSION, database, object_json, product_fields, positive_id

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

async def create_product(request):
    data = product_fields(await object_json(request))
    async with request.app[SESSION]() as session:
        async with session.begin():
            product = Product(name=data["name"], price=data["price"])
            session.add(product)
            await session.flush()
            result = product.to_dict()
        event("log", "transaction", "COMMIT: product saved")
    return web.json_response(result, status=201)

async def list_products(request):
    async with request.app[SESSION]() as session:
        statement = select(Product).order_by(Product.id)
        result = await session.execute(statement)
        products = result.scalars().all()
        return web.json_response([product.to_dict() for product in products])

async def get_product(request):
    product_id = positive_id(request.match_info["id"])
    async with request.app[SESSION]() as session:
        product = await session.get(Product, product_id)
        if product is None:
            raise web.HTTPNotFound(text="Product not found")
        return web.json_response(product.to_dict())

async def update_product(request):
    product_id = positive_id(request.match_info["id"])
    data = product_fields(await object_json(request), partial=True)
    async with request.app[SESSION]() as session:
        async with session.begin():
            product = await session.get(Product, product_id)
            if product is None:
                raise web.HTTPNotFound(text="Product not found")
            if "name" in data:
                product.name = data["name"]
            if "price" in data:
                product.price = data["price"]
            await session.flush()
            result = product.to_dict()
    return web.json_response(result)

async def main():
    async with database(Base) as factory:
        app = web.Application()
        app[SESSION] = factory
        app.router.add_post("/products", create_product)
        app.router.add_get("/products", list_products)
        app.router.add_get("/products/{id}", get_product)
        app.router.add_patch("/products/{id}", update_product)
        await demo(app, [
            ('POST', '/products', {'name': 'Notebook', 'price': 1299}, 201),
            ('GET', '/products', None, 200),
            ('GET', '/products/1', None, 200),
            ('GET', '/products/999', None, 404),
            ('PATCH', '/products/1', {'price': 999}, 200),
            ('GET', '/products/1', None, 200),
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
from lab_support import event, launch
```

Import z lab_support udostępnia narzędzia związane z zdarzeniami i pomiarem czasu pokazu, niezależnymi od logiki API. Import nie uruchamia main ani nie wysyła żądania.

### L4

```python
from api_support import demo
```

Import z api_support udostępnia narzędzia związane z lokalnym serwerem testowym, walidacją i izolowaną bazą; pełny kod jest w osobnym pliku. Import nie uruchamia main ani nie wysyła żądania.

### L6

```python
from sqlalchemy import Integer, String, select
```

Import z sqlalchemy udostępnia narzędzia związane z typami kolumn i budowaniem zapytań SQL. Import nie uruchamia main ani nie wysyła żądania.

### L7

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
```

Import z sqlalchemy.orm udostępnia narzędzia związane z bazą modeli, adnotacjami Mapped i definicjami kolumn mapped_column. Import nie uruchamia main ani nie wysyła żądania.

### L8

```python
from api_support import SESSION, database, object_json, product_fields, positive_id
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
class Product(Base):
```

Definiujemy klasę Product. Dziedziczy po Base, więc SQLAlchemy zarejestruje jej tabelę. Sama definicja klasy jeszcze nie tworzy tabeli w PostgreSQL.

### L14

```python
    __tablename__ = "products"
```

Określamy nazwę tabeli SQL jako "products". To nazwa w bazie, która może różnić się od nazwy klasy Pythona.

### L15

```python
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

Pole id: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Klucz główny jednoznacznie identyfikuje rekord; PostgreSQL wygeneruje ID podczas INSERT.

### L16

```python
    name: Mapped[str] = mapped_column(String(100))
```

Pole name: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. String(100) ogranicza tekst do 100 znaków.

### L17

```python
    price: Mapped[int] = mapped_column(Integer)
```

Pole price: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Integer przechowuje liczbę całkowitą; ceny i salda wyrażamy w groszach, żeby uniknąć błędów float.

### L19

```python
    def to_dict(self):
```

Zwykła metoda modelu, bez async: zamieni już dostępne atrybuty self na słownik. Nie wykonuje zapytania SQL.

### L20

```python
        return {"id": self.id, "name": self.name, "price": self.price}
```

self oznacza bieżący produkt. Tworzymy słownik z trzema wartościami, które można zapisać jako JSON. return oddaje go wywołującej funkcji i kończy metodę.

### L22

```python
async def create_product(request):
```

Handler POST odbierze JSON, zwaliduje go, zapisze produkt w transakcji i zwróci JSON ze statusem 201.

### L23

```python
    data = product_fields(await object_json(request))
```

Najpierw await object_json pobiera słownik z żądania. Potem product_fields sprawdza wymagane name i price: nazwę 1–100 znaków oraz nieujemną cenę w groszach typu int. Dopiero poprawny słownik trafia do data.

### L24

```python
    async with request.app[SESSION]() as session:
```

request.app to aplikacja, która odebrała żądanie. [SESSION] pobiera fabrykę; () tworzy nową sesję. async with dopilnuje jej zamknięcia i zwrotu połączenia. Samo wejście nie oznacza zapisu danych.

### L25

```python
        async with session.begin():
```

Rozpoczynamy zakres transakcji. Prawidłowe wyjście zatwierdzi zmiany przez COMMIT; wyjątek opuszczający blok uruchomi ROLLBACK. Wcięcie wskazuje, które instrukcje należą do tej transakcji.

### L26

```python
            product = Product(name=data["name"], price=data["price"])
```

Tworzymy obiekt ORM z wartości ze słownika JSON, np. Notebook i 1299 groszy. To na razie obiekt Pythona, bez rekordu w bazie.

### L27

```python
            session.add(product)
```

Dołączamy obiekt product do sesji. To zwykła metoda bez await: rejestruje plan zapisu w pamięci. INSERT zostanie wykonany podczas flush lub zatwierdzania.

### L28

```python
            await session.flush()
```

flush wysyła oczekujące INSERT/UPDATE do PostgreSQL i czeka na odpowiedź. Nowy obiekt otrzymuje ID. To jeszcze nie COMMIT: późniejszy wyjątek nadal może wycofać tę zmianę.

### L29

```python
            result = product.to_dict()
```

Metoda to_dict kopiuje id, name i price do zwykłego słownika result. Po flush ID już istnieje. Słownik nie zależy od otwartej sesji.

### L30

```python
        event("log", "transaction", "COMMIT: product saved")
```

Rejestrujemy w dzienniku zakończenie transakcji. Wcięcie jest już poza session.begin, dlatego COMMIT nastąpił przed tym komunikatem. To obserwacja, a nie instrukcja wykonująca commit.

### L31

```python
    return web.json_response(result, status=201)
```

Zwracamy odpowiedź JSON z wyrażenia result, status=201. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L33

```python
async def list_products(request):
```

Handler GET pobierze produkty. request daje dostęp do fabryki sesji i parametrów query. Wyniki przekształcimy na listę JSON.

### L34

```python
    async with request.app[SESSION]() as session:
```

request.app to aplikacja, która odebrała żądanie. [SESSION] pobiera fabrykę; () tworzy nową sesję. async with dopilnuje jej zamknięcia i zwrotu połączenia. Samo wejście nie oznacza zapisu danych.

### L35

```python
        statement = select(Product).order_by(Product.id)
```

Budujemy opis SELECT produktów w kolejności ID. Baza jeszcze nie dostała zapytania. order_by zapewnia przewidywalną kolejność rekordów.

### L36

```python
        result = await session.execute(statement)
```

Dopiero execute wysyła przygotowane statement do bazy. await odbiera wynik. result opakowuje wiersze; nie jest jeszcze listą słowników JSON.

### L37

```python
        products = result.scalars().all()
```

Dla select(Product) scalars wyciąga obiekt Product z każdego wiersza, a all zbiera obiekty do listy. Wynik jest już pobrany, więc tutaj nie ma await.

### L38

```python
        return web.json_response([product.to_dict() for product in products])
```

Zwracamy odpowiedź JSON z wyrażenia [product.to_dict() for product in products]. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L40

```python
async def get_product(request):
```

Handler otrzyma ID z URL i pobierze produkt. Brak rekordu zostanie zamieniony na odpowiedź 404, zamiast błędu atrybutu None.

### L41

```python
    product_id = positive_id(request.match_info["id"])
```

Router zapisał fragment {id} jako tekst, np. "1". positive_id zamienia go na dodatni int i odrzuca błędne dane statusem 400. product_id będzie użyty w zapytaniu do bazy.

### L42

```python
    async with request.app[SESSION]() as session:
```

request.app to aplikacja, która odebrała żądanie. [SESSION] pobiera fabrykę; () tworzy nową sesję. async with dopilnuje jej zamknięcia i zwrotu połączenia. Samo wejście nie oznacza zapisu danych.

### L43

```python
        product = await session.get(Product, product_id)
```

Pobieramy Product po kluczu głównym. await czeka na odczyt bazy, dając pętli możliwość obsługi innych zadań. Wynik to obiekt Product albo None.

### L44

```python
        if product is None:
```

None oznacza brak produktu. Tylko wtedy wejdziemy do gałęzi 404.

### L45

```python
            raise web.HTTPNotFound(text="Product not found")
```

Przerywamy handler wyjątkiem HTTPNotFound. aiohttp zamieni go na odpowiedź HTTP 404 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L46

```python
        return web.json_response(product.to_dict())
```

Zwracamy odpowiedź JSON z wyrażenia product.to_dict(). json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L48

```python
async def update_product(request):
```

Handler PATCH zmieni tylko przesłane pola. Odczyt i zapis należą do jednej transakcji.

### L49

```python
    product_id = positive_id(request.match_info["id"])
```

Router zapisał fragment {id} jako tekst, np. "1". positive_id zamienia go na dodatni int i odrzuca błędne dane statusem 400. product_id będzie użyty w zapytaniu do bazy.

### L50

```python
    data = product_fields(await object_json(request), partial=True)
```

Czytamy słownik i walidujemy częściową zmianę. partial=True pozwala przesłać samo name lub samo price. Pola nieobecne w JSON zachowają dotychczasowe wartości.

### L51

```python
    async with request.app[SESSION]() as session:
```

request.app to aplikacja, która odebrała żądanie. [SESSION] pobiera fabrykę; () tworzy nową sesję. async with dopilnuje jej zamknięcia i zwrotu połączenia. Samo wejście nie oznacza zapisu danych.

### L52

```python
        async with session.begin():
```

Rozpoczynamy zakres transakcji. Prawidłowe wyjście zatwierdzi zmiany przez COMMIT; wyjątek opuszczający blok uruchomi ROLLBACK. Wcięcie wskazuje, które instrukcje należą do tej transakcji.

### L53

```python
            product = await session.get(Product, product_id)
```

Pobieramy Product po kluczu głównym. await czeka na odczyt bazy, dając pętli możliwość obsługi innych zadań. Wynik to obiekt Product albo None.

### L54

```python
            if product is None:
```

None oznacza brak produktu. Tylko wtedy wejdziemy do gałęzi 404.

### L55

```python
                raise web.HTTPNotFound(text="Product not found")
```

Przerywamy handler wyjątkiem HTTPNotFound. aiohttp zamieni go na odpowiedź HTTP 404 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L56

```python
            if "name" in data:
```

Sprawdzamy obecność klucza name; nieobecna nazwa pozostanie bez zmian.

### L57

```python
                product.name = data["name"]
```

Zmieniamy atrybut obiektu śledzonego przez sesję. SQLAlchemy wykryje tę zmianę i przygotuje UPDATE podczas flush lub commit.

### L58

```python
            if "price" in data:
```

Sprawdzamy obecność klucza, więc również price=0 zostanie poprawnie zaktualizowane.

### L59

```python
                product.price = data["price"]
```

Przypisujemy nową cenę w groszach, np. 999. Nie mnożymy ani nie dzielimy jej przez 100; baza również przechowuje liczbę całkowitą.

### L60

```python
            await session.flush()
```

flush wysyła oczekujące INSERT/UPDATE do PostgreSQL i czeka na odpowiedź. Nowy obiekt otrzymuje ID. To jeszcze nie COMMIT: późniejszy wyjątek nadal może wycofać tę zmianę.

### L61

```python
            result = product.to_dict()
```

Metoda to_dict kopiuje id, name i price do zwykłego słownika result. Po flush ID już istnieje. Słownik nie zależy od otwartej sesji.

### L62

```python
    return web.json_response(result)
```

Zwracamy odpowiedź JSON z wyrażenia result. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L64

```python
async def main():
```

Czytaj przebieg: __main__ → launch → asyncio.run(main()) → przygotowanie aplikacji i tras → demo → klient HTTP → router → handler → odpowiedź → dziennik klienta. W zadaniach z bazą database(Base) przygotowuje fabrykę; handler tworzy własną sesję. Definicja handlera pojawia się wcześniej w pliku, ale jego ciało rusza dopiero po żądaniu. W zadaniu 18 main sam wysyła dwa żądania, aby pokazać ich nakładanie.

### L64

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L65

```python
    async with database(Base) as factory:
```

Wchodzimy do pomocnika database z api_support.py. Tworzy osobny schemat w bazie lesson32, tabele z Base.metadata i fabrykę AsyncSession. Przy wyjściu usuwa tylko schemat tego pokazu i zamyka silniki. To przygotowanie demonstracji, a nie kod handlera.

### L66

```python
        app = web.Application()
```

Tworzymy aplikację aiohttp. Przechowa router i stan; ta linia jeszcze nie otwiera portu ani nie obsługuje żądania.

### L67

```python
        app[SESSION] = factory
```

Pod kluczem SESSION zapisujemy fabrykę sesji, nie jedną wspólną sesję. Każdy handler utworzy własną AsyncSession, więc równoległe żądania nie dzielą transakcji.

### L68

```python
        app.router.add_post("/products", create_product)
```

Rejestrujemy POST /products → create_product. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L69

```python
        app.router.add_get("/products", list_products)
```

Rejestrujemy GET /products → list_products. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L70

```python
        app.router.add_get("/products/{id}", get_product)
```

Rejestrujemy GET /products/{id} → get_product. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L71

```python
        app.router.add_patch("/products/{id}", update_product)
```

Rejestrujemy PATCH /products/{id} → update_product. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L72

```python
        await demo(app, [
```

Uruchamiamy pomocnika pokazu: startuje prawdziwy serwer na wolnym porcie, klient wysyła wymienione żądania po kolei i porównuje statusy z oczekiwaniami. Każda krotka to (metoda, ścieżka, JSON, oczekiwany status). Dziennik pokazuje również body. Po pokazie serwer jest zamykany.

### L73

```python
            ('POST', '/products', {'name': 'Notebook', 'price': 1299}, 201),
```

Przypadek pokazu: POST /products. Body: {'name': 'Notebook', 'price': 1299}; None oznacza brak danych. Oczekujemy statusu 201. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L74

```python
            ('GET', '/products', None, 200),
```

Przypadek pokazu: GET /products. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L75

```python
            ('GET', '/products/1', None, 200),
```

Przypadek pokazu: GET /products/1. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L76

```python
            ('GET', '/products/999', None, 404),
```

Przypadek pokazu: GET /products/999. Body: None; None oznacza brak danych. Oczekujemy statusu 404. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L77

```python
            ('PATCH', '/products/1', {'price': 999}, 200),
```

Przypadek pokazu: PATCH /products/1. Body: {'price': 999}; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L78

```python
            ('GET', '/products/1', None, 200),
```

Przypadek pokazu: GET /products/1. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L79

```python
        ])
```

Zamykamy listę przypadków ] i wywołanie demo ). To kontynuacja poprzedniej instrukcji, a nie osobne działanie. await zaczeka na cały pokaz.

### L81

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L82

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Czy price=0 powinno być pominięte?

<details><summary>Odpowiedź</summary>

Nie. Sprawdzamy obecność klucza, a nie prawdziwość wartości.

</details>
