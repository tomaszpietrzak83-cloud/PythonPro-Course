# Lekcja 32 · Async API Studio

20 niezależnych plików z zadaniami, prawdziwy aiohttp i PostgreSQL oraz objaśnienia
każdej niepustej linijki kodu w PL/ENG. Układ i nawigacja rozwijają lekcję 31.

## Uruchomienie

Z głównego katalogu kursu, przy włączonym PostgreSQL:

```powershell
.venv\Scripts\python.exe lessons\lesson32\run_app.py
```

Otwórz [lekcję 32](http://127.0.0.1:8032/). Ponowne uruchomienie launchera
restartuje serwer tej lekcji. `--no-browser` pomija otwieranie przeglądarki.
Logi i PID znajdują się w ignorowanym katalogu `.runtime/`.

Konfiguracja połączenia jest w lokalnym, ignorowanym `.env`; osobna baza nazywa się
`lesson32`. Nie korzystamy z tabel lekcji 19 ani 28. Konfiguracja została przygotowana
skryptem `setup_database.py`, który pobiera lokalne dane z `.env` lekcji 28 i tworzy
bazę, jeśli jej brakuje. Nie wypisuje hasła. Na innym komputerze trzeba przygotować
`DATABASE_URL` z driverem `postgresql+asyncpg` i bazą `lesson32`.

Zależności:

```powershell
.venv\Scripts\python.exe -m pip install -r lessons\lesson32\requirements.txt
```

## Jak się uczyć

1. Przeczytaj oryginalne polecenie i wstęp. Przewidź wynik samodzielnie.
2. Uruchom pokaz. Porównaj status HTTP, body odpowiedzi, wartości i kolejność zdarzeń.
   Panel „Żądanie → odpowiedź” pokazuje wysłane dane i odebrane body bez otwierania
   dziennika, również w widoku skupienia. Krótkie operacje mają czasy w milisekundach.
3. W „Zrozum kod” zacznij od mapy wykonania. Każdy kolejny slajd wyróżnia
   konkretną linijkę rzeczywistego pliku i wyjaśnia jej działanie.
4. Przy `await` nazwij oczekiwaną operację. Przy `return` wskaż odbiorcę wyniku.
   Przy transakcji znajdź początek oraz moment commit lub rollback.
5. Odpowiedz na pytanie bez odsłaniania odpowiedzi. Zmień jedną wartość w przykładzie,
   przewidź konsekwencję i uruchom plik ponownie z terminala.

Kod jest po angielsku; interfejs i objaśnienia mają przełącznik PL/ENG.
Zadania mające ponad 20 slajdów objaśnień udostępniają w „Zrozum kod”
przełącznik **Szybkie / Dokładne**. Tryb szybki to osobno opracowana,
krótka opowieść o blokach kodu (maksymalnie 20 slajdów), przeznaczona do prezentacji.
Domyślnie otwiera się tryb dokładny, zachowujący wcześniejsze objaśnienia każdej linijki.
Tryb szybki wybierasz ręcznie; otwarcie kolejnego zadania lub odświeżenie strony
przywraca dokładny. Przełącznik działa również w trybie ciągłym. Zadanie 14: 16 slajdów szybkich
lub 73 dokładne. Krótsze zadania zachowują dotychczasowy układ.
Do dyspozycji są slajdy, tryb ciągły, większy tekst, pełny ekran, historia pokazów
i odtwarzanie zdarzeń. Objaśnienia po polsku są również dostępne bez aplikacji
w plikach `explanations/task01.md`–`task20.md`.
Przygotowanie silnika, tabel i fabryki sesji opisuje osobno
[przewodnik po bazie i pomocnikach](explanations/database.md).

## Pliki i pokazy

Każde zadanie ma własne rozwiązanie w `examples/task01.py`–`task20.py`.
Przykłady rozwijające CRUD powtarzają potrzebny model i handlery, żeby można było
czytać je niezależnie. `api_support.py` zawiera przygotowanie bazy, lokalny serwer,
klienta pokazu i walidację wejścia. `lab_support.py` mierzy czas i publikuje zdarzenia.
Zakładka „Cały kod” udostępnia także te pliki; zadanie 19 ma dodatkowo `routes.py`.

| Zadania | Mechanizm i sprawdzany efekt |
|---|---|
| 01 | `gather`: 1, 4 i 2 s nakładają się; całość około 4 s. |
| 02–06 | HTML, parametr ścieżki, JSON, query string i POST echo. |
| 07–08 | Model Product i odpowiedź 403 dla admin. |
| 09–11 | INSERT z ID i 201, lista, pojedynczy produkt oraz 404. |
| 12–13 | Publiczne API Coinbase: bieżąca cena BTC i trzy odczyty współbieżnie. |
| 14–15 | PATCH ceny 1299 → 999, DELETE 204 i późniejszy GET 404. |
| 16 | Przelew, blokady wierszy, commit i rzeczywisty rollback po flush. |
| 17 | Strona 2 z limitem 1 zwraca drugi produkt; strona 0 daje 400. |
| 18 | Status odpowiada podczas trzysekundowego oczekiwania czatu. |
| 19 | Rejestracja tras w osobnym module. |
| 20 | JOIN zwraca produkt wraz z nazwą twórcy Anna. |

Przykładowe uruchomienie bez interfejsu:

```powershell
.venv\Scripts\python.exe lessons\lesson32\examples\task16.py
```

Terminal wypisuje zdarzenia JSON, w tym odpowiedzi HTTP. Serwery w pokazach
używają wolnego portu localhost, wysyłają prawdziwe żądania i zamykają się po pokazie.
Każdy pokaz bazy otrzymuje własny schemat `demo_...` w `lesson32`; jest usuwany
przy normalnym zakończeniu, również po obsłużonym błędzie HTTP.
Wymuszone zabicie procesu może pozostawić schemat demonstracyjny w tej bazie.

Zadania 12–13 wymagają internetu. Stare adresy z polecenia zastąpiono publicznym
Coinbase; błąd sieci nie jest zamieniany na fikcyjną cenę. Zadanie 18 symuluje AI
przez `asyncio.sleep(3)`. Specjalna kwota 13 w zadaniu 16 to jawny punkt awarii
do nauki rollbacku, a nie reguła biznesowa. Dane i komunikaty przykładów oraz
niektóre nazwy parametrów przetłumaczono na angielski. Zadanie 19 przekazuje
handlery do `setup_routes` jawnie, aby uniknąć cyklicznych importów.

## Sprawdzenie i zmiany materiałów

```powershell
.venv\Scripts\python.exe lessons\lesson32\test_lesson32.py
```

Testy wykonują 18 lokalnych programów, sprawdzają konkretne body odpowiedzi,
rollback, 12 równoczesnych przelewów, walidację, CSRF i kompletność objaśnień.
Test publicznych API jest opcjonalny:

```powershell
$env:LESSON32_LIVE_API = "1"
.venv\Scripts\python.exe lessons\lesson32\test_lesson32.py
Remove-Item Env:LESSON32_LIVE_API
```

Po własnej edycji `taskXX.py` można od razu uruchomić go w terminalu.
Aplikacja wymaga spójnego kodu i objaśnień: przejrzyj odpowiednie wpisy
w `line_notes.py`, a następnie uruchom `create_material.py` i odśwież stronę.
Nie uruchamiaj `build_examples.py` po własnych zmianach: to skrypt autorski,
który odtwarza bazowe rozwiązania i nadpisuje pliki zadań.

Dokumentacja: [aiohttp server](https://docs.aiohttp.org/en/stable/web_reference.html),
[aiohttp client](https://docs.aiohttp.org/en/stable/client_reference.html),
[SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html),
[Coinbase prices](https://docs.cdp.coinbase.com/coinbase-app/track-apis/prices).
