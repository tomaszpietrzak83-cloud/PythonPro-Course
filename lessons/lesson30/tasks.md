# Lesson 30 - Zadania

## TASK 01 - Zadanie 1 - Pierwszy wątek (proste)

Napisz program, który tworzy i uruchamia jeden wątek.

Wątek powinien:

- odczekać 3 sekundy,
- wydrukować komunikat:

```text
Wątek zakończył pracę!
```

Główny program powinien w tym czasie wyświetlić:

```text
Główny program czeka na wątek...
```

## TASK 02 - Zadanie 2 - Wiele wątków (proste)

Stwórz program, który uruchamia 5 wątków.

Każdy wątek powinien otrzymać jako argument swój numer od 1 do 5 i wydrukować komunikat:

```text
Jestem wątkiem numer [numer]
```

Upewnij się, że główny program czeka na zakończenie wszystkich wątków.

## TASK 03 - Zadanie 3 - Symulacja pobierania danych (proste)

Napisz funkcję:

```python
pobierz_dane(id_danych)
```

Funkcja ma symulować pobieranie danych przez:

```python
time.sleep(2)
```

Uruchom tę funkcję dla 3 różnych `id_danych` sekwencyjnie i zmierz czas.

Następnie zrób to samo, ale uruchom każdą funkcję w osobnym wątku i również zmierz czas.

Porównaj wyniki.

## TASK 04 - Zadanie 4 - Problem wyścigu (proste)

Napisz program z globalną listą.

Stwórz 2 wątki:

- jeden dodaje do listy 100 tysięcy razy liczbę `1`,
- drugi dodaje do listy 100 tysięcy razy liczbę `2`.

Po zakończeniu obu wątków sprawdź długość listy.

Czy wynosi ona 200 tysięcy?

Uruchom program kilka razy.

<p style="color:red"><strong>Komentarz mentora:</strong> W CPythonie samo `list.append()` często zachowuje się bezpiecznie dla takiego testu, więc to ćwiczenie może nie pokazać problemu wyścigu. Lepszym przykładem race condition jest wspólny licznik i operacja `licznik += 1`.</p>

## TASK 05 - Zadanie 5 - Naprawa wyścigu (proste)

Zmodyfikuj program z zadania 4, dodając `threading.Lock`, aby operacja dodawania do listy była bezpieczna.

Sprawdź, czy teraz długość listy jest zawsze poprawna.

## TASK 06 - Zadanie 6 - Pierwszy proces (proste)

Napisz program, który uruchamia osobny proces.

Proces powinien obliczyć silnię liczby `10` i wydrukować wynik.

## TASK 07 - Zadanie 7 - Proces z argumentem (proste)

Stwórz funkcję:

```python
potega(liczba, pot)
```

Uruchom ją w nowym procesie, przekazując:

```python
liczba = 5
pot = 3
```

Proces powinien wydrukować wynik.

## TASK 08 - Zadanie 8 - Komunikacja z procesem (proste)

Stwórz proces, który:

- prosi użytkownika o podanie imienia przez `input()`,
- wysyła to imię do procesu nadrzędnego za pomocą `multiprocessing.Queue`.

Proces nadrzędny odbiera imię i drukuje:

```text
Witaj, [imię]!
```

## TASK 09 - Zadanie 9 - Sumowanie z wątkami i blokadą (challenge)

Napisz program, który sumuje liczby w dużej liście, na przykład 10 milionów elementów.

Podziel listę na 4 części i każdą część zsumuj w osobnym wątku.

Wyniki częściowe dodawaj do globalnej zmiennej `suma_calkowita`, zabezpieczając dostęp do niej za pomocą `threading.Lock`.

## TASK 10 - Zadanie 10 - Równoległe liczenie słów w plikach (challenge)

Napisz program, który liczy łączną liczbę wystąpień danego słowa we wszystkich plikach `.txt` w bieżącym katalogu.

Każdy plik powinien być przeszukiwany w osobnym wątku.

Wyniki zliczania z każdego wątku powinny być bezpiecznie dodane do wspólnego licznika.

## TASK 11 - Zadanie 11 - Producent i konsument (challenge)

Zaimplementuj klasyczny problem producenta-konsumenta.

Stwórz współdzieloną, bezpieczną wątkowo kolejkę:

```python
import queue

q = queue.Queue()
```

Wymagania:

- producent to wątek, który co sekundę dodaje do kolejki nowy element, na przykład losową liczbę,
- konsument to wątek, który co 1.5 sekundy pobiera element z kolejki i go drukuje,
- program powinien działać przez 10 sekund.

## TASK 12 - Zadanie 12 - GIL w praktyce (CPU-bound) (challenge)

Napisz funkcję, która wykonuje intensywne obliczenia, na przykład:

