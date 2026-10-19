# Lekcja 30 · Concurrency Studio

Kod przykładów jest po angielsku: nazwy, komentarze, dane i komunikaty
demonstracji. Materiały edukacyjne i interfejs zachowują przełącznik PL/ENG.

Osobista aplikacja dydaktyczna do wszystkich 20 zadań z `tasks.md`.
Interfejs Django prezentuje rzeczywiste wykonanie przykładów Pythona, kod
źródłowy i objaśnienia PL/ENG. Służy do nauki i udostępniania ekranu podczas
prezentacji. Nie wymaga konta, bazy danych, Celery, Redisa ani zewnętrznego API.

## Uruchomienie

Z głównego katalogu **Python Pro Course**:

```powershell
.venv\Scripts\python.exe lessons\lesson30\run_app.py
```

Skrypt otwiera [aplikację na porcie 8030](http://127.0.0.1:8030/).
Można też użyć istniejącego launchera kursu:

```powershell
python run_lesson.py lessons/lesson30/run_app.py
```

Zależności są już dostępne we wspólnym środowisku kursu. Na nowej instalacji:

```powershell
.venv\Scripts\python.exe -m pip install -r lessons\lesson30\requirements.txt
```

Ponowne uruchomienie zatrzymuje poprzedni serwer **tej lekcji** i jego procesy
potomne, następnie startuje świeżą wersję. Tożsamość procesu jest sprawdzana
przez ścieżkę i czas utworzenia. Kontenery poprzedniego serwera identyfikuje
osobna etykieta. Inne lekcje i kontenery pozostają niezależne.
Log serwera i jego PID znajdują się w `.runtime/`. Style i skrypt otrzymują
wersję na podstawie daty plików, aby przeglądarka pobierała aktualne zmiany.

## Nauka i prezentowanie

- Kafelki: 20 zadań, po cztery w rzędzie na szerokim ekranie.
- Zadanie otwiera się od **Treści zadania**, przed **Wstępem**. Pierwsza zakładka
  zawiera pełne polecenie z `tasks.md` w PL/ENG oraz osobną informację o adaptacji
  do aplikacji. Długie polecenia są podzielone na krótkie strony z przyciskiem Dalej.
- **Wstęp** zawiera nowe pojęcia dla danego tematu.
- **Obserwuj działanie**: gotowy wariant, uruchomienie, rzeczywiste zdarzenia,
  wyniki i osobna interpretacja. Warianty z parametrami mają listę oraz
  opcjonalne pole własnej wartości. Domyślny pokaz nie wymaga pisania.
- **Zrozum kod**: najpierw sens bloku, potem jego instrukcje. Pojedyncza
  instrukcja nie dostaje dwóch powtarzających się slajdów. Instrukcje
  wielowierszowe są omawiane jako całość; nagłówek pokazuje ich dokładny zakres.
- **Cały kod**: rzeczywisty plik zadania oraz osobno `lab_support.py`, czyli
  mała warstwa rejestrowania zdarzeń. Przycisk kopiowania kodu.
- **Pytania**: dwa pytania dotyczące mechanizmu, ukryte odpowiedzi i próba
  samodzielnego opowiedzenia przebiegu przed prezentacją.
- PL/ENG, Slajdy/Tryb ciągły i większy tekst są zapamiętywane lokalnie.
  Nie ma kont, ocen, oznaczeń ukończenia ani pamiętania ostatniego slajdu.
- Strzałki klawiatury **← / →** przechodzą między slajdami. W polach i na
  kontrolkach zachowują własną funkcję. Lewy pasek otwiera listę zadań.
- W trybie slajdów nawigacja zajmuje stałe miejsce na dole ekranu. Nagłówki
  i odstępy są zwarte; kod i komentarz pozostają obok siebie na laptopie.
  Nie trzeba przewijać strony do przycisku Dalej. Pełny kod i rozwijane
  odpowiedzi mogą przewijać się wewnątrz panelu; tryb ciągły przewija się normalnie.
- **⛶** przełącza pełny ekran, **A+** zwiększa tekst. Kod ma domyślnie 18 px,
  tekst 20 px, brak przewijania na boki; pełny kod pokazuje minimum 15 wierszy.

Uruchomienie przełącza na **widok skupiony**, z większą przestrzenią dla
obserwacji. Przycisk **Skup widok / wróć** przywraca menu i opis. Można
zatrzymać pokaz albo powtórzyć go z tymi samymi ustawieniami. Historia pokazów
pozwala porównać wybrane warianty w obrębie bieżącej sesji strony.

**Odtwórz ślad** i suwak odtwarzają wcześniej zapisane zdarzenia. Nie zatrzymują
działającego programu i nie uruchamiają go ponownie. Do analizy kodu służy
osobna, spokojna nawigacja po instrukcjach; nie udajemy debuggera, który potrafi
bez wpływu na pomiary zatrzymać wszystkie wątki.

## Co dokładnie pokazuje wizualizacja

Przykłady emitują JSON z czasem `perf_counter`, PID, nazwą wątku i rodzajem
zdarzenia. UI aktualizuje odczyt co około 300 ms. Pasek jest przedziałem
START–KONIEC funkcji/bloku, **wliczając oczekiwanie**. Nie jest wykresem zajęcia
rdzeni. Bardzo krótki pasek ma minimalną szerokość dla widoczności; czas
numeryczny pochodzi z rzeczywistego pomiaru.

Przy zapytaniach AI tory grupujemy według faktycznych wątków puli; przy
obrazach według procesu. Kolor rozróżnia tory, a podpisy identyfikują
uczestników. W logu są wartości, kolejność obserwowanych zdarzeń i PID.
Logi procesów mogą dotrzeć w innej kolejności niż wykonano operacje; UI
porządkuje zdarzenia według ich znaczników czasu, ale samo logowanie również
ma koszt i nie stanowi śledzenia wszystkich instrukcji interpretera.

Jednocześnie działa jeden eksperyment, aby nie zakłócać pomiarów innymi
pokazami. Limit wykonania to 180 s. Dane i pliki demonstracyjne są lokalne;
przykłady plikowe tworzą i sprzątają własne katalogi tymczasowe. Historia
w przeglądarce znika po odświeżeniu, a serwer zachowuje najwyżej 30 pokazów.

## Opcjonalny Docker

**Domyślnie wszystkie zadania działają na Windowsie we wspólnym Pythonie.**
Docker jest alternatywą, nie wymogiem uruchomienia strony. Przed pokazem
w tym trybie **włącz Docker Desktop z silnikiem Linux**. Następnie jednorazowo:

```powershell
.venv\Scripts\python.exe lessons\lesson30\run_app.py --build-docker
```

Budowanie pobiera oficjalny `python:3.12-slim` i tworzy lokalny obraz
`lesson30-python:local`. Po zakończeniu wybierz **Docker** w polu środowiska.
Panel **Zasoby / Resources** pokazuje dostępność silnika i obrazu, wersję
lokalnego Pythona, liczbę logicznych CPU i stan lokalnego GIL.

Każdy pokaz w Dockerze tworzy osobny kontener z ograniczeniem **2 CPU, 2 GB
RAM i 64 procesów/wątków systemowych**. System plików obrazu jest tylko do
odczytu; `/tmp` ma osobny obszar do 512 MB. Aktualny katalog `examples` jest
podłączony tylko do odczytu, więc wykonywany kod odpowiada kodowi w UI także
po edycji. Kontener nie ma dostępu do Internetu; lokalny crawler działa przez
loopback wewnątrz kontenera. Kontener jest usuwany po pokazie lub zatrzymaniu.

Docker zużywa zasoby Twojego komputera i swojej maszyny wirtualnej. Limity
mogą zmieniać wyniki benchmarków. Windows stosuje `spawn`; Python 3.12 w tym
kontenerze Linux domyślnie stosuje `fork`. Koszt startu procesów będzie inny.
Standardowy Python 3.12 używany tutaj ma GIL. Specjalne nowsze buildy
free-threaded mogą działać inaczej — materiał nie zakłada, że każdy Python
zawsze ma włączony GIL.

Jeśli Docker jest wyłączony lub brakuje obrazu, UI pokaże komunikat.
Nie przełącza po cichu pokazu na inne środowisko. Serwer strony pozostaje
lokalny na Windowsie, również przy kontenerowym wykonywaniu przykładów.

## Mapa zadań i świadome adaptacje

Każdy plik jest samodzielnym rozwiązaniem. Uruchomienie z terminala wypisuje
zdarzenia JSON, które w aplikacji są wizualizowane. Domyślne wejścia znajdują
się w kodzie; UI przekazuje wybrane wartości przez `LESSON30_INPUT`.

| Zadanie / plik | Nowy cel i obserwacja |
|---|---|
| 01 · `examples/task01.py` | Pierwszy wątek, 3 s oczekiwania i `join` głównego. |
| 02 · `examples/task02.py` | Pięć numerów, `args=(numer,)`, osobne pętle start/join. Sleep 0,6 s to jawny dodatek obserwacyjny. |
| 03 · `examples/task03.py` | Trzy czekania po 2 s: około 6 s sekwencyjnie kontra 2 s współbieżnie. |
| 04 · `examples/task04.py` | Lista 200 000 oraz kontrolowany utracony przyrost. Barrier wymusza dwa odczyty przed zapisem. |
| 05 · `examples/task05.py` | Ta sama lista z Lock oraz licznik kończący na 2; sekcje posiadania Lock nie nakładają się. |
| 06 · `examples/task06.py` | Proces liczy 10!, osobny PID, ochrona `__main__`. |
| 07 · `examples/task07.py` | Potęgowanie: gotowe 5³ lub 8³, opcjonalna własna podstawa. |
| 08 · `examples/task08.py` | Imię przez multiprocessing.Queue. Formularz zastępuje `input` potomka bez interaktywnej konsoli. |
| 09 · `examples/task09.py` | Cztery sumy częściowe, krótka sekcja aktualizacji wspólnego wyniku, kontrola wzorem. |
| 10 · `examples/task10.py` | Trzy przygotowane pliki .txt: zliczanie całych słów, UTF-8, casefold. |
| 11 · `examples/task11.py` | Producent co 1 s i obsługa co 1,5 s; 10 s produkcji, potem skończenie bieżącej pracy i odłożenie reszty. |
| 12 · `examples/task12.py` | Ta sama suma kwadratów dwa razy: sekwencyjnie, w dwóch wątkach i dwóch procesach. |
| 13 · `examples/task13.py` | 100 liczb ze stałym ziarnem; pula 2 procesów i map zwracający True/False w kolejności wejścia. |
| 14 · `examples/task14.py` | Rzeczywiste kopiowanie 4 plików po 2 MB; kontrola SHA256 po join. |
| 15 · `examples/task15.py` | Lokalna witryna 4 stron, prawdziwe HTTP, jawne 0,35 s opóźnienia serwera; deduplikacja i limit 50 URL. |
| 16 · `examples/task16.py` | SHA256 czterech plików w puli; odczyt blokami 65 536 bajtów. |
| 17 · `examples/task17.py` | Pipe w obie strony: lista → suma i średnia; limit oczekiwania na odpowiedź. |
| 18 · `examples/task18.py` | 5 wpłat i 5 wypłat; Lock chroni sprawdzenie oraz zmianę. Saldo porównane z historią. |
| 19 · `examples/task19.py` | 20 opinii, symulacja API bez wysyłki; gotowe pule 5/10/1 wątków, Future i as_completed. |
| 20 · `examples/task20.py` | 10 obrazów, rzeczywiste mnożenie pikseli, porównanie wyników i czasu obejmującego IPC. |

Zadania 09 i 12 mają domyślnie mniejszy rozmiar, aby prezentacja była szybka;
pełne **10 milionów** i **20 milionów** są na liście. Zadanie 20 ma domyślnie
10 obrazów **300×300**, a pełne **1000×1000** też jest gotowym wariantem.
Pełne obrazy mogą zużyć ponad 1 GB. Przy prostym mnożeniu procesy często są
wolniejsze z powodu przesyłania list. Nie dodajemy sztucznych obliczeń ani
opóźnień, aby wymusić „ładniejszy” wynik benchmarku.

`sleep` w zadaniach 03 i 19 symuluje oczekiwanie, nie intensywne obliczenia.
Zadania „AI” nie wywołują modelu. W 18 stałe kwoty i niewielkie opóźnienia
pomagają obserwować stan; nie gwarantują konkretnej kolejności operacji.
Poprawny invariant salda jest ważniejszy od identycznego przebiegu.

## Podświetlanie i kontrola zgodności z kodem

Komentarz `# @step nazwa` znajduje się **bezpośrednio przed** objaśnianą
instrukcją. Parser AST wyznacza jej początek i koniec z aktualnego pliku.
Dla bloków szczegółowy slajd nagłówka podświetla nagłówek, nie całe ciało;
przypisanie czy wywołanie wielowierszowe podświetla całą instrukcję.
Nie wyszukujemy pierwszego podobnego napisu i nie przechowujemy stałych
offsetów, które przesuwają się po formatowaniu.

Każdy komentarz slajdu jest przypisany jawnie do sprawdzonego fragmentu w
`reviewed_slides.json`: 59 bloków i 70 szczegółowych instrukcji. Opisy nie są
dobierane automatycznie na podstawie pierwszej znalezionej metody. Rejestr
zawiera też faktyczny tekst kodu, aby późniejsza zmiana instrukcji lub komentarza
wymagała ponownego przeglądu zamiast cicho zachować niepasujące objaśnienie.
Przesunięcie fragmentu do innego numeru linii nadal obsługuje parser AST.
Kod z kolorowaniem, opisy i zakresy są dostarczane razem w jednej odpowiedzi,
z tej samej wersji źródła. UI nie pobiera osobno nowszego pliku do starszych
slajdów. Odpowiedzi z materiałem mają wyłączone przechowywanie w cache.

Test sprawdza wszystkie znaczniki, jednoznaczność ich nazw, zgodność zakresów
z AST, zakresy szczegółowych instrukcji oraz zgodność kodu zwracanego UI
z rzeczywistym plikiem. Brakujący lub błędny znacznik przerywa ładowanie
materiału zamiast wskazywać przypadkową linię. Źródła przykładów sformatowano
do 80 znaków; w UI długie widoczne fragmenty dodatkowo się zawijają.

## Sprawdzenie

```powershell
.venv\Scripts\python.exe lessons\lesson30\test_lesson30.py
```

Obejmuje wszystkie 20 rzeczywistych wykonań, wyniki wyścigu i Lock, zgodność
sum i obrazów, pliki, komunikację procesów, mapowanie kodu, wejścia i CSRF.
Wymaga możliwości tworzenia plików tymczasowych i lokalnego serwera HTTP.

Sprawdzenie pełnego przepływu HTTP → wykonawca → UI/API, przy działającym serwerze:

```powershell
.venv\Scripts\python.exe lessons\lesson30\verify_live.py --backend native
.venv\Scripts\python.exe lessons\lesson30\verify_live.py --backend docker
```

Raporty są w `.runtime/verification.json`, `live-native.json` i `live-docker.json`.
Testy nie zakładają, że procesy zawsze wygrywają; porównują poprawność wyników.

## Pliki projektu

- `run_app.py`: uruchamianie, restart, otwieranie przeglądarki i budowanie obrazu.
- `app.py`: lokalny serwer Django, walidacja, procesy i odbiór zdarzeń.
- `curriculum.py`: osobne cele, interpretacje, pytania, warianty i powiązania z kodem.
- `teaching.py`, `code_notes.py`: nowe pojęcia i szczegółowe wyjaśnienia instrukcji.
- `reviewed_slides.json`: sprawdzone pary kod–komentarz dla wszystkich slajdów.
- `examples/task01.py`–`task20.py`: właściwe rozwiązania.
- `examples/lab_support.py`: obserwacja i pomiary; wspólny pomocnik przykładów.
- `static/`, `templates/`: grafitowy interfejs z turkusem i fioletem.
- `Dockerfile`, `.dockerignore`: opcjonalne środowisko Python/Linux.

Materiały źródłowe kursu `lesson-30.md` i `tasks.md` pozostają dostępne.
Nie zmieniono lekcji 29 ani innych istniejących aplikacji kursu.

## Dokumentacja mechanizmów

- [threading](https://docs.python.org/3/library/threading.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [queue](https://docs.python.org/3/library/queue.html)
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [Python free-threaded](https://docs.python.org/3/howto/free-threading-python.html)
