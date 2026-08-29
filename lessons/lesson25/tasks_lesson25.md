# Lesson 25 - Django REST Framework

## TASK 01 - Zadanie 1 - Instalacja i konfiguracja (proste)

Stworz nowy projekt Django.

Zainstaluj Django REST Framework:

```bash
pip install djangorestframework
```

Dodaj `"rest_framework"` do `INSTALLED_APPS` w ustawieniach projektu.

## TASK 02 - Zadanie 2 - Prosty model i serializator (proste)

W nowej aplikacji Django stworz model `Product` z polami:

- `name` (`CharField`)
- `price` (`DecimalField`)

Nastepnie stworz dla niego `ModelSerializer`, ktory bedzie uwzglednial pola:

- `id`
- `name`
- `price`

## TASK 03 - Zadanie 3 - Pierwszy ViewSet i Router (proste)

Stworz `ModelViewSet` dla modelu `Product`.

Podlacz go do glownego pliku `urls.py` za pomoca `DefaultRouter` pod adresem:

```text
/api/products/
```

Uruchom serwer i wejdz w przegladarce na adres:

```text
http://127.0.0.1:8000/api/products/
```

Co widzisz?

## TASK 04 - Zadanie 4 - Testowanie w Postmanie (proste)

Uzyj Postmana, aby dodac 3 nowe produkty do swojej bazy danych za pomoca zapytania `POST` na endpoint:

```text
/api/products/
```

Sprawdz, czy po wyslaniu zapytania `GET` pod ten sam adres widzisz dodane produkty.

## TASK 05 - Zadanie 5 - Widok z ciasteczkiem

Stworz dwa widoki funkcyjne i podlacz je pod adresy:

- `/api/hello/`
- `/api/set-name/`

Widok `set-name` powinien przyjmowac parametr zapytania `name`, na przyklad:

```text
/api/set-name/?name=Anna
```

Widok powinien ustawiac ciasteczko o nazwie `user_name` z podana wartoscia.

Widok `hello` powinien odczytywac to ciasteczko i zwracac komunikat:

```text
Witaj, [imie]!
```

albo:

```text
Witaj, Gosc!
```

jesli ciasteczko nie istnieje.

## TASK 06 - Zadanie 6 - API do notatek (challenge)

Rozbuduj aplikacje z zadania 1-3.

Stworz model `Note` z polami:

- `title`
- `content` (`TextField`)
- `created_at`

Zbuduj dla niego pelne API CRUD, uzywajac `ModelViewSet` i `ModelSerializer`.

Uzyj Postmana do przetestowania wszystkich 5 operacji:

- lista
- detal
- tworzenie
- aktualizacja
- usuwanie

## TASK 07 - Zadanie 7 - API Kalkulatora (challenge)

Stworz widok funkcyjny pod adresem:

```text
/api/calculate/
```

Uzyj dekoratora:

```python
@api_view(["GET"])
```

Widok powinien przyjmowac trzy parametry zapytania:

- `num1`
- `num2`
- `operation`

Parametr `operation` moze przyjac wartosci:

- `add`
- `subtract`
- `multiply`
- `divide`

Widok powinien wykonac odpowiednia operacje matematyczna i zwrocic wynik w formacie JSON, na przyklad:

```json
{"result": 15}
```

Zadbaj o obsluge bledow, na przyklad:

- dzielenie przez zero
- niepoprawna operacja
- niepoprawne liczby
- brak wymaganych parametrow

## TASK 08 - Zadanie 8 - Filtrowanie i wyszukiwanie (challenge)

W `ViewSet` dla produktow z zadania 2 zaimplementuj filtrowanie po cenie.

Chcemy moc wysylac zapytania takie jak:

```text
/api/products/?min_price=100&max_price=200
```

Endpoint powinien zwrocic produkty w danym przedziale cenowym.

Wskazowka: nadpisz metode `get_queryset` w swoim `ViewSet`.

## TASK 09 - Zadanie 9 - Relacje w API (challenge)

Stworz dwa modele:

- `Author` z polem `name`
- `Book` z polami:
  - `title`
  - `publication_year`
  - klucz obcy do `Author`

Stworz serializatory i `ViewSety` dla obu modeli.

Zmodyfikuj `BookSerializer` tak, aby przy wyswietlaniu ksiazki pokazywal nazwe autora, a nie tylko jego ID.

Wskazowka: poszukaj informacji o `Nested Serializers` albo `StringRelatedField` w dokumentacji DRF.

## TASK 10 - Zadanie 10 - Wlasna walidacja w serializatorze

W serializatorze dla notatek z zadania 6 dodaj wlasna metode walidacji:

```python
validate_title
```

Metoda powinna sprawdzic, czy tytul notatki nie jest krotszy niz 5 znakow.

Jesli tytul jest za krotki, serializator powinien zwrocic blad walidacji z odpowiednim komunikatem.

Przetestuj dzialanie, probujac dodac za krotka notatke przez Postmana.
