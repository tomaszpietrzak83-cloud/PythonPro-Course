# Lekcja 29: Asynchroniczne zadania i harmonogramowanie z Celery w Django

`#lekcja` `#python` `#django` `#celery` `#asynchroniczność` `#backend`

W tej lekcji nauczymy się, jak odciążyć aplikację Django, przenosząc długotrwałe operacje do tła.

Dzięki temu interfejs użytkownika pozostaje responsywny, a aplikacja może wykonywać złożone zadania bez blokowania głównego wątku.

Wykorzystamy do tego narzędzie **Celery**. Dowiemy się:

- czym jest Celery,
- jak skonfigurować Celery w projekcie Django,
- jak tworzyć zadania,
- jak planować ich wykonanie za pomocą Celery Beat.

## 1. Czym jest Celery i dlaczego go potrzebujemy?

Wyobraź sobie sytuację, w której użytkownik aplikacji klika przycisk `Generuj raport roczny`.

Taki proces może trwać 30 sekund, minutę albo dłużej. W standardowym podejściu przeglądarka użytkownika czekałaby na odpowiedź serwera. To zła praktyka, bo użytkownik ma wrażenie, że aplikacja się zawiesiła.

> [!definition]
>
> Celery to rozproszona kolejka zadań dla Pythona. Umożliwia uruchamianie czasochłonnych operacji w tle, w oddzielnych procesach zwanych workerami.

Główne korzyści z używania Celery:

- **Poprawa responsywności** - użytkownik nie musi czekać na zakończenie długich operacji.
- **Większa niezawodność** - zadania są umieszczane w kolejce i mogą zostać ponowione.
- **Skalowalność** - można uruchomić wielu workerów, nawet na różnych maszynach.

<p style="color:red"><strong>Komentarz mentora:</strong> Celery nie przyspiesza samego zadania. Ono nadal trwa tyle, ile trwało. Celery sprawia, że zadanie wykonuje się poza requestem użytkownika.</p>

## 2. Architektura Celery

Podstawowa architektura Celery składa się z trzech głównych komponentów:

1. **Klient, czyli aplikacja Django** - inicjuje wykonanie zadania.
2. **Broker wiadomości** - przechowuje zadania w kolejce. Najpopularniejsze brokery to Redis i RabbitMQ.
3. **Worker Celery** - osobny proces, który pobiera zadania z kolejki i je wykonuje.

Opcjonalnie można użyć też **backendu wyników**, który przechowuje status i wynik wykonanych zadań.

Schemat:

```text
Django View
    -> .delay()
    -> Broker wiadomości, np. Redis
    -> Worker Celery
    -> Result Backend, opcjonalnie
```

## 3. Konfiguracja Celery w projekcie Django

W tej lekcji używamy Redisa jako brokera wiadomości.

> [!info]
>
> Upewnij się, że masz zainstalowanego i uruchomionego Redisa na komputerze. Jeśli używasz Dockera, możesz uruchomić Redis w kontenerze.

### Krok 1: Instalacja bibliotek

```bash
pip install celery redis
```

### Krok 2: Utworzenie pliku `celery.py`

W głównym katalogu projektu Django, tam gdzie znajduje się `settings.py`, utwórz plik `celery.py`.

```python
# project_name/celery.py

import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")

app = Celery("project_name")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
```

> [!tip]
>
> Pamiętaj, aby zastąpić `project_name` rzeczywistą nazwą swojego projektu.

### Krok 3: Modyfikacja pliku `__init__.py`

Aby aplikacja Celery była ładowana przy starcie Django, zmodyfikuj plik `project_name/__init__.py`.

```python
# project_name/__init__.py

from .celery import app as celery_app

__all__ = ("celery_app",)
```

### Krok 4: Konfiguracja w `settings.py`

```python
# project_name/settings.py

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "Europe/Warsaw"
```

Struktura projektu:

```text
my_project/
    manage.py
    my_project/
        settings.py
        urls.py
        celery.py
        __init__.py
    my_app/
        models.py
        views.py
        tasks.py
```

<p style="color:red"><strong>Komentarz mentora:</strong> Jeśli worker nie widzi zadań, najpierw sprawdź trzy rzeczy: poprawną nazwę projektu w `Celery("project_name")`, import w `__init__.py` i czy plik z zadaniami nazywa się dokładnie `tasks.py`.</p>

## 4. Wykonywanie zadań CPU-bound w tle

Zadania **CPU-bound** to takie, których czas wykonania jest ograniczony głównie przez moc procesora.

Przykłady:

- skomplikowane obliczenia matematyczne,
- przetwarzanie obrazów,
- kompresja plików,
- trenowanie modeli uczenia maszynowego.

### Krok 1: Tworzenie pliku `tasks.py`

Wewnątrz aplikacji Django, na przykład `my_app`, utwórz plik `tasks.py`.

