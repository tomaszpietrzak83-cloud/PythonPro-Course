# Lesson 31 - Zadania

## TASK 01 - Pierwsza korutyna (proste)

Napisz korutynę, która po uruchomieniu wypisze na konsolę:

```text
Gotowy do nauki asyncio!
```

Uruchom ją za pomocą:

```python
asyncio.run()
```

## TASK 02 - Asynchroniczny licznik (proste)

Napisz korutynę:

```python
licznik(n)
```

Korutyna ma przyjmować liczbę `n` i co sekundę wypisywać kolejne liczby od 1 do `n`.

Użyj:

```python
asyncio.sleep(1)
```

## TASK 03 - Dwa zadania po kolei (proste)

Stwórz dwie korutyny:

- `zadanie1` - śpi przez 2 sekundy i drukuje `Zadanie 1 zakończone`,
- `zadanie2` - śpi przez 1 sekundę i drukuje `Zadanie 2 zakończone`.

W głównej korutynie `main` uruchom je sekwencyjnie, używając `await` na każdej z nich po kolei.

Zmierz czas wykonania.

## TASK 04 - Dwa zadania współbieżnie (proste)

Zmodyfikuj kod z poprzedniego zadania.

Uruchom obie korutyny współbieżnie, używając:

```python
asyncio.gather()
```

Zmierz i porównaj czas wykonania.

## TASK 05 - Korutyna zwracająca wartość (proste)

Napisz korutynę:

```python
oblicz_potege(liczba, potega)
```

Korutyna ma po 2 sekundach opóźnienia zwrócić wynik potęgowania.

W `main` wywołaj ją i wydrukuj otrzymany wynik.

## TASK 06 - Symulacja pobierania danych (proste)

Stwórz korutynę:

```python
pobierz_pogode(miasto)
```

Korutyna ma po 1.5 sekundy zwracać słownik z fikcyjnymi danymi pogodowymi, na przykład:

```python
{
    "miasto": miasto,
    "temperatura": 25,
    "stan": "słonecznie",
}
```

## TASK 07 - Wiele miast (proste)

Używając korutyny z zadania 6, napisz program, który współbieżnie pobierze dane pogodowe dla listy miast:

```python
["Warszawa", "Kraków", "Gdańsk"]
```

Wydrukuj wyniki.

## TASK 08 - Asynchroniczny ping (proste)

Napisz korutynę:

```python
ping(host)
```

Korutyna ma symulować pingowanie serwera przez:

```python
asyncio.sleep(random.uniform(0.1, 1.0))
```

Ma zwracać tekst:

```python
f"Host {host} odpowiada"
```

Uruchom ją dla 5 różnych hostów współbieżnie.

## TASK 09 - Pobieranie statusów HTTP (challenge)

Napisz program, który przyjmuje listę adresów URL i współbieżnie sprawdza status HTTP każdego z nich.

Użyj biblioteki `aiohttp`.

Wskazówka:

```bash
pip install aiohttp
```

Użyj `aiohttp.ClientSession`.

Dla każdego URL wypisz status, na przykład:

```text
https://google.com - Status: 200
```

## TASK 10 - Współbieżne odliczanie (challenge)

Napisz korutynę:

```python
odliczanie(nazwa, start)
```

Korutyna ma co sekundę drukować komunikat:

```text
{nazwa}: zostało {pozostało} sekund
```

Uruchom trzy takie odliczania współbieżnie, każde z inną nazwą i innym czasem początkowym, na przykład 5s, 3s i 7s.

## TASK 11 - Sumowanie wyników zadań (challenge)

Napisz korutynę:

```python
dlugie_obliczenia()
```

Korutyna ma po losowym czasie od 2 do 5 sekund zwracać losową liczbę całkowitą od 1 do 100.

Uruchom 10 takich zadań współbieżnie.

Po zakończeniu wszystkich oblicz i wypisz sumę ich wyników.

## TASK 12 - Kto pierwszy, ten lepszy (challenge)

Uruchom 5 zadań.

Każde zadanie ma:

- spać przez losowy czas od 1 do 10 sekund,
- zwracać swój czas uśpienia.

Napisz program, który zakończy działanie i wypisze wynik pierwszego zakończonego zadania, nie czekając na pozostałe.

Wskazówka: użyj `asyncio.wait()` z argumentem:

