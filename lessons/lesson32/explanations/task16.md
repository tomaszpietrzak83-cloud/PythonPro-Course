# Zadanie 16: Przelew, blokady i rollback

Jedna transakcja obejmuje oba salda i historię. FOR UPDATE chroni wiersze przed równoległą zmianą.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

100 groszy: salda 900 i 600. Próba 13 po flush kończy się 409; salda nadal 900 i 600. 9999 również daje 409.

## Pełny kod

```python
import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from api_support import SESSION, database, object_json

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    balance: Mapped[int] = mapped_column(Integer)

class Transfer(Base):
    __tablename__ = "transfers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

async def transfer(request):
    data = await object_json(request)
    if set(data) != {"from_id", "to_id", "amount"}:
        raise web.HTTPBadRequest(text="from_id, to_id and amount required")
    if any(type(data[key]) is not int or not 1 <= data[key] <= 2147483647 for key in data):
        raise web.HTTPBadRequest(text="Use positive integers")
    if data["from_id"] == data["to_id"]:
        raise web.HTTPBadRequest(text="Accounts must differ")
    async with request.app[SESSION]() as session:
        async with session.begin():
            statement = select(Account).where(Account.id.in_([data["from_id"], data["to_id"]])).order_by(Account.id).with_for_update()
            accounts = (await session.execute(statement)).scalars().all()
            by_id = {account.id: account for account in accounts}
            if len(by_id) != 2:
                raise web.HTTPNotFound(text="Account not found")
            source = by_id[data["from_id"]]
            target = by_id[data["to_id"]]
            if source.balance < data["amount"]:
                raise web.HTTPConflict(text="Insufficient balance; transaction rolled back")
            source.balance -= data["amount"]
            await session.flush()
            if data["amount"] == 13:
                raise web.HTTPConflict(text="Demo failure after debit; transaction rolled back")
            target.balance += data["amount"]
            session.add(Transfer(description=f"Transfer {data['amount']} cents"))
    return web.json_response({"transferred": data["amount"]})

async def balances(request):
    async with request.app[SESSION]() as session:
        accounts = (await session.execute(select(Account).order_by(Account.id))).scalars().all()
        return web.json_response({str(account.id): account.balance for account in accounts})

async def main():
    async with database(Base) as factory:
        async with factory.begin() as session:
            session.add_all([Account(id=1, balance=1000), Account(id=2, balance=500)])
        app = web.Application()
        app[SESSION] = factory
        app.router.add_post("/transfer", transfer)
        app.router.add_get("/balances", balances)
        await demo(app, [
            ("POST", "/transfer", {"from_id": 1, "to_id": 2, "amount": 100}, 200),
            ("GET", "/balances", None, 200),
            ("POST", "/transfer", {"from_id": 1, "to_id": 2, "amount": 13}, 409),
            ("GET", "/balances", None, 200),
            ("POST", "/transfer", {"from_id": 1, "to_id": 2, "amount": 9999}, 409),
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
from api_support import SESSION, database, object_json
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
class Account(Base):
```

Definiujemy klasę Account. Dziedziczy po Base, więc SQLAlchemy zarejestruje jej tabelę. Sama definicja klasy jeszcze nie tworzy tabeli w PostgreSQL.

### L14

```python
    __tablename__ = "accounts"
```

Określamy nazwę tabeli SQL jako "accounts". To nazwa w bazie, która może różnić się od nazwy klasy Pythona.

### L15

```python
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

Pole id: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Klucz główny jednoznacznie identyfikuje rekord; PostgreSQL wygeneruje ID podczas INSERT.

### L16

```python
    balance: Mapped[int] = mapped_column(Integer)
```

Pole balance: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Integer przechowuje liczbę całkowitą; ceny i salda wyrażamy w groszach, żeby uniknąć błędów float.

### L18

```python
class Transfer(Base):
```

Definiujemy klasę Transfer. Dziedziczy po Base, więc SQLAlchemy zarejestruje jej tabelę. Sama definicja klasy jeszcze nie tworzy tabeli w PostgreSQL.

### L19

```python
    __tablename__ = "transfers"
