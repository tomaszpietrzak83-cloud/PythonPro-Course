# Zadanie 01: Współbieżne oczekiwania

gather planuje trzy korutyny; await pozwala nakładać ich oczekiwania.

## Przebieg

Start: blok `__main__` → `launch` → `asyncio.run(main())` → przygotowanie aplikacji → pokaz HTTP → router → handler → odpowiedź. Definicje funkcji i modeli są przygotowane przy ładowaniu modułu; ich ciała nie wykonują się wtedy.

Koniec A po 1 s, C po 2 s, B po 4 s. Wyniki [1, 4, 2] zachowują kolejność wejścia.

## Pełny kod

```python
import asyncio
from lab_support import launch, metric, span

async def operation(name, delay):
    with span(name, "Waiting for I/O"):
        await asyncio.sleep(delay)
        return delay

async def main():
    results = await asyncio.gather(operation("A", 1), operation("B", 4), operation("C", 2))
    metric("Delays in input order", str(results))

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
async def operation(name, delay):
```

Korutyna otrzyma nazwę i opóźnienie, zaczeka bez blokowania pętli, a następnie zwróci delay.

### L5

```python
    with span(name, "Waiting for I/O"):
```

Pomocnik obserwacji zapisuje początek i koniec tego bloku z czasem. Nawet przy wyjątku finally w span zapisze koniec. Pasek obejmuje czekanie; nie mierzy pracy procesora.

### L6

```python
        await asyncio.sleep(delay)
```

Zawieszamy bieżącą korutynę na delay sekund. W tym czasie inne gotowe korutyny mogą działać. To symulacja oczekiwania I/O, nie pomiar intensywnych obliczeń.

### L7

```python
        return delay
```

Kończymy operation i przekazujemy liczbę sekund do gather. Ta wartość trafi na odpowiednią pozycję listy results.

### L9

```python
async def main():
```

Czytaj przebieg: __main__ → launch → asyncio.run → main → gather → trzy operation → sleep → return → lista wyników → metric. Definicje na górze pliku przygotowują funkcje; samo ich przeczytanie przez interpreter nie uruchamia oczekiwań.

### L9

```python
async def main():
```

Główna korutyna przygotowuje dane i uruchamia pokaz. Definicja nie wykonuje ciała; wykonanie zacznie się przez asyncio.run(main()).

### L10

```python
    results = await asyncio.gather(operation("A", 1), operation("B", 4), operation("C", 2))
```

Tworzymy trzy korutyny i przekazujemy je gather. Oczekiwania 1, 4 i 2 sekundy nakładają się, więc całość trwa około 4 s. results ma kolejność wejściową [1, 4, 2], chociaż kolejność końców to A, C, B.

### L11

```python
    metric("Delays in input order", str(results))
```

Publikujemy wskazaną wartość w panelu wyników i terminalu jako zdarzenie JSON. Argument pierwszy jest etykietą, drugi wynikiem. Nie zmieniamy danych w bazie; str zamienia listę na czytelny tekst, a data["data"]["amount"] odczytuje cenę z zagnieżdżonego JSON.

### L13

```python
if __name__ == "__main__":
```

Ten warunek jest prawdziwy przy uruchomieniu pliku jako skryptu. Import pliku nie uruchomi pokazu. Stąd przechodzimy do launch, asyncio.run i main.

### L14

```python
    launch(lambda options: asyncio.run(main()))
```

launch dodaje zdarzenia START/END i pomiar czasu. lambda jest funkcją przekazaną do launch; options to dane wariantu, tutaj nieużywane. main() tworzy korutynę, a asyncio.run uruchamia ją w nowej pętli i zamyka pętlę po zakończeniu.

## Sprawdź rozumienie

Ile trwałby wariant sekwencyjny?

<details><summary>Odpowiedź</summary>

Około 7 s: 1 + 4 + 2. Współbieżnie około 4 s, plus narzut.

</details>
