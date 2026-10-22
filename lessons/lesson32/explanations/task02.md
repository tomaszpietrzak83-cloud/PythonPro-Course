# Zadanie 02: Pierwszy serwer HTML

Handler to funkcja otrzymująca request i zwracająca odpowiedź. Router wybiera handler.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

GET / zwraca 200 i nagłówek HTML. Content-Type to text/html.

## Pełny kod

```python
import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

async def hello(request):
    return web.Response(text="<h1>Welcome to my page!</h1>", content_type="text/html")

async def main():
    app = web.Application()
    app.router.add_get("/", hello)
    await demo(app, [
        ('GET', '/', None, 200),
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
async def hello(request):
```

Handler powitania otrzyma request od aiohttp dopiero po dopasowaniu trasy. Jego return stanie się odpowiedzią HTTP.

### L7

```python
    return web.Response(text="<h1>Welcome to my page!</h1>", content_type="text/html")
```

Tworzymy odpowiedź z treścią HTML i typem text/html. Przeglądarka zinterpretuje <h1> jako nagłówek. return kończy handler. W tym przykładzie HTML jest stałym tekstem.

### L9

```python
async def main():
```

Czytaj przebieg: __main__ → launch → asyncio.run(main()) → przygotowanie aplikacji i tras → demo → klient HTTP → router → handler → odpowiedź → dziennik klienta. W zadaniach z bazą database(Base) przygotowuje fabrykę; handler tworzy własną sesję. Definicja handlera pojawia się wcześniej w pliku, ale jego ciało rusza dopiero po żądaniu. W zadaniu 18 main sam wysyła dwa żądania, aby pokazać ich nakładanie.

### L9

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L10

```python
    app = web.Application()
```

Tworzymy aplikację aiohttp. Przechowa router i stan; ta linia jeszcze nie otwiera portu ani nie obsługuje żądania.

### L11

```python
    app.router.add_get("/", hello)
```

Rejestrujemy GET / → hello. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L12

```python
    await demo(app, [
```

Uruchamiamy pomocnika pokazu: startuje prawdziwy serwer na wolnym porcie, klient wysyła wymienione żądania po kolei i porównuje statusy z oczekiwaniami. Każda krotka to (metoda, ścieżka, JSON, oczekiwany status). Dziennik pokazuje również body. Po pokazie serwer jest zamykany.

### L13

```python
        ('GET', '/', None, 200),
```

Przypadek pokazu: GET /. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L14

```python
    ])
```

Zamykamy listę przypadków ] i wywołanie demo ). To kontynuacja poprzedniej instrukcji, a nie osobne działanie. await zaczeka na cały pokaz.

### L16

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L17

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Co zmienia content_type?

<details><summary>Odpowiedź</summary>

Mówi klientowi, jak interpretować body: tutaj jako HTML.

</details>
