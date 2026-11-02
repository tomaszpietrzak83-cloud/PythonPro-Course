# Lekcja 35 · Cloud Operations

20 osobnych zadań DevOps / AWS, wspólnie przeglądanych w lokalnej aplikacji.
Wzorcem nawigacji jest lekcja 34: **Treść zadania → Wstęp (3 slajdy) → Obserwuj działanie → Zrozum kod → Cały kod → Pytania**.
Interfejs i materiały mają wersje PL/ENG, tryb slajdów i ciągły, większy tekst oraz pełny ekran.

## Uruchomienie

Z katalogu kursu:

```powershell
.venv/Scripts/python.exe -m pip install -r lessons/lesson35/requirements.txt
.venv/Scripts/python.exe lessons/lesson35/run_app.py
```

Adres: http://127.0.0.1:8035/. `--no-browser` pomija otwarcie przeglądarki.
Launcher korzysta ze środowiska kursu; opcjonalnie wybierze własne `lesson35/.venv`, jeśli istnieje.
Sprawdza materiały i nie zamyka obcych usług zajmujących port. Log: `.runtime/server.log`.

## Zadania i wyniki

Każde zadanie ma `examples/task01/main.py` … `examples/task20/main.py`.
Zadanie 18 ma dodatkowo `config.json`, widoczny w zakładce „Cały kod”.
Funkcje są oddzielone od scenariuszy `demo(work, cloud)`, więc można importować je do własnych eksperymentów.

```powershell
.venv/Scripts/python.exe lessons/lesson35/examples/run_task.py 17
.venv/Scripts/python.exe -m unittest discover -s lessons/lesson35 -p test_lesson35.py
node --check lessons/lesson35/static/studio.js
```

Każdy pokaz uruchamia osobny proces i zapisuje wyniki do własnego katalogu `.runtime/taskXX-*`.
Aplikacja pokazuje wynik JSON, rzeczywiste pliki tekstowe, pomiary oraz historię bieżącej sesji.
Miniatura JPG i archiwum ZIP pozostają w katalogu wynikowym. Historia w przeglądarce nie jest trwałym dziennikiem.

## Zakres wykonania

- 1: prawdziwy `requests` i trzy adresy lokalnego serwera HTTP (200/200/503).
- 2, 7, 8, 16, 18, 20: lokalne operacje i dane kontrolne. Zadanie 8 nie wypisuje wartości sekretów.
- 3–6, 9–12, 14, 17, 19: jawny adapter `LocalCloud` w pamięci, bez połączeń z AWS.
- 13: symulowany wykonawca poleceń; trzy ścieżki: sukces, błąd testów, rollback.
- 15: dwa przyspieszone cykle; dane infrastruktury i HTTP są testowe, CSV i alerty lokalne. Pętla `monitor()` ma domyślnie 300 s i nieograniczoną liczbę cykli.

Adapter celowo zwraca po jednym elemencie na stronę, aby ćwiczenia naprawdę przechodziły przez paginację.
To niewielki test double, nie emulator wszystkich reguł AWS. Nie weryfikuje IAM, limitów ani rozliczeń.
Kod S3/EC2 przyjmuje wstrzykiwanego klienta; sam pokaz nigdy nie tworzy klienta boto3 i nie odczytuje danych logowania.
Zadanie 4 pozwala jawnie utworzyć klienta boto3 przy wywołaniu funkcji bez argumentu `client`.

Pipeline jest modelem sterowania etapami, a nie gotowym wdrożeniem: wymaga rzeczywistego repozytorium, logowania do ECR, tagów obrazów oraz implementacji SSH i health checku.
Hosting zadania 14 działa w CLI na adapterze; wyświetlony URL nie jest opublikowaną stroną. Kod nie wyłącza Block Public Access.
Zadanie 17 wykonuje dwa sprawdzenia listy obiektów; zbiór przetworzonych wersji żyje w pamięci procesu. Nie jest to podłączona Lambda.
Backup S3 kopiuje bieżące obiekty, bez wersjonowania i pełnego zachowania metadanych.
Wartości kosztów są wyłącznie stawkami ćwiczeniowymi, nie aktualnym cennikiem.

## Wygląd i dalszy rozwój

Nowy motyw „Cloud Operations”: ciemne granatowe tło, jasny tekst, stonowane panele i turkusowe akcje i jawna etykieta trybu wykonania.
Objaśnienia wiążą się z aktualnym AST: najazd lub fokus pokazuje instrukcję/blok, kliknięcie przypina dymek. Można przypinać wiele opisów i przenosić je jak w lekcji 34.
Opis instrukcji obejmuje jej cały zakres, a nie osobne opisy każdego tokenu. Scenariusz lektorski specyficzny dla WebSocket z lekcji 34 nie jest kopiowany.

Sugestie na kolejny etap: zapis postępu, własne przewidywania przed pokazem, wybór scenariusza awarii i porównanie dwóch wykonań.

## Źródła

- [Tworzenie bucketów i region us-east-1](https://docs.aws.amazon.com/boto3/latest/guide/s3-example-creating-buckets.html)
- [Paginacja ListObjectsV2](https://docs.aws.amazon.com/boto3/latest/reference/services/s3/paginator/ListObjectsV2.html)
- [Metryki CloudWatch Agent, w tym disk_used_percent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/metrics-collected-by-CloudWatch-agent.html)

Zajętość systemu plików w zadaniu 15 wymaga danych systemu operacyjnego/agenta; sama wielkość wolumenu EBS nie jest procentem zajętości.
