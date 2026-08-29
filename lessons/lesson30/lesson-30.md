# Lekcja 30: Wątki, procesy i Globalna Blokada Interpretera (GIL)

`#lekcja` `#python` `#współbieżność` `#wątki` `#procesy` `#gil` `#optymalizacja`

Do tej pory nasze programy wykonywały zadania jedno po drugim, sekwencyjnie.

W tej lekcji przechodzimy do programowania współbieżnego. Nauczymy się, jak sprawić, by aplikacje robiły kilka rzeczy "jednocześnie" za pomocą wątków i procesów.

Poznamy też **GIL**, czyli Globalną Blokadę Interpretera, i zobaczymy, jak wpływa ona na wydajność programów w Pythonie.

## 1. Wątki (threads)

Wyobraź sobie kucharza w kuchni. Kucharz musi przygotować obiad: ugotować ziemniaki, usmażyć kotlety i zrobić sałatkę.

Podejście sekwencyjne:

- kucharz najpierw gotuje ziemniaki,
- czeka, aż się ugotują,
- potem smaży kotlety,
- na końcu robi sałatkę.

Podejście wielowątkowe:

- kucharz wstawia ziemniaki,
- zamiast czekać, zaczyna smażyć kotlety,
- w międzyczasie przygotowuje sałatkę,
- wraca do ziemniaków, gdy wymagają jego uwagi.

Wątki to takie podzadania w ramach jednego programu, które mogą być wykonywane współbieżnie.

> [!definition]
>
> Wątek (Thread) to najmniejsza sekwencja instrukcji, którą może zarządzać system operacyjny. W jednym procesie może działać wiele wątków, które dzielą tę samą przestrzeń pamięci.

W Pythonie do pracy z wątkami służy moduł `threading`.

## 2. Pierwszy wątek

```python
import threading
import time


def zadanie_dla_watku():
    """Prosta funkcja, którą wykona nasz wątek."""
    print("Wątek startuje...")
    time.sleep(2)
    print("Wątek kończy pracę.")


thread = threading.Thread(target=zadanie_dla_watku)
thread.start()

print("Główny program czeka...")

thread.join()

print("Główny program zakończył działanie.")
```

> [!info]
>
> `thread.start()` rozpoczyna wykonywanie wątku.
>
> `thread.join()` sprawia, że główny program czeka w tym miejscu, aż dany wątek zakończy działanie.

Bez `join()` główny program mógłby zakończyć się, zanim wątek skończy swoją pracę.

## 3. Wiele wątków

```python
import threading
import time


def witaj(numer_watku):
    print(f"Wątek numer {numer_watku} mówi: Cześć!")
    time.sleep(1)


watki = []

for i in range(5):
    thread = threading.Thread(target=witaj, args=(i,))
    watki.append(thread)
    thread.start()

print("Wszystkie wątki zostały uruchomione.")

for thread in watki:
    thread.join()

print("Wszystkie wątki zakończyły pracę.")
```

Wątki są dobre do zadań, które często czekają na coś zewnętrznego, na przykład:

- odpowiedź z serwera,
- odczyt pliku z dysku,
- odpowiedź z bazy danych.

Takie zadania nazywamy **I/O-bound**, czyli ograniczone przez operacje wejścia-wyjścia.

<p style="color:red"><strong>Komentarz mentora:</strong> Wątki nie zawsze oznaczają szybszy program. Najlepiej sprawdzają się wtedy, gdy program dużo czeka, a nie wtedy, gdy intensywnie liczy.</p>

## 4. Race condition

Wątki w jednym procesie dzielą tę samą pamięć. To oznacza, że kilka wątków może próbować zmienić tę samą zmienną w tym samym czasie.

Może wtedy dojść do błędu nazywanego **race condition**.

> [!definition]
>
> Wyścig (Race Condition) to błąd programistyczny, który występuje, gdy wynik działania programu zależy od nieprzewidywalnej kolejności wykonywania operacji przez wiele wątków.

Przykład problemu:

```python
import threading


licznik = 0


def inkrementuj():
    global licznik

    for _ in range(100000):
        licznik += 1


watki = []

for _ in range(10):
    thread = threading.Thread(target=inkrementuj)
    watki.append(thread)
    thread.start()

for thread in watki:
    thread.join()

print(f"Ostateczna wartość licznika: {licznik}")
```

Oczekiwany wynik:

```text
1000000
```

