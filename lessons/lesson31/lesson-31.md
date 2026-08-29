# Lekcja 31: Asynchroniczność w Pythonie - wprowadzenie do asyncio

`#lekcja` `#python` `#asynchroniczność` `#asyncio` `#korutyny` `#programowanie-współbieżne`

W tej lekcji wchodzimy w programowanie asynchroniczne w Pythonie.

Dowiesz się, jak pisać kod, który potrafi obsługiwać wiele operacji wejścia-wyjścia jednocześnie, bez używania wielu wątków czy procesów.

To ważna umiejętność w nowoczesnym backendzie, szczególnie przy budowie:

- aplikacji webowych,
- API,
- botów,
- integracji z zewnętrznymi usługami.

Wykorzystamy wbudowany moduł `asyncio`.

## 1. Czym jest asynchroniczność?

Asynchroniczność to inne podejście do współbieżności niż wątki i procesy.

Najlepiej sprawdza się przy zadaniach **I/O-bound**, czyli takich, w których program dużo czeka na zewnętrzne zasoby:

- odpowiedź z API,
- zapytanie do bazy danych,
- odczyt pliku,
- odpowiedź z sieci.

> [!definition]
>
> Asynchroniczność to model programowania współbieżnego, w którym pojedynczy wątek może zarządzać wieloma zadaniami. Zamiast czekać bezczynnie na zakończenie operacji, program może w tym czasie wykonywać inne zadanie.

Przykład z kucharzem:

- **Synchronicznie** - kucharz wstawia ziemniaki i czeka 20 minut, nic nie robiąc. Potem smaży kotlet i znowu czeka.
- **Asynchronicznie** - kucharz wstawia ziemniaki, a podczas czekania zaczyna smażyć kotlet i robić sałatkę.

<p style="color:red"><strong>Komentarz mentora:</strong> Asynchroniczność nie oznacza automatycznie szybszych obliczeń. Największy zysk daje wtedy, gdy program dużo czeka na I/O.</p>

## 2. Synchronicznie vs asynchronicznie

Schemat synchroniczny:

```text
Klient -> Program
Program -> Baza danych
Program czeka...
Baza danych -> Program
Program -> API
Program czeka...
API -> Program
Program -> Klient
```

Schemat asynchroniczny:

```text
Klient -> Program
Program -> rozpocznij zapytanie do bazy
Program -> rozpocznij zapytanie do API
Program może robić coś innego
Baza/API zwracają odpowiedzi
Program -> Klient
```

## 3. Korutyny

Podstawowym budulcem asynchroniczności w `asyncio` są korutyny.

> [!definition]
>
> Korutyna (Coroutine) to specjalny rodzaj funkcji, której wykonanie można wstrzymać i wznowić później. W Pythonie tworzymy ją za pomocą `async def`.

Wywołanie korutyny nie uruchamia jej kodu od razu. Zwraca obiekt korutyny.

```python
import asyncio


async def moja_korutyna():
    print("Witaj w świecie asynchroniczności!")


korutyna_obj = moja_korutyna()

print(f"Typ obiektu: {type(korutyna_obj)}")
print(f"Obiekt korutyny: {korutyna_obj}")

print("Uruchamiam korutynę...")
asyncio.run(korutyna_obj)
```

Aby uruchomić korutynę, potrzebujemy pętli zdarzeń. Najczęściej używamy do tego:

```python
asyncio.run(...)
```

Korutyny mogą przyjmować argumenty i zwracać wartości tak jak zwykłe funkcje.

```python
import asyncio


async def przygotuj_danie(nazwa, czas_przygotowania):
    print(f"Rozpoczynam przygotowanie: {nazwa}")
    await asyncio.sleep(czas_przygotowania)
    print(f"Danie gotowe: {nazwa}")
    return f"Serwuję {nazwa}"


async def main():
    wynik = await przygotuj_danie("Pizza", 2)
    print(wynik)


asyncio.run(main())
```

## 4. Pętla zdarzeń

Sercem `asyncio` jest pętla zdarzeń, czyli **event loop**.

