# Zadanie 06: POST i echo JSON

Body to osobna część requestu. await request.json odbiera je i parsuje.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

POST z message: Python zwraca tę samą strukturę JSON.

## Pełny kod

```python
import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

import json

async def echo(request):
    try:
        data = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise web.HTTPBadRequest(text="Invalid JSON")
    return web.json_response(data)

async def main():
    app = web.Application()
    app.router.add_post("/api/echo", echo)
    await demo(app, [
        ('POST', '/api/echo', {'message': 'Python'}, 200),
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
import json
```

Import z json udostępnia narzędzia związane z dekodowaniem JSON i rozpoznawaniem JSONDecodeError. Import nie uruchamia main ani nie wysyła żądania.

### L8

```python
async def echo(request):
```

Handler odczyta body JSON i odeśle tę samą strukturę jako JSON. To nie jest drukowanie do terminala.

### L9

```python
    try:
```

Początek bloku obsługi błędu JSON. Jeśli parsowanie zawiedzie, wykonanie przejdzie do pasującego except; prawidłowe dane przejdą dalej.

### L10

```python
        data = await request.json()
```

Czekamy na ciało żądania i parsujemy JSON do obiektu Pythona. Przykład {"message":"Python"} staje się słownikiem. Niepoprawny JSON przechodzi do except.

### L11

```python
    except (json.JSONDecodeError, UnicodeDecodeError):
```

Przechwytujemy wyłącznie błędy dekodowania JSON i kodowania znaków. Zamienimy je na 400. Inne błędy programowania nie zostają ukryte szerokim except Exception.

### L12

```python
        raise web.HTTPBadRequest(text="Invalid JSON")
```

Przerywamy handler wyjątkiem HTTPBadRequest. aiohttp zamieni go na odpowiedź HTTP 400 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L13

```python
    return web.json_response(data)
```

Zwracamy odpowiedź JSON z wyrażenia data. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L15

```python
async def main():
```

Czytaj przebieg: __main__ → launch → asyncio.run(main()) → przygotowanie aplikacji i tras → demo → klient HTTP → router → handler → odpowiedź → dziennik klienta. W zadaniach z bazą database(Base) przygotowuje fabrykę; handler tworzy własną sesję. Definicja handlera pojawia się wcześniej w pliku, ale jego ciało rusza dopiero po żądaniu. W zadaniu 18 main sam wysyła dwa żądania, aby pokazać ich nakładanie.

### L15

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L16

```python
    app = web.Application()
```

Tworzymy aplikację aiohttp. Przechowa router i stan; ta linia jeszcze nie otwiera portu ani nie obsługuje żądania.

### L17

```python
    app.router.add_post("/api/echo", echo)
```

Rejestrujemy POST /api/echo → echo. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L18

```python
    await demo(app, [
```

Uruchamiamy pomocnika pokazu: startuje prawdziwy serwer na wolnym porcie, klient wysyła wymienione żądania po kolei i porównuje statusy z oczekiwaniami. Każda krotka to (metoda, ścieżka, JSON, oczekiwany status). Dziennik pokazuje również body. Po pokazie serwer jest zamykany.

### L19

```python
        ('POST', '/api/echo', {'message': 'Python'}, 200),
```

Przypadek pokazu: POST /api/echo. Body: {'message': 'Python'}; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L20

```python
    ])
```

Zamykamy listę przypadków ] i wywołanie demo ). To kontynuacja poprzedniej instrukcji, a nie osobne działanie. await zaczeka na cały pokaz.

### L22

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L23

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Co się stanie przy uszkodzonym JSON?

<details><summary>Odpowiedź</summary>

JSONDecodeError trafia do except i odpowiedzi 400.

</details>