Rzeczywisty wynik może być mniejszy.

Problem polega na tym, że operacja:

```python
licznik += 1
```

nie jest atomowa. Składa się z kilku kroków:

1. Odczytaj wartość `licznik`.
2. Dodaj `1`.
3. Zapisz nową wartość do `licznik`.

Jeśli dwa wątki odczytają tę samą wartość w tym samym czasie, jeden z przyrostów może zostać utracony.

## 5. Lock

Aby zapobiegać race condition, trzeba zapewnić, że tylko jeden wątek naraz modyfikuje współdzielone dane.

Służy do tego blokada, czyli `Lock`.

> [!definition]
>
> Blokada (Lock) to mechanizm synchronizacyjny. Wątek, który chce wejść do sekcji krytycznej kodu, musi najpierw zdobyć blokadę. Dopóki jej nie zwolni, inny wątek nie może wejść do tej samej sekcji.

Przykład z `acquire()` i `release()`:

```python
import threading


licznik = 0
lock = threading.Lock()


def bezpieczna_inkrementacja():
    global licznik

    for _ in range(100000):
        lock.acquire()
        try:
            licznik += 1
        finally:
            lock.release()
```

> [!tip]
>
> Zawsze zwalniaj blokadę w `finally`, aby mieć pewność, że zostanie zwolniona nawet wtedy, gdy wystąpi błąd.

Lepszy zapis z `with`:

```python
def jeszcze_bezpieczniejsza_inkrementacja():
    global licznik

    for _ in range(100000):
        with lock:
            licznik += 1
```

`with lock` automatycznie zdobywa i zwalnia blokadę.

<p style="color:red"><strong>Komentarz mentora:</strong> Jeśli używasz `lock.acquire()` bez `finally`, bardzo łatwo przypadkiem zablokować program na stałe po wyjątku.</p>

## 6. GIL

Mogłoby się wydawać, że jeśli mamy procesor 4-rdzeniowy, to 4 wątki w Pythonie będą działać 4 razy szybciej przy zadaniu obliczeniowym.

W CPythonie tak zwykle nie jest. Powodem jest **GIL**.

> [!definition]
>
> Globalna Blokada Interpretera (GIL) to mechanizm w standardowym interpreterze Pythona (CPython), który pozwala tylko jednemu wątkowi wykonywać kod bajtowy Pythona w danym momencie, nawet na wielordzeniowym procesorze.

GIL upraszcza zarządzanie pamięcią w CPythonie, ale sprawia, że programy wielowątkowe nie mogą w pełni wykorzystać wielu rdzeni procesora do zadań **CPU-bound**.

Zadania CPU-bound to zadania ograniczone głównie mocą procesora, na przykład:

- skomplikowane obliczenia matematyczne,
- przetwarzanie obrazów,
- kompresja danych.

## 7. Kiedy wątki są użyteczne?

Wątki są użyteczne przy zadaniach **I/O-bound**.

Podczas oczekiwania na dane z sieci, dysku czy bazy danych wątek może zwolnić GIL, a inny wątek może w tym czasie działać.

Przykład:

```python
import threading
import time

import requests


urls = [
    "http://google.com",
    "http://youtube.com",
    "http://python.org",
    "http://github.com",
] * 3


def pobierz_strone(url):
    try:
        requests.get(url)
    except requests.exceptions.RequestException as error:
        print(f"Błąd dla {url}: {error}")


start_time = time.time()

for url in urls:
    pobierz_strone(url)

print(f"Sekwencyjnie: {time.time() - start_time:.2f} s")


start_time = time.time()
watki = []

for url in urls:
    thread = threading.Thread(target=pobierz_strone, args=(url,))
    watki.append(thread)
    thread.start()

for thread in watki:
    thread.join()

print(f"Wielowątkowo: {time.time() - start_time:.2f} s")
```

Wersja wielowątkowa powinna być szybsza, ponieważ podczas gdy jeden wątek czeka na odpowiedź serwera, inne mogą wysyłać swoje zapytania.

## 8. Procesy

Jak obejść GIL i wykorzystać wiele rdzeni procesora do zadań CPU-bound?

Odpowiedzią są procesy.

W Pythonie do tworzenia procesów służy moduł `multiprocessing`.

> [!definition]
>
> Proces (Process) to instancja uruchomionego programu. Każdy proces ma własną przestrzeń pamięci i własny interpreter Pythona, a więc także własny GIL.

