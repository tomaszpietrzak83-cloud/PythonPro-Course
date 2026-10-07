# Uruchamianie kursu na tym komputerze

Repozytorium pobrano do `C:\Users\DELL\Documents\developer\Python Pro Course`.
Wspólne środowisko `.venv` zawiera Python 3.12.13 oraz zależności lekcji.

## PowerShell

W głównym katalogu repozytorium:

```powershell
.\.venv\Scripts\Activate.ps1
cd lessons\lesson01
python task1_hello.py
```

Skrypty najlepiej uruchamiać z katalogu zawierającego dany skrypt,
ponieważ część ćwiczeń używa względnych ścieżek do plików.
Jeśli PowerShell blokuje aktywację, można użyć interpretera bez aktywacji:

```powershell
& 'C:\Users\DELL\Documents\developer\Python Pro Course\.venv\Scripts\python.exe' .\task1_hello.py
```

W edytorze wybierz interpreter `.venv\Scripts\python.exe` z głównego katalogu.

## Zależności

`requirements.txt` zawiera wspólny zestaw zależności, a `requirements-lock.txt`
dokładne zainstalowane wersje. Odtworzenie pakietów w aktywnym środowisku:

```powershell
python -m pip install -r requirements-lock.txt
python -m pip check
```

Historyczne pliki requirements poszczególnych lekcji mają sprzeczne wersje
Flask, SQLAlchemy, Django i innych pakietów. Dla wspólnego środowiska używaj
listy z głównego katalogu. Skrypty `run_before_checking_lesson.py` tworzą
osobne środowiska lekcji; nie są potrzebne do korzystania ze wspólnego `.venv`.

Wybrano Django 5.2.17, Flask 3.1.3 oraz SQLAlchemy 2.0.52.
Sprawdzono importy 21 bibliotek, zgodność zależności (`pip check`) i polecenie
`manage.py check` we wszystkich 12 projektach Django. Kontrole Django dla
lekcji 19 i 28 używały tymczasowych zmiennych środowiskowych wyłącznie na czas
sprawdzenia. To nie był test połączenia z bazą ani wszystkich ćwiczeń.

## Django i SQLite

Przykład po aktywacji środowiska, zaczynając w głównym katalogu:

```powershell
cd lessons\lesson20\myproject
python manage.py migrate
python manage.py runserver
```

Migracje i ewentualne dane przykładowe przygotuj osobno dla wybranej lekcji,
zgodnie z jej instrukcją.

## PostgreSQL i Redis na drugim komputerze

Biblioteki klienckie są zainstalowane. Serwery znajdują się na innym komputerze,
który będzie wyłączony: ćwiczenia wymagające tych usług nie będą wtedy działać.
Nie skonfigurowano ani nie sprawdzono połączeń z usługami zdalnymi.

- Lekcja 18: projekty `flask_masterclass` i `room_booking` domyślnie wymagają
  PostgreSQL. W pliku `.env` danego projektu ustaw `DATABASE_URL` z adresem
  działającego serwera, nazwą bazy i danymi logowania.
- Lekcje 19 i 28: plik `.env` w katalogu lekcji powinien zawierać
  `DJANGO_SECRET_KEY`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`,
  `POSTGRES_USER` i `POSTGRES_PASSWORD`. Następnie wykonaj migracje.
- Lekcja 27, projekt `l27_pro_3`: Redis jest obecnie wskazany jako
  `redis://127.0.0.1:6379/1` w `l27_pro_3/settings.py`. Zdalny serwer wymaga
  zmiany adresu. Pomocnik `myapp3/redis_cache_helper.py` zakłada lokalny Docker.

Pełna praca offline z tymi ćwiczeniami wymagałaby lokalnych serwerów albo
osobnego dostosowania ćwiczeń do SQLite i pamięci podręcznej bez Redis.
