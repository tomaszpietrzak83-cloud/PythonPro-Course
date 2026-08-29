# Lesson 29 - Zadania

## TASK 01 - Zadanie 1 - Pierwsze zadanie (proste)

Stwórz w pliku `tasks.py` proste zadanie o nazwie `hello_world`, które drukuje w konsoli workera napis:

```text
Hello from Celery!
```

Stwórz widok Django, który po wejściu na odpowiedni URL wywoła to zadanie.

## TASK 02 - Zadanie 2 - Zadanie z argumentami (proste)

Napisz zadanie:

```python
multiply(a, b)
```

Zadanie ma przyjmować dwie liczby i zwracać ich iloczyn.

W widoku stwórz prosty formularz HTML z dwoma polami. Pobierz z nich liczby i przekaż je do zadania Celery.

## TASK 03 - Zadanie 3 - Zapis do pliku (proste)

Stwórz zadanie:

```python
log_timestamp()
```

Zadanie ma zapisywać aktualną datę i godzinę do pliku `log.txt`.

## TASK 04 - Zadanie 4 - Pierwsze zadanie z harmonogramem (proste)

Użyj Celery Beat, aby uruchamiać zadanie `log_timestamp()` z poprzedniego ćwiczenia co 10 sekund.

## TASK 05 - Zadanie 5 - Zmiana w bazie danych (proste)

Stwórz zadanie:

```python
count_users()
```

Zadanie ma liczyć wszystkich użytkowników w bazie danych:

```python
User.objects.count()
```

Wynik wydrukuj w konsoli workera.

## TASK 06 - Zadanie 6 - Harmonogram z crontab (proste)

Skonfiguruj Celery Beat tak, aby zadanie `count_users()` uruchamiało się codziennie o godzinie 23:00.

## TASK 07 - Zadanie 7 - Przekazywanie ID obiektu (proste)

Stwórz zadanie:

```python
update_user_last_login(user_id)
```

Zadanie ma:

- przyjąć ID użytkownika,
- znaleźć użytkownika w bazie,
- zaktualizować jego pole `last_login` na aktualny czas.

> [!tip]
>
> Do zadań Celery zawsze przekazuj proste typy danych, na przykład ID, a nie całe obiekty Django. Obiekt w momencie wykonania zadania może już być inny niż w momencie jego wywołania.

## TASK 08 - Zadanie 8 - Prosta symulacja (proste)

Napisz zadanie, które symuluje przetwarzanie wideo przez 15 sekund:

```python
time.sleep(15)
```

Widok, który je wywołuje, powinien natychmiast zwrócić komunikat:

```text
Przetwarzanie wideo rozpoczęte!
```

## TASK 09 - Zadanie 9 - Masowe tworzenie zadań (challenge)

Napisz własną komendę `manage.py`, na przykład:

```text
enqueue_tasks
```

Komenda ma w pętli tworzyć i dodawać do kolejki 50 zadań `multiply` z losowymi argumentami.

## TASK 10 - Zadanie 10 - Powiadomienie mailowe (challenge)

Rozbuduj zadanie z symulacją wysyłki maila.

Stwórz prosty model `EmailNotification` z polami:

- `recipient_email`
- `subject`
- `body`
- `sent_at`, nullable

Zadanie Celery powinno:

- przyjąć ID obiektu tego modelu,
- wysłać "maila", czyli zasymulować opóźnienie,
- po zakończeniu zaktualizować pole `sent_at` na aktualny czas.

## TASK 11 - Zadanie 11 - Śledzenie postępu zadania (challenge)

Stwórz zadanie, które w pętli od 1 do 100 wykonuje jakąś operację, śpiąc 0.1 sekundy w każdej iteracji.

Po każdej iteracji zadanie powinno aktualizować swój stan i informować o postępie.

Stwórz drugi endpoint Django:

```text
/task-status/<task_id>/
```

Endpoint ma zwracać aktualny postęp zadania.

> [!tip]
>
> Użyj `self.update_state(state="PROGRESS", meta={"current": i, "total": 100})` wewnątrz zadania. Będziesz musiał związać zadanie z instancją przez `@shared_task(bind=True)`.

## TASK 12 - Zadanie 12 - Czyszczenie bazy danych (challenge)

