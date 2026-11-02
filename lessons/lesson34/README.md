# Lekcja 34 · Realtime Studio

20 osobnych rozwiązań WebSocket / GraphQL, rzeczywiste pokazy sieciowe i interaktywny kod z objaśnieniami PL / ENG.

## Uruchomienie

Z katalogu kursu, tak samo jak lekcję 33:

```powershell
.venv/Scripts/python.exe lessons/lesson34/run_app.py
```

Launcher automatycznie wybiera **osobne środowisko lekcji 34** i otwiera <http://127.0.0.1:8034/>. Sprawdza wczytanie wszystkich materiałów przed zgłoszeniem sukcesu. Log serwera: `.runtime/server.log`. Ponowne uruchomienie restartuje wyłącznie proces należący do tej lekcji.

Pierwsza instalacja na innym komputerze (Python 3.12+):

```powershell
.venv/Scripts/python.exe -m venv lessons/lesson34/.venv
lessons/lesson34/.venv/Scripts/python.exe -m pip install -r lessons/lesson34/requirements.txt
lessons/lesson34/.venv/Scripts/python.exe lessons/lesson34/run_app.py
```

Osobne środowisko zapobiega konfliktom wersji Strawberry / graphql-core z pozostałymi projektami kursu. PostgreSQL i `.env` nie są potrzebne; zadanie 16 korzysta z SQLite.

## Sposób nauki i prezentacji

Każde zadanie ma: **Treść zadania → Wstęp → Obserwuj działanie → Zrozum kod → Cały kod → Pytania**. Wstęp to trzy slajdy: mechanizm, konkretny przebieg zadania, oczekiwany wynik. PL zachowuje polecenia z `tasks.md`; ENG zawiera tłumaczenie. Komunikaty i identyfikatory kodu są angielskie.

W „Zrozum kod”:

- Najedź na tło wiersza: opis najbliższego otaczającego bloku (funkcja, warunek, pętla, try).
- Najedź na nazwę funkcji lub wywoływaną metodę: cel, działanie i wynik tej operacji.
- Najedź na numer: opis całej instrukcji w tej linii. W instrukcjach wieloliniowych wskazany jest wiersz początkowy.
- **Kliknięcie fragmentu kodu** przypina jego dymek. Sam najazd pokazuje podgląd znikający po 3 sekundach. Można przypiąć wiele, przeciągać je za nagłówek i zmieniać rozmiar za dowolny narożnik. Każdy przypięty dymek ma „Wyczyść” usuwające wszystkie dymki; × zamyka tylko jeden.
- Najazd na dymek wyróżnia powiązany kod. „Pokaż w kodzie” przełącza plik i przewija do fragmentu.
- Tab pokazuje opis, a Enter przypina go bez myszy. Esc zamyka dymek tymczasowy, potem ostatni przypięty.
- Przypięcia zostają przy przełączaniu plików i języka w zadaniu, chowają się poza zakładką i są czyszczone po zmianie zadania. Nie są zapisywane po odświeżeniu strony.

Objaśnienia są powiązane z AST bieżącego źródła. Numery linii nie są zapisane na sztywno, więc formatowanie nie rozjeżdża materiału. Po zmianie logiki należy również przejrzeć znaczenie opisów w `annotations.py` i zapowiedzi w `course_content.py`.

## Zadanie 7: „Pokaz z lektorem”

Dodatkowa zakładka jest dostępna tylko w zadaniu 7. Ma 12 klatek: cel, siedem fragmentów kodu, trzy etapy odczytywania rzeczywistego pokazu oraz podsumowanie. Animowany kursor wskazuje podświetlony fragment, a tekst wypowiedzi jest widoczny w napisach. Przejście następuje po zakończeniu wypowiedzi, nie po sztywno ustalonym czasie.

Przed **Play / Odtwórz** wybierz źródło lektora, głos i tempo. Domyślne źródło to **ElevenLabs · MP3**. Polska prezentacja pokazuje wyłącznie polskie głosy: z konta oraz z polskiego katalogu Voice Library oznaczonego przez API free_users_allowed. Domyślny głos to Piotr. Lista nie dodaje głosów do konta i nie zmienia uprawnień klucza. Dostęp do generowania nadal zależy od ograniczeń usługi i konta. Angielskie głosy są pokazywane tylko w prezentacji ENG. **Głos przeglądarki** pozostaje osobną opcją; aplikacja nie przełącza na niego automatycznie w razie błędu ElevenLabs.

Konfiguracja ElevenLabs znajduje się w `lessons/lesson34/.env` (plik pomijany przez Git). Szablon: `.env.example`:

```dotenv
ELEVENLABS_API_KEY=tu_wpisz_klucz
ELEVENLABS_VOICE_ID=o2xdfKUpc1Bwq7RchZuW
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
```

W panelu ElevenLabs klucz potrzebuje **Text to Speech → Dostęp** oraz **Głosy → Przeczytane**. Po zapisaniu `.env` kliknij **Odśwież głosy**; zmiana konfiguracji nie wymaga restartu. Wartość klucza pozostaje w Pythonie i nie jest zwracana przeglądarce. Backend używa oficjalnego REST API przez standardową bibliotekę Pythona, bez dodatkowych zależności.

Pierwsze Play danej klatki wysyła jej tekst ze wspólnego scenariusza do ElevenLabs i zapisuje MP3 w `.runtime/narration/`. Generowanie korzysta z limitu konta. Kolejne odtworzenia tego samego tekstu, głosu, języka, modelu i ustawień czytają lokalny plik. Zmiana tych parametrów tworzy inne nagranie. Tempo odtwarzania jest zmieniane lokalnie, więc samo przestawienie tempa nie generuje MP3 ponownie. Dwa równoczesne żądania tej samej klatki są zabezpieczone przed podwójnym generowaniem.