> [!definition]
>
> Pętla zdarzeń to mechanizm, który zarządza wykonaniem zadań asynchronicznych. Sprawdza, które zadania są gotowe do działania, i przekazuje im kontrolę.

Kiedy korutyna trafia na operację wymagającą czekania, na przykład:

```python
await asyncio.sleep(1)
```

informuje pętlę zdarzeń, że może zostać chwilowo wstrzymana. W tym czasie event loop może uruchomić inną gotową korutynę.

Zwykle nie zarządzamy pętlą zdarzeń ręcznie. `asyncio.run()`:

- tworzy pętlę zdarzeń,
- uruchamia przekazaną korutynę,
- zamyka pętlę po zakończeniu.

## 5. `async` i `await`

`async` i `await` to podstawowe słowa kluczowe składni asynchronicznej.

- `async def` definiuje funkcję jako korutynę.
- `await` wstrzymuje wykonanie aktualnej korutyny i czeka na wynik innej korutyny albo innego obiektu awaitable.

`await` można używać tylko wewnątrz funkcji zadeklarowanej jako `async def`.

Przykład sekwencyjny:

```python
import asyncio


async def pobierz_dane_uzytkownika(user_id):
    print(f"Pobieram dane dla użytkownika {user_id}...")
    await asyncio.sleep(2)
    print("Dane użytkownika pobrane.")
    return {"id": user_id, "name": "Jan Kowalski"}


async def pobierz_zamowienia_uzytkownika(user_id):
    print(f"Pobieram zamówienia dla użytkownika {user_id}...")
    await asyncio.sleep(3)
    print("Zamówienia pobrane.")
    return ["książka", "długopis", "zeszyt"]


async def main():
    dane = await pobierz_dane_uzytkownika(1)
    zamowienia = await pobierz_zamowienia_uzytkownika(dane["id"])

    print(f"Użytkownik: {dane['name']}, zamówienia: {zamowienia}")


asyncio.run(main())
```

Czas wykonania to około 5 sekund, bo najpierw czekamy 2 sekundy, a potem 3 sekundy.

<p style="color:red"><strong>Komentarz mentora:</strong> Samo dodanie `async` nie daje współbieżności. Jeśli używasz `await` jedno po drugim, kod nadal może działać sekwencyjnie.</p>

## 6. Task

Aby uruchomić wiele operacji współbieżnie, używamy zadań, czyli `Task`.

> [!definition]
>
> Task opakowuje korutynę i planuje jej wykonanie w pętli zdarzeń. Tworzymy go za pomocą `asyncio.create_task()`.

Różnica:

- `await moja_korutyna()` - czeka na zakończenie korutyny i działa sekwencyjnie.
- `asyncio.create_task(moja_korutyna())` - planuje wykonanie korutyny i pozwala kontynuować aktualną funkcję.

Przykład współbieżny:

```python
import asyncio
import time


async def pobierz_dane_uzytkownika(user_id):
    print(f"Pobieram dane dla użytkownika {user_id}...")
    await asyncio.sleep(2)
    print("Dane użytkownika pobrane.")
    return {"id": user_id, "name": "Jan Kowalski"}


async def pobierz_zamowienia_uzytkownika(user_id):
    print(f"Pobieram zamówienia dla użytkownika {user_id}...")
    await asyncio.sleep(3)
    print("Zamówienia pobrane.")
    return ["książka", "długopis", "zeszyt"]


async def main():
    start_time = time.time()

    task_dane = asyncio.create_task(pobierz_dane_uzytkownika(1))
    task_zamowienia = asyncio.create_task(pobierz_zamowienia_uzytkownika(1))

    dane = await task_dane
    zamowienia = await task_zamowienia

    print(f"Użytkownik: {dane['name']}, zamówienia: {zamowienia}")
    print(f"Całkowity czas wykonania: {time.time() - start_time:.2f} s")


asyncio.run(main())
```

Czas wykonania to około 3 sekundy, czyli mniej więcej czas najdłuższej operacji.

## 7. `asyncio.gather()`

Często chcemy uruchomić wiele zadań i poczekać, aż wszystkie się zakończą.

