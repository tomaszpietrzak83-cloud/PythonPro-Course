# Lesson 32 - Zadania

## TASK 01 - Kalkulator opóźnień (proste)

Napisz główną korutynę `main`, która uruchomi 3 symulowane zadania `asyncio.sleep` z opóźnieniami:

- 1 sekunda,
- 4 sekundy,
- 2 sekundy.

Użyj:

```python
asyncio.gather()
```

Program powinien wypisać całkowity czas wykonania. Powinien być bliski 4 sekund.

## TASK 02 - Aiohttp: strona powitalna (proste)

Stwórz prosty serwer `aiohttp`, który na ścieżce `/` zwróci odpowiedź `web.Response` z tekstem:

```html
<h1>Witaj na mojej stronie!</h1>
```

Ustaw poprawny typ odpowiedzi:

```python
content_type="text/html"
```

## TASK 03 - Aiohttp: dynamiczne powitanie (proste)

Rozbuduj serwer z zadania 2.

Dodaj handler na ścieżce:

```text
/witaj/{imie}
```

Handler ma odczytać `imie` z `request.match_info` i zwrócić tekst:

```text
Witaj, {imie}!
```

## TASK 04 - Aiohttp: proste API JSON (proste)

Stwórz handler na ścieżce:

```text
/api/status
```

Metodą `GET` zwróć odpowiedź JSON:

```json
{
  "status": "OK",
  "server_time": "..."
}
```

Użyj:

```python
datetime.now()
web.json_response()
```

## TASK 05 - Aiohttp: odczyt query params (proste)

Stwórz handler:

```text
/api/search
```

Handler ma odczytać z `request.query` parametr `q`.

Jeśli parametr istnieje, zwróć:

```json
{
  "szukana_fraza": "wartosc_q"
}
```

Jeśli parametru nie ma, zwróć:

```json
{
  "błąd": "Brak parametru q"
}
```

## TASK 06 - Aiohttp: odczyt JSON, echo (proste)

Stwórz handler `POST` na ścieżce:

```text
/api/echo
```

Handler ma:

- odczytać dane JSON wysłane w ciele requestu przez `await request.json()`,
- odesłać te dane z powrotem przez `web.json_response`.

## TASK 07 - SQLAlchemy Async: definicja modelu (proste)

Zdefiniuj model `Product`, używając `DeclarativeBase` z SQLAlchemy.

Model powinien mieć pola:

- `id` - `int`, klucz główny,
- `name` - `String(100)`,
- `price` - `Integer`, przechowujący cenę w groszach.

## TASK 08 - Aiohttp: obsługa błędu (proste)

W handlerze z zadania 3, czyli `/witaj/{imie}`, dodaj sprawdzenie.

Jeśli `imie` to:

```text
admin
```

podnieś wyjątek:

```python
raise web.HTTPForbidden(text="Dostęp dla admina zabroniony")
```

## TASK 09 - CRUD API: produkty, POST (challenge)

Używając aplikacji z przykładu z integracją SQLAlchemy:

1. Dodaj model `Product` z zadania 7.
2. Pamiętaj o dodaniu go do `Base.metadata.create_all`.
3. Stwórz handler `POST` na `/products`.
4. Handler ma odczytać `name` i `price` z JSON.
5. Handler ma stworzyć nowy obiekt `Product` i zapisać go w bazie.
6. Handler powinien zwrócić dane nowego produktu wraz z ID i statusem `201`.

## TASK 10 - CRUD API: produkty, GET lista (challenge)

Bazując na zadaniu 9, stwórz handler `GET` na:

```text
/products
```

Handler ma pobrać wszystkie produkty z bazy danych:

```python
select(Product)
```

Zwróć produkty jako listę obiektów JSON.

## TASK 11 - CRUD API: produkty, GET pojedynczy (challenge)

Bazując na zadaniu 10, stwórz handler `GET` na:

```text
/products/{id}
```

Handler ma:

- pobrać ID z `match_info`,
- znaleźć produkt w bazie,
- zwrócić dane produktu jako JSON, jeśli istnieje,
- podnieść `web.HTTPNotFound()`, jeśli produktu nie ma.

Przykład zapytania:

```python
select(Product).where(Product.id == product_id)
```

## TASK 12 - Aiohttp klient: publiczne API (challenge)

`aiohttp` to także klient HTTP.

Napisz osobny skrypt `.py`, a nie serwer.

W korutynie `main`:

1. Stwórz `aiohttp.ClientSession()`.
2. Wykonaj zapytanie `GET` na publiczne API:

```text
https://api.coindesk.com/v1/bpi/currentprice.json
```