```python
return_when=asyncio.FIRST_COMPLETED
```

<p style="color:red"><strong>Komentarz mentora:</strong> Po znalezieniu pierwszego wyniku warto anulować pozostałe zadania, żeby nie zostawiać ich działających w tle bez kontroli.</p>

## TASK 13 - Prosty serwer echa (challenge)

Używając `asyncio`, napisz prosty serwer TCP, który nasłuchuje na:

```text
localhost:8888
```

Kiedy klient się połączy i wyśle wiadomość, serwer powinien:

- odesłać tę samą wiadomość,
- zamknąć połączenie.

Wskazówka: poszukaj w dokumentacji:

```python
asyncio.start_server
```

## TASK 14 - Kolejka producent-konsument (challenge)

Zaimplementuj system z jednym producentem i dwoma konsumentami przy użyciu:

```python
asyncio.Queue
```

Wymagania:

- producent co 0.5 sekundy dodaje do kolejki liczbę od 1 do 20,
- konsumenci pobierają liczby z kolejki, gdy tylko się pojawią,
- program wypisuje, który konsument przetworzył daną liczbę.

Przykład:

```text
Konsument 1 przetworzył liczbę: 5
```

## TASK 15 - Asynchroniczny zapis do pliku (challenge)

Napisz program, w którym 5 korutyn współbieżnie generuje dane tekstowe, na przykład:

```text
Log z korutyny X
```

Wszystkie korutyny mają zapisywać logi do jednego pliku.

Zapewnij synchronizację dostępu do pliku, żeby wpisy się nie pomieszały.

Użyj:

- `asyncio.Lock`,
- `aiofiles`.

Wskazówka:

```bash
pip install aiofiles
```

## TASK 16 - Ogranicznik zapytań, czyli Rate Limiter (challenge)

Stwórz klasę `RateLimiter` z metodą:

```python
acquire()
```

Klasa powinna pozwalać na wykonanie `acquire()` tylko `n` razy na sekundę.

Jeśli limit jest przekroczony, `acquire()` powinno asynchronicznie czekać tyle, ile trzeba, aby kolejne wywołanie było dozwolone.

Przetestuj klasę, tworząc 20 zadań, które próbują wywołać `acquire()` w pętli.

Ustaw limit na przykład na 5 zapytań na sekundę.

## TASK 17 - Łańcuch zależności (challenge)

Stwórz łańcuch zależnych od siebie korutyn:

1. `pobierz_id_uzytkownika(nazwa_uzytkownika)` - zwraca ID po 1 sekundzie.
2. `pobierz_posty(id_uzytkownika)` - zwraca listę ID postów po 1 sekundzie.
3. `pobierz_komentarze(id_postu)` - zwraca listę komentarzy po 1 sekundzie.

Napisz `main`, które:

- dla nazwy użytkownika pobierze jego ID,
- następnie pobierze listę jego postów,
- na końcu pobierze komentarze dla wszystkich jego postów współbieżnie.

Zmierz czas wykonania.

## TASK 18 - Anulowanie zadania (challenge)

Stwórz zadanie, które działa w nieskończonej pętli i co sekundę drukuje:

```text
Pracuję...
```

W głównej korutynie `main` pozwól mu pracować przez 5 sekund, a następnie je anuluj:

```python
task.cancel()
```

W pracującej korutynie obsłuż wyjątek:

```python
asyncio.CancelledError
```

Przed ostatecznym zakończeniem wydrukuj:

```text
Anulowano, sprzątam...
```

## TASK 19 - Generator liczb pierwszych (challenge)

Napisz asynchroniczny generator, który co pewien czas, na przykład co 0.1 sekundy, produkuje kolejną liczbę pierwszą.

W głównej pętli iteruj po generatorze za pomocą:

```python
async for
```

Wypisuj liczby, aż dojdziesz do 100.

## TASK 20 - Timeout dla zadania (challenge)

Napisz korutynę, która śpi przez losowy czas od 1 do 5 sekund.

Uruchom ją z ograniczeniem czasowym na 3 sekundy.

Jeśli korutyna nie zakończy się w tym czasie, program powinien rzucić wyjątek:

```python
asyncio.TimeoutError
```

Obsłuż ten wyjątek i wypisz odpowiedni komunikat.

Wskazówka: użyj:

```python
asyncio.wait_for()
```