```

Określamy nazwę tabeli SQL jako "transfers". To nazwa w bazie, która może różnić się od nazwy klasy Pythona.

### L20

```python
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

Pole id: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. Klucz główny jednoznacznie identyfikuje rekord; PostgreSQL wygeneruje ID podczas INSERT.

### L21

```python
    description: Mapped[str] = mapped_column(String(100))
```

Pole description: Mapped opisuje typ atrybutu ORM, mapped_column definiuje kolumnę SQL. String(100) ogranicza tekst do 100 znaków.

### L23

```python
async def transfer(request):
```

Handler przelewu waliduje wejście i zmienia dwa salda atomowo. Blokady wierszy chronią odczyt sald przed równoczesnymi przelewami.

### L24

```python
    data = await object_json(request)
```

Pomocnik czyta JSON i sprawdza, czy wynikiem jest słownik. Zwraca go do data. Niepoprawny JSON lub lista zamiast obiektu kończą żądanie statusem 400.

### L25

```python
    if set(data) != {"from_id", "to_id", "amount"}:
```

Porównujemy zestaw kluczy JSON z trzema wymaganymi polami; brakujące i dodatkowe klucze są błędem.

### L26

```python
        raise web.HTTPBadRequest(text="from_id, to_id and amount required")
```

Przerywamy handler wyjątkiem HTTPBadRequest. aiohttp zamieni go na odpowiedź HTTP 400 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L27

```python
    if any(type(data[key]) is not int or not 1 <= data[key] <= 2147483647 for key in data):
```

any sprawdza wszystkie wartości wejścia: dodatnie int w zakresie PostgreSQL Integer. type(... ) is int odrzuca także bool, mimo że bool dziedziczy po int.

### L28

```python
        raise web.HTTPBadRequest(text="Use positive integers")
```

Przerywamy handler wyjątkiem HTTPBadRequest. aiohttp zamieni go na odpowiedź HTTP 400 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L29

```python
    if data["from_id"] == data["to_id"]:
```

Przelew na to samo konto nie ma sensu w tym ćwiczeniu, więc odrzucamy go statusem 400.

### L30

```python
        raise web.HTTPBadRequest(text="Accounts must differ")
```

Przerywamy handler wyjątkiem HTTPBadRequest. aiohttp zamieni go na odpowiedź HTTP 400 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L31

```python
    async with request.app[SESSION]() as session:
```

request.app to aplikacja, która odebrała żądanie. [SESSION] pobiera fabrykę; () tworzy nową sesję. async with dopilnuje jej zamknięcia i zwrotu połączenia. Samo wejście nie oznacza zapisu danych.

### L32

```python
        async with session.begin():
```

Rozpoczynamy zakres transakcji. Prawidłowe wyjście zatwierdzi zmiany przez COMMIT; wyjątek opuszczający blok uruchomi ROLLBACK. Wcięcie wskazuje, które instrukcje należą do tej transakcji.

### L33

```python
            statement = select(Account).where(Account.id.in_([data["from_id"], data["to_id"]])).order_by(Account.id).with_for_update()
```

Wybieramy oba konta i żądamy blokady FOR UPDATE na czas transakcji. Inny przelew poczeka na te wiersze. order_by(ID) narzuca zgodną kolejność blokowania, zmniejszając ryzyko zakleszczeń.

### L34

```python
            accounts = (await session.execute(statement)).scalars().all()
```

Wykonujemy zapytanie blokujące wiersze kont. Po await wyciągamy obiekty Account do listy. Jeśli inna transakcja trzyma blokadę, oczekiwanie nie blokuje całej pętli zdarzeń.

### L35

```python
            by_id = {account.id: account for account in accounts}
```

Tworzymy słownik przez comprehension: kluczem jest ID, wartością obiekt Account. Dzięki temu wybierzemy konto źródłowe i docelowe po ID, niezależnie od kolejności przesłanej w JSON.