System operacyjny może uruchomić wiele procesów na różnych rdzeniach procesora w tym samym czasie. To daje prawdziwą równoległość.

Przykład:

```python
import multiprocessing
import time


def ciezka_praca_obliczeniowa(n):
    print("Proces startuje...")
    suma = sum(i * i for i in range(n))
    print(f"Proces zakończył, suma: {suma}")


start = time.time()
ciezka_praca_obliczeniowa(20_000_000)
ciezka_praca_obliczeniowa(20_000_000)
print(f"Sekwencyjnie zajęło: {time.time() - start:.2f} s")


if __name__ == "__main__":
    start = time.time()

    p1 = multiprocessing.Process(
        target=ciezka_praca_obliczeniowa,
        args=(20_000_000,),
    )
    p2 = multiprocessing.Process(
        target=ciezka_praca_obliczeniowa,
        args=(20_000_000,),
    )

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"Równolegle zajęło: {time.time() - start:.2f} s")
```

> [!note]
>
> Konstrukcja `if __name__ == "__main__":` jest kluczowa przy `multiprocessing`, szczególnie na Windowsie. Zapobiega tworzeniu nowych procesów w nieskończoność, gdy moduł jest importowany.

<p style="color:red"><strong>Komentarz mentora:</strong> Na Windowsie brak `if __name__ == "__main__":` przy `multiprocessing` to jeden z najczęstszych błędów.</p>

## 9. Pule procesów

Ręczne zarządzanie wieloma procesami może być kłopotliwe.

`multiprocessing.Pool` pozwala łatwo rozdzielić pracę pomiędzy określoną liczbę procesów.

```python
from multiprocessing import Pool


def podnies_do_kwadratu(x):
    return x * x


if __name__ == "__main__":
    dane = range(10)

    with Pool(processes=4) as pool:
        wyniki = pool.map(podnies_do_kwadratu, dane)

    print(f"Oryginalne dane: {list(dane)}")
    print(f"Wyniki: {wyniki}")
```

## 10. Komunikacja między procesami

Procesy mają oddzielną pamięć, więc nie mogą komunikować się przez globalne zmienne tak jak wątki.

Potrzebują specjalnych mechanizmów komunikacji międzyprocesowej, czyli **IPC**.

> [!definition]
>
> IPC (Inter-Process Communication) to zestaw mechanizmów pozwalających procesom na komunikację i synchronizację. W Pythonie najczęściej używa się kolejek (`Queue`) i potoków (`Pipe`).

## 11. Kolejki (`multiprocessing.Queue`)

Kolejki są bezpieczne do użycia przez wiele procesów.

Jeden proces może wkładać obiekty do kolejki przez `put()`, a inny może je odbierać przez `get()`.

```python
from multiprocessing import Process, Queue


def pracownik(kolejka_zadan, kolejka_wynikow):
    for zadanie in iter(kolejka_zadan.get, "STOP"):
        wynik = zadanie * 2
        kolejka_wynikow.put(wynik)


if __name__ == "__main__":
    zadania_q = Queue()
    wyniki_q = Queue()

    for i in range(10):
        zadania_q.put(i)

    p = Process(target=pracownik, args=(zadania_q, wyniki_q))
    p.start()

    zadania_q.put("STOP")
    p.join()

    while not wyniki_q.empty():
        print(f"Odebrano wynik: {wyniki_q.get()}")
```

## 12. AI w zastosowaniach współbieżnych

Wątki i procesy można wykorzystać także przy zadaniach związanych z AI.

**Wątki i AI**

Jeśli aplikacja wysyła wiele opinii użytkowników do zewnętrznego API AI, większość czasu spędza na czekaniu na odpowiedź sieciową. To zadanie I/O-bound, więc wątki sprawdzą się dobrze.

**Procesy i AI**

Trenowanie modelu uczenia maszynowego albo przetwarzanie dużych zbiorów danych to zadania CPU-bound. W takich przypadkach można użyć `multiprocessing.Pool`, aby rozdzielić pracę między procesy.

## 13. Podsumowanie

W tej lekcji poznaliśmy:

- wątki i moduł `threading`,
- `start()` i `join()`,
- zadania I/O-bound,
- race condition,
- blokady `Lock`,
- GIL w CPythonie,
- procesy i moduł `multiprocessing`,
- pule procesów,
- komunikację między procesami przez `Queue`,
- różnicę między współbieżnością i równoległością.
