# Zadanie 12: Klient publicznego API

ClientSession jest klientem HTTP, a nie serwerem ani sesją bazy danych.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

Prawdziwe publiczne API zwraca bieżącą cenę BTC w USD. Wartość zależy od momentu zapytania.

## Pełny kod

```python
import asyncio
from lab_support import launch, metric

from aiohttp import ClientSession, ClientTimeout

async def main():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    async with ClientSession(timeout=ClientTimeout(total=15)) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            metric("Bitcoin USD (live)", data["data"]["amount"])

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
from lab_support import launch, metric
```

Import z lab_support udostępnia narzędzia związane z zdarzeniami i pomiarem czasu pokazu, niezależnymi od logiki API. Import nie uruchamia main ani nie wysyła żądania.

### L4

```python
from aiohttp import ClientSession, ClientTimeout
```

Import z aiohttp udostępnia narzędzia związane z asynchronicznym HTTP: web buduje serwer, ClientSession wysyła żądania. Import nie uruchamia main ani nie wysyła żądania.

### L6

```python
async def main():
```

Czytaj przebieg: __main__ → asyncio.run(main()) → ClientSession → GET publicznego API → status HTTP → response.json → słownik → metric. W zadaniu 13 gather uruchamia trzy fetch współbieżnie. Te pliki są klientami; nie uruchamiają własnego serwera.

### L6

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L7

```python
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
```

Zapisujemy adres publicznego endpointu ceny BTC w USD. Zastępuje wskazany w poleceniu stary CoinDesk. Ten pokaz potrzebuje internetu; otrzymana cena jest bieżąca, a nie stałą daną ćwiczenia.

### L8

```python
    async with ClientSession(timeout=ClientTimeout(total=15)) as session:
```

Tworzymy klienta HTTP z pulą połączeń i limitem 15 s na żądanie. async with zamknie sesję także przy błędzie. To ClientSession sieci, a nie AsyncSession SQLAlchemy.

### L9

```python
        async with session.get(url) as response:
```

Wysyłamy asynchroniczne GET na url. Po otrzymaniu nagłówków response opisuje odpowiedź; body przeczytamy osobno. async with zwolni odpowiedź i umożliwi ponowne użycie połączenia.

### L10

```python
            response.raise_for_status()
```

Sprawdzamy odebrany status. Dla 4xx/5xx zgłaszany jest wyjątek zamiast próby odczytania błędu jako poprawnej ceny. Ta metoda nie potrzebuje await.

### L11

```python
            data = await response.json()
```

Odczytujemy body odpowiedzi serwera i dekodujemy JSON do słownika. To odpowiedź zewnętrznego API, nie JSON przychodzącego requestu naszego serwera.

### L12

```python
            metric("Bitcoin USD (live)", data["data"]["amount"])
```

Publikujemy wskazaną wartość w panelu wyników i terminalu jako zdarzenie JSON. Argument pierwszy jest etykietą, drugi wynikiem. Nie zmieniamy danych w bazie; str zamienia listę na czytelny tekst, a data["data"]["amount"] odczytuje cenę z zagnieżdżonego JSON.

### L14

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L15

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Gdzie jest cena w słowniku?

<details><summary>Odpowiedź</summary>

data["data"]["amount"]. Zewnętrzne data to zmienna; wewnętrzne "data" to klucz JSON.

</details>