```python
sum(i * i for i in range(20_000_000))
```

Zmierz czas wykonania:

1. tej funkcji dwa razy pod rząd,
2. tej funkcji dwa razy jednocześnie w dwóch różnych wątkach,
3. tej funkcji dwa razy jednocześnie w dwóch różnych procesach.

Porównaj wyniki i wyjaśnij je w komentarzu w kodzie.

## TASK 13 - Zadanie 13 - Pula procesów do przetwarzania danych (challenge)

Stwórz listę 100 losowych liczb od 1 do 1000.

Użyj `multiprocessing.Pool`, aby stworzyć pulę procesów, która dla każdej liczby sprawdzi, czy jest ona liczbą pierwszą.

Funkcja `pool.map` powinna zwrócić listę wartości `True` / `False`.

Wydrukuj, ile liczb pierwszych znalazłeś.

## TASK 14 - Zadanie 14 - Kopiowanie plików w tle (challenge)

Napisz program, który kopiuje wszystkie pliki z jednego katalogu do drugiego.

Każdy plik powinien być kopiowany w osobnym wątku.

Wyświetlaj postęp, na przykład:

```text
Kopiowanie pliku X...
Ukończono kopiowanie pliku X
```

Program główny powinien zakończyć się dopiero po skopiowaniu wszystkich plików.

## TASK 15 - Zadanie 15 - Prosty web crawler (challenge)

Napisz prosty crawler, który zaczyna od jednego adresu URL.

Program powinien:

- pobierać zawartość strony,
- znajdować wszystkie linki do tej samej domeny,
- dodawać je do kolejki do odwiedzenia,
- używać puli wątków do jednoczesnego pobierania stron z kolejki,
- ograniczyć liczbę odwiedzonych stron, na przykład do 50,
- używać bezpiecznej wątkowo kolejki i zbioru `set` do przechowywania już odwiedzonych linków.

## TASK 16 - Zadanie 16 - Równoległe haszowanie plików (challenge)

Napisz skrypt, który oblicza skrót SHA256 dla każdego pliku w danym katalogu.

Użyj `multiprocessing.Pool`, aby rozdzielić listę plików między dostępne rdzenie procesora.

Program powinien na końcu wydrukować słownik, gdzie:

- kluczem jest nazwa pliku,
- wartością jest jego hash.

## TASK 17 - Zadanie 17 - Komunikacja dwukierunkowa (Pipe) (challenge)

Użyj `multiprocessing.Pipe` do stworzenia dwukierunkowej komunikacji.

Proces nadrzędny wysyła do procesu potomnego listę liczb.

Proces potomny:

- oblicza ich sumę,
- oblicza ich średnią,
- odsyła krotkę z wynikami:

```python
(suma, srednia)
```

Proces nadrzędny odbiera wyniki i je drukuje.

## TASK 18 - Zadanie 18 - Symulacja wyścigu w banku (challenge)

Stwórz klasę `KontoBankowe` z atrybutem `saldo`.

Stwórz metody:

- `wplac(kwota)`
- `wyplac(kwota)`

Metoda `wyplac` powinna sprawdzać, czy na koncie jest wystarczająco środków.

Uruchom 10 wątków:

- 5 wpłaca losowe kwoty,
- 5 wypłaca losowe kwoty.

Zabezpiecz metody za pomocą blokady, aby saldo na koniec było prawidłowe.

## TASK 19 - Zadanie 19 - AI: Równoległa analiza sentymentu (symulacja) (challenge)

Stwórz listę 20 przykładowych zdań, czyli opinii o produkcie.

Napisz funkcję:

```python
analizuj_sentyment(zdanie)
```

Funkcja ma symulować zapytanie do API AI przez:

```python
time.sleep(random.uniform(0.5, 2.0))
```

Funkcja ma zwracać losowo:

- `Pozytywny`
- `Negatywny`
- `Neutralny`

Użyj puli wątków `concurrent.futures.ThreadPoolExecutor`, aby przeanalizować wszystkie zdania i zebrać wyniki.

Zmierz czas wykonania.

## TASK 20 - Zadanie 20 - AI: Równoległe przetwarzanie obrazów (symulacja) (challenge)

Załóżmy, że masz do przetworzenia 10 obrazów reprezentowanych jako listy `1000x1000` losowych liczb.

Napisz funkcję:

```python
zastosuj_filtr(obraz)
```

Funkcja ma iterować po każdym pikselu i wykonywać na nim prostą operację matematyczną, na przykład:

```python
pixel * 1.1
```

To symuluje zadanie CPU-bound.

Użyj `multiprocessing.Pool`, aby przetworzyć wszystkie 10 obrazów równolegle i zmierz czas.

Porównaj go z czasem wykonania sekwencyjnego.
