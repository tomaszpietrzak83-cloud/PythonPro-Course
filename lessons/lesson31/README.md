# Lekcja 31 · Asyncio Studio

Lokalna aplikacja do nauki i prezentowania wszystkich 20 zadań z `tasks.md`.
Interfejs i objaśnienia są dostępne w PL/ENG. Kod przykładów jest po angielsku.

## Uruchomienie

Z głównego katalogu kursu:

```powershell
.venv\Scripts\python.exe lessons\lesson31\run_app.py
```

Aplikacja otwiera http://127.0.0.1:8031/.
Ponowne uruchomienie restartuje serwer tej lekcji. `--no-browser` pomija
otwarcie przeglądarki. Logi i identyfikator serwera znajdują się w `.runtime/`.
Launcher sprawdza ścieżkę programu i czas utworzenia procesu przed restartem.

Zależności są dostępne we wspólnym środowisku kursu. Dla nowej instalacji:

```powershell
.venv\Scripts\python.exe -m pip install -r lessons\lesson31\requirements.txt
```

## Co przejęto z lekcji 29 i 30

W lekcji 29 użyteczne są osobne cele zadań, powiązanie komentarzy z kodem,
pytania z ukrytymi odpowiedziami i prezentowanie rzeczywistych efektów pracy.
Uruchamianie Celery, brokera i workerów odpowiada jednak innemu tematowi.

Lekcja 30 lepiej pasuje do nauki początkującego: polecenie przed wstępem,
gotowy pokaz bez wpisywania danych, oś czasu, interpretacja wyniku,
analiza fragmentów, pełne źródło i próba opowiedzenia mechanizmu.
Z niej pochodzą podstawy serwera oraz nawigacji, slajdów, historii i odtwarzania.

Lekcja 31 zachowuje ten układ i rozszerza dydaktykę:

- **Treść zadania** zachowuje oryginalne polskie polecenia. Osobna informacja
  wyjaśnia adaptacje. Angielski wariant przekazuje te same wymagania.
- **Wstęp** objaśnia cel oraz najważniejszy mechanizm konkretnego zadania.
- **Obserwuj działanie** uruchamia prawdziwy program. Pokazuje tory,
  zmierzone czasy, wartości i dziennik. Można zatrzymać pokaz, powtórzyć go
  albo odtworzyć zapis zdarzeń suwakiem.
- **Zrozum kod** ma 218 slajdów łącznie: wejście do programu, cele funkcji,
  przebieg operacji oraz osobne objaśnienia wywołanych metod i funkcji.
  Pokazuje dokładne argumenty z kodu, sposób działania, zwracane wartości
  i częste pułapki. Ponowne użycie tej samej metody w jednej funkcji nie
  tworzy kolejnego identycznego objaśnienia.
- Objaśnienia obejmują również podstawy: parametry, słowniki, `range`,
  listy składane, rozpakowanie `*`, `return`, `yield`, `self`,
  `try/except/finally`, `async with` i różnicę między korutyną a Task.
- **Cały kod** udostępnia plik zadania i osobno pomocnik obserwacji.
- **Pytania** mają odpowiedzi ukryte, pytanie „co się zmieni, jeśli…” oraz
  podpowiedź do samodzielnej wypowiedzi przed publicznością.

Nowa oprawa wykorzystuje przygaszony granat i petrol bez czarnych powierzchni:
jasne teksty, miętowe akcje, bursztynowe akcenty i granatowy edytor. Pełny ekran, większy tekst, strzałki
←/→ i tryb ciągły służą prezentacji. Wybór języka, wielkości tekstu i trybu
jest zapamiętywany w przeglądarce niezależnie od lekcji 30.

## Mapa pokazów

| Zadanie | Rzeczywisty rezultat i ważna obserwacja |
|---|---|
| 01 | Komunikat z pierwszej korutyny; obiekt korutyny a jej wykonanie. |
| 02 | Liczby 1–3 co sekundę; granice `range`. |
| 03 | Oczekiwania 2 s oraz 1 s po kolei, razem około 3 s. |
| 04 | Te same oczekiwania przez `gather`, razem około 2 s. |
| 05 | Wynik 5³ = 125 po 2 s, przekazany przez `return` i `await`. |
| 06 | Fikcyjny słownik pogody po 1,5 s. |
| 07 | Trzy fikcyjne miasta współbieżnie, lista słowników. |
| 08 | Pięć symulowanych pingów; kolejność ukończeń a kolejność wyników. |
| 09 | Prawdziwe lokalne HTTP przez aiohttp, statusy 200/404/503. |
| 10 | Trzy odliczania 5/3/7 s, wspólny czas około 7 s. |
| 11 | Dziesięć liczb 1–100, opóźnienia 2–5 s i ich suma. |
| 12 | Pięć Task, `FIRST_COMPLETED`, anulowanie reszty i odebranie zakończeń. |
| 13 | Prawdziwy serwer i klient TCP echo; kontrola identycznych bajtów. |
| 14 | 20 liczb co 0,5 s, dwóch konsumentów, potwierdzenia i kontrola kompletności. |
| 15 | Prawdziwy wspólny plik, pięć wierszy przez aiofiles i Lock. |
| 16 | 20 zadań × dwie próby, 40 zezwoleń, limit 5 w kroczącym oknie 1 s. |
| 17 | ID → posty → komentarze współbieżnie, około 3 s. |
| 18 | Worker przez 5 s, anulowanie, sprzątanie i kontrola `cancelled()`. |
| 19 | Async generator: 25 liczb pierwszych do 100, największa 97. |
| 20 | Warianty 1 s / 5 s / losowo 1–5 s, limit 3 s i obsługa timeout. |

