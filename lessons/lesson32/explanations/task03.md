# Zadanie 03: Parametr ścieżki

Fragment {name} w trasie przechwytuje tekst z URL do match_info.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

/witaj/Anna → Hello, Anna! Parametr zmienia treść odpowiedzi.

## Pełny kod

```python
import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

async def hello(request):
    name = request.match_info["name"]
    return web.Response(text=f"Hello, {name}!")

async def main():
    app = web.Application()
    app.router.add_get("/witaj/{name}", hello)
    await demo(app, [
        ('GET', '/witaj/Anna', None, 200),
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
    return web.Response(text=f"Hello, {name}!")
```

f-string wstawia name do powitania, np. Hello, Anna!. Zwracamy zwykły tekst (domyślnie text/plain), dzięki czemu nazwa użytkownika nie jest interpretowana jako HTML.

### L10

```python
async def main():
```

Czytaj przebieg: __main__ → launch → asyncio.run(main()) → przygotowanie aplikacji i tras → demo → klient HTTP → router → handler → odpowiedź → dziennik klienta. W zadaniach z bazą database(Base) przygotowuje fabrykę; handler tworzy własną sesję. Definicja handlera pojawia się wcześniej w pliku, ale jego ciało rusza dopiero po żądaniu. W zadaniu 18 main sam wysyła dwa żądania, aby pokazać ich nakładanie.

### L10

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L11

```python
    app = web.Application()
```

Tworzymy aplikację aiohttp. Przechowa router i stan; ta linia jeszcze nie otwiera portu ani nie obsługuje żądania.

### L12

```python
    app.router.add_get("/witaj/{name}", hello)
```

Rejestrujemy GET /witaj/{name} → hello. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L13

```python
    await demo(app, [
```

Uruchamiamy pomocnika pokazu: startuje prawdziwy serwer na wolnym porcie, klient wysyła wymienione żądania po kolei i porównuje statusy z oczekiwaniami. Każda krotka to (metoda, ścieżka, JSON, oczekiwany status). Dziennik pokazuje również body. Po pokazie serwer jest zamykany.

### L14

```python
        ('GET', '/witaj/Anna', None, 200),
```

Przypadek pokazu: GET /witaj/Anna. Body: None; None oznacza brak danych. Oczekujemy statusu 200. Pomocnik wyśle to żądanie po zakończeniu poprzedniego i zapisze body odpowiedzi. Porównaj wartości z wcześniejszym stanem bazy.

### L15

```python
    ])
```

Zamykamy listę przypadków ] i wywołanie demo ). To kontynuacja poprzedniej instrukcji, a nie osobne działanie. await zaczeka na cały pokaz.

### L17

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L18

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Czy name pochodzi z JSON?

<details><summary>Odpowiedź</summary>

Nie, pochodzi ze ścieżki URL, z request.match_info.

</details>
