# Zadanie 18: Czat nie blokuje statusu

Handler czatu czeka przez asyncio.sleep, a pętla może w tym czasie obsłużyć inną trasę.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

Status OK pojawia się przed odpowiedzią czatu, mimo że czat wystartował pierwszy.

## Pełny kod

```python
import asyncio
from aiohttp import web
from lab_support import launch, span

from aiohttp import ClientSession
from api_support import server, request, object_json

async def chat(request):
    data = await object_json(request)
    prompt = data.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise web.HTTPBadRequest(text="prompt must be non-empty text")
    with span("chat", "Simulated AI wait"):
        await asyncio.sleep(3)
    return web.json_response({"response": f"Received and processed: {prompt}"})

async def status(request):
    return web.json_response({"status": "OK"})

async def main():
    app = web.Application()
    app.router.add_post("/api/v1/chat", chat)
    app.router.add_get("/api/status", status)
    async with server(app) as url:
        async with ClientSession() as client:
            chat_task = asyncio.create_task(request(client, "POST", url + "/api/v1/chat", {"prompt": "Explain await"}))
            await asyncio.sleep(0.1)
            await request(client, "GET", url + "/api/status")
            await chat_task

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
from lab_support import launch, span
```

Import z lab_support udostępnia narzędzia związane z zdarzeniami i pomiarem czasu pokazu, niezależnymi od logiki API. Import nie uruchamia main ani nie wysyła żądania.

### L5

```python
from aiohttp import ClientSession
```

Import z aiohttp udostępnia narzędzia związane z asynchronicznym HTTP: web buduje serwer, ClientSession wysyła żądania. Import nie uruchamia main ani nie wysyła żądania.

### L6

```python
from api_support import server, request, object_json
```

Import z api_support udostępnia narzędzia związane z lokalnym serwerem testowym, walidacją i izolowaną bazą; pełny kod jest w osobnym pliku. Import nie uruchamia main ani nie wysyła żądania.

### L8

```python
async def chat(request):
```

Handler udaje usługę AI: odbierze prompt i poczeka 3 sekundy. W czasie czekania inne żądania mogą być obsługiwane.

### L9

```python
    data = await object_json(request)
```

Pomocnik czyta JSON i sprawdza, czy wynikiem jest słownik. Zwraca go do data. Niepoprawny JSON lub lista zamiast obiektu kończą żądanie statusem 400.

### L10

```python
    prompt = data.get("prompt")
```

Ze słownika JSON odczytujemy prompt. Przy braku klucza get zwraca None; następny warunek sprawdzi typ i niepustą treść.

### L11

```python
    if not isinstance(prompt, str) or not prompt.strip():
```

Akceptujemy wyłącznie tekst z co najmniej jednym znakiem innym niż biały. or odrzuca błędny typ przed próbą strip.

### L12

```python
        raise web.HTTPBadRequest(text="prompt must be non-empty text")
```

Przerywamy handler wyjątkiem HTTPBadRequest. aiohttp zamieni go na odpowiedź HTTP 400 z podanym tekstem. Jeśli wyjątek wychodzi z session.begin, zmiany tej transakcji zostaną wycofane. Dalsze linie handlera nie wykonają się.

### L13

```python
    with span("chat", "Simulated AI wait"):
```

Pomocnik obserwacji zapisuje początek i koniec tego bloku z czasem. Nawet przy wyjątku finally w span zapisze koniec. Pasek obejmuje czekanie; nie mierzy pracy procesora.

### L14

```python
        await asyncio.sleep(3)
```

Symulujemy trzysekundowe oczekiwanie na usługę AI. Korutyna czatu zostaje zawieszona, a event loop może obsłużyć /api/status. Nie uruchamiamy tu prawdziwego modelu AI.

### L15

```python
    return web.json_response({"response": f"Received and processed: {prompt}"})
```

Zwracamy odpowiedź JSON z wyrażenia {"response": f"Received and processed: {prompt}"}. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L17

```python
async def status(request):
```

Szybki handler stanu zwraca JSON. Nie ma powodu dodawać await do samego tworzenia odpowiedzi.

### L18

```python
    return web.json_response({"status": "OK"})
```

Zwracamy odpowiedź JSON z wyrażenia {"status": "OK"}. json_response koduje wartości Pythona i ustawia Content-Type: application/json. Domyślny status to 200; status=201 oznacza utworzenie, a 400 błędne wejście. return kończy handler i oddaje odpowiedź aiohttp.

### L20

```python
async def main():
```

Czytaj przebieg: __main__ → launch → asyncio.run(main()) → przygotowanie aplikacji i tras → demo → klient HTTP → router → handler → odpowiedź → dziennik klienta. W zadaniach z bazą database(Base) przygotowuje fabrykę; handler tworzy własną sesję. Definicja handlera pojawia się wcześniej w pliku, ale jego ciało rusza dopiero po żądaniu. W zadaniu 18 main sam wysyła dwa żądania, aby pokazać ich nakładanie.

### L20

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L21

```python
    app = web.Application()
```

Tworzymy aplikację aiohttp. Przechowa router i stan; ta linia jeszcze nie otwiera portu ani nie obsługuje żądania.

### L22

```python
    app.router.add_post("/api/v1/chat", chat)
```

Rejestrujemy POST /api/v1/chat → chat. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L23

```python
    app.router.add_get("/api/status", status)
```

Rejestrujemy GET /api/status → status. Przekazujemy funkcję bez (), więc nie wywołujemy jej teraz. aiohttp zrobi to po dopasowaniu metody i ścieżki żądania.

### L24

```python
    async with server(app) as url:
```

Pomocnik uruchamia prawdziwy serwer aiohttp na wolnym porcie localhost. url zawiera jego adres. Po wyjściu z bloku runner.cleanup zatrzyma serwer i posprząta zasoby.

### L25

```python
        async with ClientSession() as client:
```

Tworzymy jednego klienta HTTP do lokalnych żądań. Sesja współdzieli pulę połączeń; blok async with zamknie ją po zakończeniu pokazu.

### L26

```python
            chat_task = asyncio.create_task(request(client, "POST", url + "/api/v1/chat", {"prompt": "Explain await"}))
```

Tworzymy Task dla żądania POST z promptem Explain await. create_task planuje korutynę, lecz nie czeka na odpowiedź. Zachowujemy uchwyt chat_task, aby później odebrać wynik i ewentualny wyjątek.

### L27

```python
            await asyncio.sleep(0.1)
```

Oddajemy pętli sterowanie na około 0,1 s, aby zaplanowane żądanie czatu mogło ruszyć. Potem wyślemy szybkie żądanie statusu, zanim czat skończy trzysekundowe oczekiwanie.

### L28

```python
            await request(client, "GET", url + "/api/status")
```

Wysyłamy drugie żądanie tym samym klientem, gdy czat nadal czeka. Status OK powinien pojawić się w dzienniku przed odpowiedzią czatu: to dowód, że sleep w handlerze oddaje sterowanie.

### L29

```python
            await chat_task
```

Czekamy na zakończenie wcześniej utworzonego Task czatu. Nie uruchamiamy drugiego czatu. Ewentualny wyjątek zostanie zgłoszony tutaj, zamiast pozostać nieodebrany.

### L31

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L32

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Co zmieni time.sleep(3)?

<details><summary>Odpowiedź</summary>

Zablokuje wątek event loop i opóźni również odpowiedź statusu.

</details>