```python
# my_app/tasks.py

import time

from celery import shared_task


@shared_task
def add(x, y):
    """Proste zadanie, które dodaje dwie liczby."""
    return x + y


@shared_task
def simulate_cpu_bound_task(duration):
    """
    Symuluje długotrwałe zadanie, np. generowanie raportu.
    """
    print(f"Rozpoczynam zadanie, które potrwa {duration} sekund...")
    time.sleep(duration)
    print("Zadanie zakończone.")
    return f"Raport wygenerowany pomyślnie po {duration} sekundach."


@shared_task
def send_welcome_email(user_email):
    """
    Symuluje wysyłanie maila powitalnego.
    """
    print(f"Wysyłanie maila powitalnego do {user_email}...")
    time.sleep(10)
    print(f"Mail do {user_email} wysłany.")
    return True
```

### Krok 2: Wywoływanie zadań z widoku Django

Zadania wywołujemy asynchronicznie za pomocą `.delay()` lub `.apply_async()`.

```python
# my_app/views.py

from django.http import JsonResponse

from .tasks import simulate_cpu_bound_task


def generate_report_view(request):
    task = simulate_cpu_bound_task.delay(20)

    return JsonResponse({
        "message": "Twoje żądanie generowania raportu zostało przyjęte i jest przetwarzane w tle.",
        "task_id": task.id,
    })
```

`.delay()` nie czeka na zakończenie zadania. Zwraca obiekt zadania, z którego możemy pobrać `task.id`.

## 5. Uruchomienie workera Celery

Aby zadania były wykonywane, trzeba uruchomić co najmniej jednego workera.

W osobnym terminalu, w katalogu głównym projektu:

```bash
celery -A project_name worker -l info
```

Znaczenie elementów polecenia:

- `-A project_name` - wskazuje na instancję aplikacji Celery w projekcie,
- `worker` - uruchamia proces workera,
- `-l info` - ustawia poziom logowania na `INFO`.

Po wywołaniu widoku `generate_report_view` w logach workera powinieneś zobaczyć informację o podjęciu i wykonaniu zadania.

<p style="color:red"><strong>Komentarz mentora:</strong> Serwer Django i worker Celery to dwa osobne procesy. Samo `python manage.py runserver` nie wystarczy, żeby zadania z kolejki faktycznie się wykonywały.</p>

## 6. AI w zadaniach asynchronicznych

Zadania asynchroniczne są dobrym miejscem do integracji z modelami AI.

Operacje takie jak:

- klasyfikacja obrazów,
- analiza sentymentu tekstu,
- generowanie podsumowań,

mogą trwać długo.

Można stworzyć zadanie Celery, które przyjmuje dane wejściowe, na przykład ID obrazka z bazy danych, ładuje model AI, wykonuje obliczenia i zapisuje wynik z powrotem do bazy.

Dzięki temu użytkownik nie musi czekać na zakończenie pracy modelu.

## 7. Celery Beat

Celery Beat to harmonogram zadań.

Pozwala uruchamiać zadania:

- o stałych porach, na przykład codziennie o północy,
- w regularnych interwałach, na przykład co 5 minut.

> [!definition]
>
> Celery Beat to usługa, która okresowo dodaje zadania do kolejki zgodnie ze zdefiniowanym harmonogramem. Działa jako oddzielny proces i współpracuje z workerami.

### Konfiguracja w `settings.py`

```python
# project_name/settings.py

from celery.schedules import crontab


CELERY_BEAT_SCHEDULE = {
    "send-summary-every-5-minutes": {
        "task": "my_app.tasks.send_periodic_summary",
        "schedule": 300.0,
        "args": (["user1@example.com", "user2@example.com"],),
    },
    "cleanup-database-daily": {
        "task": "my_app.tasks.cleanup_old_logs",
        "schedule": crontab(hour=4, minute=5),
    },
}
```

Teraz trzeba stworzyć zadania w `my_app/tasks.py`.

```python
# my_app/tasks.py

from celery import shared_task


@shared_task
def send_periodic_summary(user_emails):
    print(f"Wysyłanie podsumowania do {len(user_emails)} użytkowników...")
    print("Podsumowanie wysłane.")


@shared_task
def cleanup_old_logs():
    print("Rozpoczynam czyszczenie starych logów...")
    print("Logi wyczyszczone.")
```

### Uruchomienie Celery Beat

Celery Beat uruchamiamy jako oddzielny proces:

```bash
celery -A project_name beat -l info
```

W typowej pracy masz uruchomione trzy procesy:

1. Serwer deweloperski Django:

```bash
python manage.py runserver
```

2. Worker Celery:

```bash
celery -A project_name worker -l info
```

3. Harmonogram Celery Beat:

```bash
celery -A project_name beat -l info
```

## 8. Monitorowanie z Flower

Flower to narzędzie do monitorowania zadań Celery w czasie rzeczywistym.

Pozwala zobaczyć między innymi:

- status workerów,
- zadania zakończone,
- zadania nieudane,
- zadania w trakcie,
- szczegóły wykonania zadań.

Instalacja:

```bash
pip install flower
```

Uruchomienie:

```bash
celery -A project_name flower
```

## 9. Podsumowanie

W tej lekcji nauczyliśmy się:

- czym jest Celery,
- czym są broker wiadomości, worker i backend wyników,
- jak skonfigurować Celery w Django,
- jak tworzyć zadania w `tasks.py`,
- jak wywoływać zadania przez `.delay()`,
- jak uruchomić workera,
- czym jest Celery Beat,
- jak planować zadania cykliczne,
- jak monitorować zadania przez Flower.