### L36

```python
            if len(by_id) != 2:
```

Potrzebujemy dokładnie dwóch istniejących kont; brak któregokolwiek to 404.

### L37

```python
                raise web.HTTPNotFound(text="Account not found")
```

Przerywamy handler wyjątkiem HTTPNotFound. aiohttp zamieni go na odpowiedź HTTP 404 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L38

```python
            source = by_id[data["from_id"]]
```

Ze słownika kont pobieramy obiekt konta źródłowego. Przy from_id=1 to konto z początkowym saldem 1000 groszy.

### L39

```python
            target = by_id[data["to_id"]]
```

Pobieramy konto odbiorcy. Dla to_id=2 początkowe saldo wynosi 500 groszy. source i target są różnymi obiektami.

### L40

```python
            if source.balance < data["amount"]:
```

Kwota większa od dostępnego salda zostanie odrzucona przed zmianą sald.

### L41

```python
                raise web.HTTPConflict(text="Insufficient balance; transaction rolled back")
```

Przerywamy handler wyjątkiem HTTPConflict. aiohttp zamieni go na odpowiedź HTTP 409 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L42

```python
            source.balance -= data["amount"]
```

Odejmujemy kwotę od salda źródła w obiekcie ORM. Dla przelewu 100: 1000 → 900. Następny flush wyśle UPDATE, ale zmiana nadal należy do niezatwierdzonej transakcji.

### L43

```python
            await session.flush()
```

flush wysyła oczekujące INSERT/UPDATE do PostgreSQL i czeka na odpowiedź. Nowy obiekt otrzymuje ID. To jeszcze nie COMMIT: późniejszy wyjątek nadal może wycofać tę zmianę.

### L44

```python
            if data["amount"] == 13:
```

To jawnie edukacyjny punkt awarii: kwota 13 wywoła błąd po odjęciu i flush, ale przed dodaniem odbiorcy. Pozwala sprawdzić prawdziwy rollback zapisu. Taka specjalna kwota nie należy do reguł zwykłej aplikacji.

### L45

```python
                raise web.HTTPConflict(text="Demo failure after debit; transaction rolled back")
```

Przerywamy handler wyjątkiem HTTPConflict. aiohttp zamieni go na odpowiedź HTTP 409 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L46

```python
            target.balance += data["amount"]
```

Dodajemy tę samą kwotę odbiorcy: 500 → 600 dla przelewu 100. Obie zmiany zatwierdzą się razem. Suma sald pozostaje 1500.

### L47

```python
            session.add(Transfer(description=f"Transfer {data['amount']} cents"))
```

Dodajemy wpis historii przelewu w tej samej transakcji co salda. Jeśli zapis historii zawiedzie, zmiany sald również zostaną wycofane.

### L48

```python
    return web.json_response({"transferred": data["amount"]})
```

Zwracamy odpowiedź JSON z wyrażenia {"transferred": data["amount"]}. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L50

```python
async def balances(request):
```

Handler kontrolny odczyta salda bez ich zmieniania. Użyjemy go przed i po błędzie, aby potwierdzić rollback.

### L51

```python
    async with request.app[SESSION]() as session:
```

request.app to aplikacja, która odebrała żądanie. [SESSION] pobiera fabrykę; () tworzy nową sesję. async with dopilnuje jej zamknięcia i zwrotu połączenia. Samo wejście nie oznacza zapisu danych.

### L52

```python
        accounts = (await session.execute(select(Account).order_by(Account.id))).scalars().all()
```

Odczytujemy konta po zatwierdzonym przelewie albo rollbacku. scalars().all() daje listę Account uporządkowaną według ID; ten odczyt sprawdza rzeczywisty stan bazy.

### L53

```python
        return web.json_response({str(account.id): account.balance for account in accounts})
```

Zwracamy odpowiedź JSON z wyrażenia {str(account.id): account.balance for account in accounts}. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L55

```python
async def main():
```

