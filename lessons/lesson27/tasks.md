# Lesson 27 - Zadania

## TASK 01 - Zadanie 1 - Konfiguracja locmem cache (proste)

W swoim projekcie Django, w pliku `settings.py`, skonfiguruj domyślny cache tak, aby używał:

```python
django.core.cache.backends.locmem.LocMemCache
```

Uruchom serwer, aby upewnić się, że aplikacja startuje bez błędów.

## TASK 02 - Zadanie 2 - Instalacja Django Debug Toolbar (proste)

Zainstaluj i skonfiguruj `django-debug-toolbar` zgodnie z instrukcjami z lekcji.

Upewnij się, że panel jest widoczny w Twojej aplikacji i możesz wejść w zakładkę `Cache`.

## TASK 03 - Zadanie 3 - Cachowanie widoku API (proste)

Wybierz jeden z istniejących, prostych widoków `GET` w Twoim API, na przykład listę obiektów.

Za pomocą dekoratora `@cache_page` ustaw cache na 60 sekund.

Użyj Django Debug Toolbar, aby zweryfikować:

- przy pierwszym żądaniu jest `cache miss`,
- przy kolejnych żądaniach w ciągu 60 sekund jest `cache hit`.

## TASK 04 - Zadanie 4 - Zabawa z niskopoziomowym API w shellu (proste)

Uruchom Django shell:

```bash
python manage.py shell
```

Zaimportuj cache:

```python
from django.core.cache import cache
```

Ustaw wartość:

```python
cache.set("my_key", "hello world", 30)
```

Odczytaj ją:

```python
cache.get("my_key")
```

Poczekaj 30 sekund i spróbuj odczytać ją ponownie.

Co się stało?

## TASK 05 - Zadanie 5 - Czyszczenie cache (proste)

Znajdź w dokumentacji Django komendę `manage.py`, która pozwala na wyczyszczenie całego cache.

Użyj jej w terminalu, aby usunąć wszystkie zbuforowane dane.

<p style="color:red"><strong>Komentarz mentora:</strong> W standardowym Django dokumentacja opisuje metodę `cache.clear()` do usunięcia wszystkich kluczy z cache. Nie widzę uniwersalnej wbudowanej komendy `manage.py` do czyszczenia cache, więc potraktuj to zadanie jako okazję do sprawdzenia dokumentacji i porównania jej z treścią lekcji.</p>

## TASK 06 - Zadanie 6 - Implementacja cache plikowego (challenge)

Zmień konfigurację cache w `settings.py` na `FileBasedCache`.

Stwórz odpowiedni katalog.

Użyj widoku z zadania 3.

Sprawdź, czy po pierwszym odwołaniu do widoku w Twoim katalogu cache pojawiły się nowe pliki.

Co zawierają te pliki?

## TASK 07 - Zadanie 7 - Selektywne cachowanie w widoku (challenge)

Stwórz widok, który pobiera dane z dwóch źródeł:

- jedno zapytanie do bazy, które jest proste i szybkie,
- drugie źródło, które symuluje bardzo skomplikowane i długie obliczenia.

Do symulacji użyj:

```python
time.sleep(3)
```

Użyj niskopoziomowego API cache, aby zbuforować tylko wynik skomplikowanych obliczeń, a nie całą odpowiedź widoku.

## TASK 08 - Zadanie 8 - Różne czasy cache dla różnych metod ViewSetu (challenge)

Stwórz `ModelViewSet` dla jednego z Twoich modeli.

Użyj dekoratora:

```python
@method_decorator(cache_page(...))
```

Wymagania:

- widok listy, czyli `list`, ma być cachowany na 10 minut,
- widok szczegółów, czyli `retrieve`, ma być cachowany tylko na 1 minutę,
- metody `create`, `update` i `destroy` nie powinny być cachowane.

## TASK 09 - Zadanie 9 - Unieważnianie cache po aktualizacji obiektu (challenge)

Rozszerz zadanie 8.

Zaimplementuj logikę, która po każdej udanej operacji `update` lub `partial_update` na obiekcie unieważni cache dla widoku szczegółów, czyli `retrieve`, tego konkretnego obiektu.

Wskazówka: pomocne mogą być sygnały Django `post_save` albo nadpisanie metody `perform_update` w ViewSecie.

Musisz też wiedzieć, jak Django buduje klucze cache dla widoków. Może to wymagać researchu albo użycia własnych kluczy.

## TASK 10 - Zadanie 10 - Konfiguracja Redis jako backendu cache (challenge)

To zadanie wymaga zainstalowania Redis na Twoim komputerze, na przykład przez Docker.

Zainstaluj bibliotekę:

```bash
pip install django-redis
```

Zmień konfigurację `CACHES` w `settings.py`, aby używać Redis jako backendu.

Sprawdź za pomocą Django Debug Toolbar, czy Twoja aplikacja poprawnie komunikuje się z serwerem Redis.

Jest to konfiguracja zbliżona do produkcyjnej.
