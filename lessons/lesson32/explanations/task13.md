# Zadanie 13: Trzy żądania przez gather

Wspólna ClientSession obsługuje kilka połączeń. gather nakłada oczekiwania sieciowe.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

Odczytujemy BTC, ETH i LTC. Tory pokazują nakładanie żądań; lista wyników zachowuje kolejność URL.

## Pełny kod

```python
import asyncio
from lab_support import launch, metric, span

from aiohttp import ClientSession, ClientTimeout

async def fetch(session, url):
    with span(url.split("/")[-2], "External HTTP"):
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

async def main():
    urls = [f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot" for symbol in ("BTC", "ETH", "LTC")]
    async with ClientSession(timeout=ClientTimeout(total=15)) as session:
        results = await asyncio.gather(*(fetch(session, url) for url in urls))
    for data in results:
        metric(data["data"]["base"] + " USD (live)", data["data"]["amount"])

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
from lab_support import launch, metric, span
```

Import z lab_support udostępnia narzędzia związane z zdarzeniami i pomiarem czasu pokazu, niezależnymi od logiki API. Import nie uruchamia main ani nie wysyła żądania.

### L4

```python
from aiohttp import ClientSession, ClientTimeout
```

Import z aiohttp udostępnia narzędzia związane z asynchronicznym HTTP: web buduje serwer, ClientSession wysyła żądania. Import nie uruchamia main ani nie wysyła żądania.

### L6

```python
async def fetch(session, url):
```

Korutyna klienta otrzymuje wspólną sesję HTTP oraz URL. Zwróci zdekodowany JSON; sama nie tworzy osobnej sesji.

### L7

```python
    with span(url.split("/")[-2], "External HTTP"):
```

Pomocnik obserwacji zapisuje początek i koniec tego bloku z czasem. Nawet przy wyjątku finally w span zapisze koniec. Pasek obejmuje czekanie; nie mierzy pracy procesora.

### L8

```python
        async with session.get(url) as response:
```

Wysyłamy asynchroniczne GET na url. Po otrzymaniu nagłówków response opisuje odpowiedź; body przeczytamy osobno. async with zwolni odpowiedź i umożliwi ponowne użycie połączenia.

### L9

```python
            response.raise_for_status()
```

Sprawdzamy odebrany status. Dla 4xx/5xx zgłaszany jest wyjątek zamiast próby odczytania błędu jako poprawnej ceny. Ta metoda nie potrzebuje await.

### L10

```python
            return await response.json()
```

Czekamy na body zewnętrznej odpowiedzi, zamieniamy JSON na obiekt Pythona i zwracamy go z fetch. gather zbierze te zwrócone obiekty.

### L12

```python
async def main():
```

Czytaj przebieg: __main__ → asyncio.run(main()) → ClientSession → GET publicznego API → status HTTP → response.json → słownik → metric. W zadaniu 13 gather uruchamia trzy fetch współbieżnie. Te pliki są klientami; nie uruchamiają własnego serwera.

### L12

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L13

```python
    urls = [f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot" for symbol in ("BTC", "ETH", "LTC")]
```

Lista składana tworzy trzy różne adresy dla BTC, ETH i LTC. f-string podstawia symbol do URL. Samo tworzenie listy nie wysyła żadnego żądania HTTP.

### L14

```python
    async with ClientSession(timeout=ClientTimeout(total=15)) as session:
```

Tworzymy klienta HTTP z pulą połączeń i limitem 15 s na żądanie. async with zamknie sesję także przy błędzie. To ClientSession sieci, a nie AsyncSession SQLAlchemy.

### L15

```python
        results = await asyncio.gather(*(fetch(session, url) for url in urls))
```

Generator tworzy fetch dla każdego URL, a * przekazuje je jako oddzielne argumenty gather. Jedna sesja HTTP obsługuje trzy współbieżne odczyty. Lista results zachowuje kolejność urls. Sesji HTTP można używać współbieżnie; AsyncSession bazy nie należy tak współdzielić.

### L16

```python
    for data in results:
```

Iterujemy po odpowiedziach z gather w kolejności wejściowych URL. data w każdej iteracji to jeden słownik odpowiedzi z ceną danej waluty.

### L17

```python
        metric(data["data"]["base"] + " USD (live)", data["data"]["amount"])
```

Publikujemy wskazaną wartość w panelu wyników i terminalu jako zdarzenie JSON. Argument pierwszy jest etykietą, drugi wynikiem. Nie zmieniamy danych w bazie; str zamienia listę na czytelny tekst, a data["data"]["amount"] odczytuje cenę z zagnieżdżonego JSON.

### L19

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L20

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Czy AsyncSession bazy też można tak współdzielić?

<details><summary>Odpowiedź</summary>

Nie. Każde współbieżne zadanie powinno mieć własną sesję bazy.

</details>