Czytaj przebieg: __main__ → launch → asyncio.run(main()) → przygotowanie aplikacji i tras → demo → klient HTTP → router → handler → odpowiedź → dziennik klienta. W zadaniach z bazą database(Base) przygotowuje fabrykę; handler tworzy własną sesję. Definicja handlera pojawia się wcześniej w pliku, ale jego ciało rusza dopiero po żądaniu. W zadaniu 18 main sam wysyła dwa żądania, aby pokazać ich nakładanie.

### L55

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L56

```python
    async with database(Base) as factory:
```

Wchodzimy do pomocnika database z api_support.py. Tworzy osobny schemat w bazie lesson32, tabele z Base.metadata i fabrykę AsyncSession. Przy wyjściu usuwa tylko schemat tego pokazu i zamyka silniki. To przygotowanie demonstracji, a nie kod handlera.

### L57

```python
        async with factory.begin() as session:
```

Fabryka tworzy sesję i rozpoczyna transakcję do przygotowania danych. Przy poprawnym wyjściu zapisze rekordy, a następnie zamknie sesję; wyjątek spowoduje rollback.

### L58

```python
            session.add_all([Account(id=1, balance=1000), Account(id=2, balance=500)])
```

Przygotowujemy dwa konta: 1 → 1000 i 2 → 500 groszy. add_all rejestruje listę nowych obiektów bez await. Wyjście z factory.begin zapisze oba.

### L59

```python
        app = web.Application()
```

Tworzymy aplikację aiohttp. Przechowa router i stan; ta linia jeszcze nie otwiera portu ani nie obsługuje żądania.

### L60

```python
        app[SESSION] = factory
```

Pod kluczem SESSION zapisujemy fabrykę sesji, nie jedną wspólną sesję. Każdy handler utworzy własną AsyncSession, więc równoległe żądania nie dzielą transakcji.

### L61

```python
        app.router.add_post("/transfer", transfer)
```

Rejestrujemy POST /transfer → transfer. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L62

```python
        app.router.add_get("/balances", balances)
```

Rejestrujemy GET /balances → balances. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L63

```python
        await demo(app, [
```

Uruchamiamy pomocnika pokazu: startuje prawdziwy serwer na wolnym porcie, klient wysyła wymienione żądania po kolei i porównuje statusy z oczekiwaniami. Każda krotka to (metoda, ścieżka, JSON, oczekiwany status). Dziennik pokazuje również body. Po pokazie serwer jest zamykany.

### L64

```python
            ("POST", "/transfer", {"from_id": 1, "to_id": 2, "amount": 100}, 200),
```

Przypadek pokazu: POST /transfer. Body: {'from_id': 1, 'to_id': 2, 'amount': 100}; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L65

```python
            ("GET", "/balances", None, 200),
```

Przypadek pokazu: GET /balances. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L66

```python
            ("POST", "/transfer", {"from_id": 1, "to_id": 2, "amount": 13}, 409),
```

Przypadek pokazu: POST /transfer. Body: {'from_id': 1, 'to_id': 2, 'amount': 13}; None oznacza brak danych. Oczekujemy statusu 409. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L67

```python
            ("GET", "/balances", None, 200),
```

Przypadek pokazu: GET /balances. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L68

```python
            ("POST", "/transfer", {"from_id": 1, "to_id": 2, "amount": 9999}, 409),
```

Przypadek pokazu: POST /transfer. Body: {'from_id': 1, 'to_id': 2, 'amount': 9999}; None oznacza brak danych. Oczekujemy statusu 409. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L69

```python
        ])
```

Zamykamy listę przypadków ] i wywołanie demo ). To kontynuacja poprzedniej instrukcji, a nie osobne działanie. await zaczeka na cały pokaz.

### L71

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L72

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Po co awaria po flush, zamiast przed zmianą?

<details><summary>Odpowiedź</summary>

Pokazuje, że rollback wycofuje SQL już wykonany w bazie, nie tylko obiekty w pamięci.

</details>