Do tego służy `asyncio.gather()`.

> [!definition]
>
> `asyncio.gather(*aws)` uruchamia przekazane korutyny lub zadania współbieżnie i zwraca listę wyników, gdy wszystkie się zakończą.

Przykład:

```python
import asyncio
import time


async def operacja(nazwa, czas_trwania):
    print(f"Start: {nazwa}")
    await asyncio.sleep(czas_trwania)
    print(f"Koniec: {nazwa}")
    return f"Wynik z {nazwa}"


async def main():
    start_time = time.time()

    wyniki = await asyncio.gather(
        operacja("A", 3),
        operacja("B", 1),
        operacja("C", 2),
    )

    print(f"Wyniki: {wyniki}")
    print(f"Całkowity czas wykonania: {time.time() - start_time:.2f} s")


asyncio.run(main())
```

Czas wykonania to około 3 sekundy, czyli czas najdłuższej operacji.

## 8. Inne mechanizmy synchronizacji w `asyncio`

`asyncio` ma też inne przydatne narzędzia:

- `asyncio.wait()` - daje większą kontrolę, na przykład pozwala czekać na pierwsze zakończone zadanie.
- `asyncio.Queue` - asynchroniczna kolejka do komunikacji między korutynami.
- `asyncio.Lock` - blokada zapobiegająca jednoczesnemu dostępowi do zasobu przez wiele korutyn.

<p style="color:red"><strong>Komentarz mentora:</strong> W kodzie asynchronicznym nie używaj `time.sleep()`, bo blokuje cały wątek i event loop. Używaj `await asyncio.sleep()`.</p>

## 9. AI i asynchroniczność

Wiele nowoczesnych zastosowań AI polega na wysyłaniu zapytań do zewnętrznego API.

To klasyczny przykład operacji I/O-bound.

Jeśli trzeba przetworzyć setki albo tysiące zapytań, robienie tego synchronicznie byłoby bardzo wolne.

Asynchroniczność pozwala wysłać wiele zapytań współbieżnie i zbierać odpowiedzi, gdy tylko są gotowe.

Przykład koncepcyjny:

```python
import asyncio
import random
import time


async def popros_ai_o_analize(tekst):
    """Symuluje zapytanie do API analizującego sentyment tekstu."""
    print(f"Wysyłam do analizy: '{tekst[:20]}...'")

    czas_oczekiwania = random.uniform(1, 4)
    await asyncio.sleep(czas_oczekiwania)

    wynik = random.choice(["pozytywny", "negatywny", "neutralny"])
    print(f"Otrzymano odpowiedź dla: '{tekst[:20]}...' -> {wynik}")

    return {"tekst": tekst, "sentyment": wynik}


async def main():
    zdania = [
        "To był absolutnie fantastyczny film!",
        "Obsługa klienta jest poniżej krytyki.",
        "Pogoda dzisiaj jest całkiem w porządku.",
        "Nie mogę się doczekać wakacji.",
        "Znowu utknąłem w korku, co za dzień.",
    ]

    start_time = time.time()

    zadania = [popros_ai_o_analize(zdanie) for zdanie in zdania]
    wyniki_analizy = await asyncio.gather(*zadania)

    print("\n--- Wyniki końcowe ---")
    for wynik in wyniki_analizy:
        print(f"'{wynik['tekst']}' ma sentyment: {wynik['sentyment']}")

    print(f"\nCałkowity czas analizy: {time.time() - start_time:.2f} s")


asyncio.run(main())
```

## 10. Podsumowanie

W tej lekcji nauczyliśmy się:

- czym jest asynchroniczność,
- kiedy warto używać `asyncio`,
- czym są korutyny,
- jak działa pętla zdarzeń,
- do czego służą `async` i `await`,
- czym różni się `await` od `asyncio.create_task()`,
- jak działa `asyncio.gather()`,
- do czego służą `asyncio.wait()`, `asyncio.Queue` i `asyncio.Lock`,
- dlaczego asynchroniczność dobrze pasuje do zapytań do zewnętrznych API.
