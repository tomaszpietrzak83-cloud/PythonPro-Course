# Zadanie 05: Query string i brak parametru

Query to parametry po znaku ?; get pozwala rozpoznać brak klucza.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

?q=python → 200 z frazą; brak q → 400. Pusty q jest obecnym parametrem.

## Pełny kod

```python
import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

async def search(request):
    query = request.query.get("q")
    if query is None:
        return web.json_response({"error": "Missing q parameter"}, status=400)
    return web.json_response({"search_query": query})

async def main():
    app = web.Application()
    app.router.add_get("/api/search", search)
    await demo(app, [
        ('GET', '/api/search?q=python', None, 200),
        ('GET', '/api/search', None, 400),
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
async def search(request):
```

Handler wyszukiwania odczyta q z query string, np. /api/search?q=python. Brak parametru obsłuży osobną gałęzią.

### L7

```python
    query = request.query.get("q")
```

Z query string odczytujemy q. Dla ?q=python dostaniemy "python"; bez q metoda get zwróci None, zamiast zgłosić KeyError. ?q= daje pusty tekst.

### L8

```python
    if query is None:
```

Sprawdzamy brak q, nie pusty napis. ?q= i brak q to różne wejścia.

### L9

```python
        return web.json_response({"error": "Missing q parameter"}, status=400)
```

Zwracamy odpowiedź JSON z wyrażenia {"error": "Missing q parameter"}, status=400. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L10

```python
    return web.json_response({"search_query": query})
```

Zwracamy odpowiedź JSON z wyrażenia {"search_query": query}. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L12

```python
async def main():
```

Czytaj przebieg: __main__ → launch → asyncio.run(main()) → przygotowanie aplikacji i tras → demo → klient HTTP → router → handler → odpowiedź → dziennik klienta. W zadaniach z bazą database(Base) przygotowuje fabrykę; handler tworzy własną sesję. Definicja handlera pojawia się wcześniej w pliku, ale jego ciało rusza dopiero po żądaniu. W zadaniu 18 main sam wysyła dwa żądania, aby pokazać ich nakładanie.

### L12

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L13

```python
    app = web.Application()
```

Tworzymy aplikację aiohttp. Przechowa router i stan; ta linia jeszcze nie otwiera portu ani nie obsługuje żądania.

### L14

```python
    app.router.add_get("/api/search", search)
```

Rejestrujemy GET /api/search → search. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L15

```python
    await demo(app, [
```

Uruchamiamy pomocnika pokazu: startuje prawdziwy serwer na wolnym porcie, klient wysyła wymienione żądania po kolei i porównuje statusy z oczekiwaniami. Każda krotka to (metoda, ścieżka, JSON, oczekiwany status). Dziennik pokazuje również body. Po pokazie serwer jest zamykany.

### L16

```python
        ('GET', '/api/search?q=python', None, 200),
```

Przypadek pokazu: GET /api/search?q=python. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L17

```python
        ('GET', '/api/search', None, 400),
```

Przypadek pokazu: GET /api/search. Body: None; None oznacza brak danych. Oczekujemy statusu 400. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L18

```python
    ])
```

Zamykamy listę przypadków ] i wywołanie demo ). To kontynuacja poprzedniej instrukcji, a nie osobne działanie. await zaczeka na cały pokaz.

### L20

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L21

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Czym różni się brak q od ?q=?

<details><summary>Odpowiedź</summary>

Brak daje None, a obecny pusty parametr daje pusty tekst.

</details>