Napisz zadanie, które usuwa z bazy wszystkie obiekty modelu `LogEntry` starsze niż 90 dni.

Model `LogEntry` musisz najpierw stworzyć.

Uruchom to zadanie za pomocą Celery Beat raz dziennie.

## TASK 13 - Zadanie 13 - Web scraping w tle (challenge)

Stwórz zadanie, które używa bibliotek `requests` i `BeautifulSoup4` do pobrania tytułu strony:

```text
https://example.com
```

Tytuł strony zapisz w bazie danych.

Zadanie ma być uruchamiane co godzinę.

## TASK 14 - Zadanie 14 - Generowanie raportu CSV (challenge)

Napisz zadanie, które generuje plik CSV ze wszystkimi użytkownikami i ich adresami email.

Plik powinien być zapisany w katalogu `media`.

Widok, który inicjuje to zadanie, powinien zwrócić `task_id`.

Stwórz drugi widok, który:

- pozwala sprawdzić, czy zadanie się zakończyło,
- jeśli zadanie się zakończyło, udostępnia link do pobrania pliku.

## TASK 15 - Zadanie 15 - Obsługa błędów i ponawianie (challenge)

Stwórz zadanie, które próbuje połączyć się z nieistniejącym adresem URL.

Zadanie oczywiście rzuci wyjątek.

Skonfiguruj je tak, aby w przypadku błędu ponawiało próbę 3 razy w odstępach 1-minutowych.

> [!tip]
>
> Użyj `try ... except` oraz `self.retry(countdown=60, max_retries=3)`.

## TASK 16 - Zadanie 16 - [AI] Klasyfikacja obrazu w tle (challenge)

Stwórz model `UploadedImage` z polami:

- `ImageField`
- `classification_result` jako `CharField`

Gdy użytkownik prześle obrazek:

- zapisz go,
- uruchom zadanie Celery,
- przekaż do zadania ID obrazka.

Zadanie powinno użyć biblioteki `Pillow` do otwarcia obrazka i "sklasyfikowania" go, na przykład:

- czy jest w skali szarości,
- czy jest kolorowy,
- jakie ma wymiary.

Wynik zapisz w polu `classification_result`.

To uproszczona wersja prawdziwego zadania AI.

## TASK 17 - Zadanie 17 - Łańcuchy zadań, czyli chains (challenge)

Zapoznaj się z dokumentacją Celery na temat `chains`.

Stwórz łańcuch trzech zadań:

1. Pierwsze generuje losową liczbę.
2. Drugie mnoży ją przez 10.
3. Trzecie zapisuje wynik do pliku.

Wywołaj cały łańcuch jednym poleceniem z widoku Django.

## TASK 18 - Zadanie 18 - Różne kolejki zadań (challenge)

Skonfiguruj dwie różne kolejki:

- `default` dla większości zadań,
- `priority_queue` dla zadań krytycznych.

Stwórz zadanie do wysyłania maila i skonfiguruj je tak, aby zawsze trafiało do `priority_queue`.

Uruchom dwa workery:

- jeden nasłuchujący na kolejce domyślnej,
- drugi nasłuchujący na kolejce priorytetowej.

## TASK 19 - Zadanie 19 - Instalacja i eksploracja Flower (challenge)

Zainstaluj i uruchom Flower dla swojego projektu.

Przejrzyj dostępne zakładki:

- dashboard,
- tasks,
- workers.

Spróbuj wywołać zadanie z poziomu interfejsu Flower.

## TASK 20 - Zadanie 20 - Transakcje bazodanowe i zadania (challenge)

Stwórz widok, który w ramach transakcji atomowej:

```python
@transaction.atomic
```

tworzy nowy obiekt w bazie i następnie wywołuje zadanie Celery, które ma ten obiekt przetworzyć.

Odpowiedz:

- Dlaczego ważne jest, aby wywołać zadanie po pomyślnym zatwierdzeniu transakcji?
- Jak można to zapewnić?

> [!tip]
>
> Poszukaj informacji o `transaction.on_commit`.

<p style="color:red"><strong>Komentarz mentora:</strong> To zadanie jest bardzo praktyczne. Jeśli worker dostanie ID obiektu przed zatwierdzeniem transakcji, może próbować pobrać z bazy rekord, którego jeszcze nie widzi.</p>
