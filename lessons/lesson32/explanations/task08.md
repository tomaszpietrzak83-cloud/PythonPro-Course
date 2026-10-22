# Zadanie 08: Wyjątek jako odpowiedź 403

HTTPForbidden przerywa handler; aiohttp zamienia wyjątek na odpowiedź HTTP.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

Anna otrzymuje 200; admin otrzymuje 403 i nie dochodzi do powitania.

## Pełny kod

```python
import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

async def hello(request):
    name = request.match_info["name"]
    if name == "admin":
        raise web.HTTPForbidden(text="Admin access forbidden")
    return web.Response(text=f"Hello, {name}!")

async def main():
    app = web.Application()
    app.router.add_get("/witaj/{name}", hello)
    await demo(app, [
        ('GET', '/witaj/Anna', None, 200),
        ('GET', '/witaj/admin', None, 403),
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
    name = request.match_info["name"]
```

Odczytujemy nazwę z fragmentu URL {name}. Dla /witaj/Anna zmienna name otrzyma tekst "Anna". To parametr ścieżki, nie query string ani JSON.

### L8

```python
    if name == "admin":
```

Porównanie jest czułe na wielkość liter. Tylko dokładne admin otrzyma 403.

### L9

```python
        raise web.HTTPForbidden(text="Admin access forbidden")
```

Przerywamy handler wyjątkiem HTTPForbidden. aiohttp zamieni go na odpowiedź HTTP 403 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L10

```python
    return web.Response(text=f"Hello, {name}!")
```

f-string wstawia name do powitania, np. Hello, Anna!. Zwracamy zwykły tekst (domyślnie text/plain), dzięki czemu nazwa użytkownika nie jest interpretowana jako HTML.

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
    app.router.add_get("/witaj/{name}", hello)
```

Rejestrujemy GET /witaj/{name} → hello. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L15

```python
    await demo(app, [
```

Uruchamiamy pomocnika pokazu: startuje prawdziwy serwer na wolnym porcie, klient wysyła wymienione żądania po kolei i porównuje statusy z oczekiwaniami. Każda krotka to (metoda, ścieżka, JSON, oczekiwany status). Dziennik pokazuje również body. Po pokazie serwer jest zamykany.

### L16

```python
        ('GET', '/witaj/Anna', None, 200),
```

Przypadek pokazu: GET /witaj/Anna. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L17

```python
        ('GET', '/witaj/admin', None, 403),
```

Przypadek pokazu: GET /witaj/admin. Body: None; None oznacza brak danych. Oczekujemy statusu 403. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

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

Czy po raise wykona się return powitania?

<details><summary>Odpowiedź</summary>

Nie. Wyjątek przerywa ten przebieg handlera.

</details>