### Adaptacje i dokładność obserwacji

Pogoda, ping i opóźnienia obliczeń/API są **symulacjami** przez sleep.
Nie korzystamy z zewnętrznego API ani modelu AI. HTTP i TCP naprawdę używają
sieci lokalnej. Port HTTP jest wolnym portem systemowym; TCP ma wariant
wolnego portu oraz `8888` z polecenia. Wiadomość TCP kończy się nową linią.
Automatyczny klient umożliwia pokaz bez dodatkowej konsoli, a serwer kończy
się po wymianie wiadomości.

Kolejka ma dwa sygnały None do zakończenia konsumentów i jawne 0,7 s
symulowanego przetwarzania. Rate limiter wykonuje skończoną liczbę prób.
Nie jest rozproszonym limiterem i nie gwarantuje sprawiedliwości.
W timeout gotowe czasy pokazują oba rozstrzygnięcia; losowanie jest osobnym
wariantem. Plik z zadania 15 jest tymczasowy: treść zostaje w logu pokazu.
aiofiles deleguje operacje plikowe do puli wątków.

Oś czasu pochodzi z `perf_counter` i zdarzeń programu. Paski obejmują
oczekiwanie, nie pokazują obciążenia rdzeni ani wszystkich instrukcji.
Całkowity czas obejmuje main i sprzątanie, bez startu interpretera. Logowanie
ma koszt. Nie wymagamy idealnie równych czasów ani kolejności zdarzeń
gotowych jednocześnie. Odtwarzanie pokazuje zapis, nie jest debuggerem.

Jednocześnie działa jeden pokaz. Limit wykonania wynosi 180 s. Serwer
zachowuje najwyżej 30 pokazów; historia strony znika po odświeżeniu.
Przycisk Stop kończy proces pokazu; zadania 12/18/20 osobno demonstrują
kooperacyjne anulowanie przez asyncio.

## Źródła i objaśnienia

- `examples/task01.py`–`task20.py`: samodzielne programy, możliwe do
  uruchomienia również w terminalu. Ich wynik to zdarzenia JSON.
- `examples/lab_support.py`: obserwacja, wejście i pomiar; osobno od asyncio.
- `material.json`: sprawdzona wersja kodu z opisami bloków PL/ENG.
- `create_material.py`: autorskie materiały do regenerowania źródeł i opisów.
  Uruchomienie nadpisuje przykłady: zmiany do regeneracji wprowadzaj tutaj.
- `curriculum.py`: kontrola zgodności kodu, zakresy AST, pytania i warianty.
- `method_notes.py`: objaśnienia API, argumentów i wartości zwracanych.
- `assignments.py`: podział oryginalnych poleceń na strony i angielski wariant.
- `app.py`: serwer Django, CSRF, walidacja, wykonanie i odbiór zdarzeń.
- `static/theme.css`: nowa szata graficzna; `studio.css` stanowi bazę układu.

Zmiana kodu przykładu bez przeglądu materiału zatrzymuje ładowanie zamiast
pokazywać objaśnienia do starego kodu. API wysyła kod, zakresy, kolorowanie
i objaśnienia w jednym spójnym odczycie, bez cache.

Nie zapisujemy statystyk błędów ucznia: uruchomienie gotowego przykładu nie
jest dowodem popełnienia błędu. W tej aplikacji ćwiczeniem jest przewidywanie
wyników i wyjaśnianie kodu własnymi słowami.

## Sprawdzenie

```powershell
.venv\Scripts\python.exe lessons\lesson31\test_lesson31.py
```

Test uruchamia wszystkie 20 programów i dodatkowo timeout 5 s, sprawdza
wyniki, kolejkę, plik, TCP/HTTP, limit szybkości, anulowanie, liczby pierwsze,
zgodność objaśnień ze źródłem, walidację i rzeczywisty przepływ API do procesu.
Trwa około minuty. Raport wyników: `.runtime/verification.json`.

Dokumentacja do dalszej nauki:

- [Korutyny, Task, gather, wait i timeout](https://docs.python.org/3/library/asyncio-task.html)
- [Kolejki asyncio](https://docs.python.org/3/library/asyncio-queue.html)
- [Strumienie TCP](https://docs.python.org/3/library/asyncio-stream.html)
- [Klient aiohttp](https://docs.aiohttp.org/en/stable/client_quickstart.html)
- [aiofiles i delegowanie operacji plikowych](https://github.com/Tinche/aiofiles)