Po otrzymaniu nagrania przejście klatki czeka na zdarzenie zakończenia audio. Pauza i wyjście z zakładki zatrzymują dźwięk. Gdy przeglądarka wymaga ponownego kliknięcia po długim generowaniu, aplikacja pokazuje odpowiedni komunikat; ponowne Play korzysta z już zapisanego pliku. Zapisana lista głosów i gotowe MP3 pozwalają odtwarzać istniejące nagrania również bez połączenia z API. Nowe nagranie nadal wymaga połączenia i działającego klucza.

Aplikacja rozróżnia błędną konfigurację, limit konta, brak uprawnień i blokadę `detected_unusual_activity` zgłaszaną przez ElevenLabs. Taka blokada pochodzi z usługi; kod nie omija jej ani nie przedstawia jej jako błędnego klucza. Przeglądarka nie może przesłać dowolnego tekstu do płatnej syntezy: backend dopuszcza wyłącznie 12 klatek tego scenariusza w PL lub ENG.

Play włącza widok skupiony na pokazie; przycisk „Skup pokaz / wróć” przywraca nagłówki lekcji. Pauza zachowuje klatkę, a wznowienie czyta ją od początku. Strzałki i lista klatek pozwalają przejść do wybranego fragmentu. „Od początku” resetuje pokaz. Wyjście z zakładki, zmiana zadania lub języka zatrzymuje wypowiedź i przerywa uruchomiony przez nią pokaz, jeśli ten jeszcze trwa.

Pierwsza klatka „Obserwuj działanie” uruchamia faktyczny scenariusz zadania 7 przez istniejące API aplikacji. Omówienie wyniku zaczyna się dopiero po sukcesie procesu i potwierdzeniu jednego wysłania oraz odbioru przez dwóch różnych klientów. Pozostałe klatki odtwarzają ten sam zapis, podświetlając połączenia, nadawcę i odbiorców. To zapis zakończonego wykonania — pauza lektora nie zatrzymuje działającego serwera w połowie wysyłania. Przebieg jest również dostępny w historii zakładki „Obserwuj działanie”.

Wspólny tekst: `static/narrated-script.json`; sterowanie: `static/narrated-tour.js`; backend i pamięć nagrań: `eleven_narration.py`; wygląd: `static/narrated-tour.css`. Zakresy kodu są wyszukiwane w aktualnym źródle zadania 7. Po zmianie jego logiki trzeba przejrzeć treść scenariusza.

Testy synchronizacji, późnego ładowania głosów, pauzy, anulowania oraz błędnych wyników (bez instalowania dodatkowych pakietów):

```powershell
node --test lessons/lesson34/test_narrated_tour.cjs
lessons/lesson34/.venv/Scripts/python.exe -m unittest discover -s lessons/lesson34 -p test_eleven_narration.py
```

Testy ElevenLabs korzystają z odpowiedzi testowych, bez wywołań płatnego API.

Referencje API: [lista głosów i voiceschanged](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/voiceschanged_event), [zakończenie wypowiedzi](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/end_event).

## Pliki i wykonanie

`examples/task01/main.py` … `examples/task20/main.py` to niezależne rozwiązania. Zadanie 2 ma dodatkowo `client.py`. `demo_support.py` zawiera jedynie wspólny broadcast i wybór pliku SQLite; `lab_support.py` rejestruje pomiary. `run_task.py` uruchamia prawdziwy serwer aiohttp na wolnym porcie oraz kontrolowanych klientów i sprawdza otrzymane odpowiedzi.

Pojedynczy pokaz z konsoli:

```powershell
lessons/lesson34/.venv/Scripts/python.exe lessons/lesson34/examples/run_task.py 7
```

Serwer do własnych eksperymentów (pozostaje aktywny do Ctrl+C):

```powershell
lessons/lesson34/.venv/Scripts/python.exe lessons/lesson34/examples/run_task.py 4 --serve --port 8134
```

Dla zadań GraphQL otwórz <http://127.0.0.1:8134/graphql>. Przycisk GraphiQL w aplikacji sam uruchamia serwer wybranego zadania. Jego log to `.runtime/graphql.log`. Edytor GraphiQL pobiera zasoby z CDN; pokazy i objaśnienia nie wymagają CDN. Dla zadań WS endpoint to `ws://127.0.0.1:8134/ws`.

Zadanie 11 zachowuje domyślne **30 s / 60 s**; pokaz skraca je do 0,05 s / 0,15 s i informuje o tym w wynikach. Są to wiadomości tekstowe ping/pong na poziomie aplikacji.

SQLite otrzymuje osobny katalog `.runtime/task16-*` dla każdego pokazu. Historia jest trwała w obrębie konkretnego pliku, ale kolejny pokaz celowo zaczyna od pustej bazy. Dane fake zadań GraphQL żyją w procesie. JWT używa jawnego klucza demonstracyjnego. DataLoader mierzy wywołania fake pobierania postów, a nie SQL. Gra obsługuje jedną partię na proces: wygraną, remis i rozłączenie; nowy proces rozpoczyna nową partię.

To przykłady jednego procesu do nauki; wieloprocesowy serwer wymagałby współdzielonego stanu i dystrybucji zdarzeń.

## Weryfikacja

```powershell
lessons/lesson34/.venv/Scripts/python.exe lessons/lesson34/test_lesson34.py
```

Testy wykonują wszystkie 20 pokazów, sprawdzają zgodność opisów ze źródłem, remis i rozłączenie, błędne ruchy bez zmiany planszy, historię ostatnich 50 wpisów po ponownym otwarciu SQLite, odrzucanie JWT i niezależny DataLoader dla każdego żądania.