3. Pobierz odpowiedź JSON przez `await response.json()`.
4. Wypisz w konsoli cenę Bitcoina w USD.

Wskazówka:

```python
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()
```

<p style="color:red"><strong>Komentarz mentora:</strong> Ten endpoint CoinDesk może być niedostępny lub niestabilny. Jeśli nie działa, zachowaj sens zadania i użyj innego publicznego endpointu JSON, bo celem jest przećwiczenie `aiohttp.ClientSession`, a nie konkretnego API Bitcoina.</p>

## TASK 13 - Aiohttp klient: gather (challenge)

Rozbuduj zadanie 12.

Napisz korutynę:

```python
fetch(session, url)
```

która pobiera dane.

W `main` stwórz listę 3 różnych URL-i, na przykład:

```text
https://api.publicapis.org/random?auth=null
```

Wywołaj je 3 razy i użyj `asyncio.gather`, aby pobrać wszystkie jednocześnie.

## TASK 14 - CRUD API: produkty, PUT/PATCH (challenge)

Bazując na zadaniu 11, stwórz handler `PUT` albo `PATCH` na:

```text
/products/{id}
```

Handler ma:

1. Pobrać produkt i zwrócić `404`, jeśli go nie ma.
2. Odczytać nowe dane `name` i/lub `price` z `await request.json()`.
3. Zaktualizować atrybuty produktu.
4. Zapisać zmiany w bazie w ramach sesji i transakcji.
5. Zwrócić zaktualizowane dane produktu.

## TASK 15 - CRUD API: produkty, DELETE (challenge)

Bazując na zadaniu 11, stwórz handler `DELETE` na:

```text
/products/{id}
```

Handler ma:

- pobrać produkt,
- usunąć go przez `await session.delete(product)`,
- zwrócić pustą odpowiedź ze statusem `204 No Content`.

## TASK 16 - SQLAlchemy Async: transakcja (challenge)

Stwórz dwa modele:

- `Account`,
- drugi model według potrzeb projektu.

Model `Account` powinien mieć pole:

```python
balance: Mapped[int]
```

Stwórz handler `POST`:

```text
/transfer
```

Handler ma przyjąć JSON:

```json
{
  "from_id": 1,
  "to_id": 2,
  "amount": 100
}
```

W ramach jednej transakcji:

```python
async with session.begin():
```

1. Pobierz oba konta.
2. Sprawdź, czy na koncie `from_id` jest wystarczająco środków.
3. Odejmij `amount` z `from_id`.
4. Dodaj `amount` do `to_id`.
5. Jeśli coś pójdzie nie tak, transakcja powinna zostać wycofana.

## TASK 17 - Aiohttp: paginacja (challenge)

Zmodyfikuj handler `GET /products` z zadania 10.

Handler ma przyjmować z `request.query`:

- `page`, domyślnie `1`,
- `limit`, domyślnie `10`.

Zmodyfikuj zapytanie SQLAlchemy, aby użyć:

```python
offset()
limit()
```

Wzór:

```python
offset = (page - 1) * limit
```

## TASK 18 - Aiohttp: Mock API dla AI (challenge)

Stwórz handler `POST` na:

```text
/api/v1/chat
```

Handler ma:

1. Oczekiwać JSON-a:

```json
{
  "prompt": "jakaś treść"
}
```

2. Symulować długie przetwarzanie przez AI:

```python
await asyncio.sleep(3)
```

3. Zwrócić odpowiedź JSON:

```json
{
  "response": "Otrzymałem twój prompt: '...' i przetworzyłem go."
}
```

To ćwiczenie pokazuje, jak serwer `aiohttp` radzi sobie z długimi zadaniami I/O, nie blokując innych zapytań.

## TASK 19 - Refaktoryzacja: organizacja tras (challenge)

Zamiast dodawać wszystkie trasy w `create_app()`, stwórz osobną funkcję:

```python
setup_routes(app)
```

Umieść ją w osobnym pliku:

```text
routes.py
```

Zaimportuj ją i wywołaj w `create_app`.

To poprawia czytelność większych projektów.

## TASK 20 - SQLAlchemy Async: JOIN (challenge)

Dodaj do modelu `Product` relację `ForeignKey` do `User`, czyli twórcy produktu.

Zmodyfikuj handler:

```text
GET /products/{id}
```

Handler ma pobierać produkt wraz z nazwą użytkownika, który go stworzył.

Możesz użyć:

```python
select(Product, User).join(User)
```

albo, w trudniejszej wersji:

```python
options(joinedload(Product.user))
```
