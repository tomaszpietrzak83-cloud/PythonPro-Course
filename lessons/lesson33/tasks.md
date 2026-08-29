# Lesson 33 - Zadania

## TASK 01 - Pierwsze API (proste)

Stwórz aplikację FastAPI z trzema endpointami:

- `GET /` - zwraca `{"message": "Hello"}`,
- `GET /time` - zwraca aktualny czas,
- `GET /random` - zwraca losową liczbę od 1 do 100.

Uruchom aplikację przez:

```bash
uvicorn main:app --reload
```

## TASK 02 - Path params (proste)

Dodaj endpoint:

```text
GET /greet/{name}
```

Endpoint ma zwracać powitanie dla podanego imienia.

Dodaj walidację, aby `name` miało minimum 2 znaki.

## TASK 03 - Query params: kalkulator (proste)

Stwórz endpoint:

```text
GET /calculate
```

Parametry:

- `a: int`,
- `b: int`,
- `operation: str = "add"`.

Obsłuż operacje:

- `add`,
- `subtract`,
- `multiply`,
- `divide`.

Przy dzieleniu przez zero zwróć błąd HTTP.

## TASK 04 - Model Pydantic: Product (proste)

Zdefiniuj model `Product` z polami:

- `name`,
- `price`,
- `quantity`.

Dodaj endpoint:

```text
POST /products
```

Endpoint ma przyjmować produkt i zwracać go razem z polem:

```text
total_price = price * quantity
```

## TASK 05 - CRUD w pamięci: książki (średnie)

Stwórz prostą bazę w pamięci:

```python
books = {}
```

Dodaj endpointy:

- `GET /books`,
- `GET /books/{id}`,
- `POST /books`,
- `DELETE /books/{id}`.

## TASK 06 - Status codes (średnie)

Rozbuduj zadanie 5 o poprawne statusy HTTP:

- `201 Created` przy tworzeniu książki,
- `204 No Content` przy usuwaniu książki,
- `404 Not Found`, gdy książka nie istnieje.

## TASK 07 - Email validation (proste)

Stwórz model `User` z polem:

```python
email: EmailStr
```

Dodaj endpoint:

```text
POST /users
```

Endpoint ma walidować poprawność adresu email.

## TASK 08 - Dokumentacja API (proste)

Dodaj do aplikacji:

- `title`,
- `description`,
- `version`,
- tagi endpointów,
- docstringi z przykładami.

Sprawdź wynik pod adresem:

```text
/docs
```

## TASK 09 - APIRouter (średnie)

Podziel aplikację książek na pliki:

```text
main.py
routers/
    books.py
    authors.py
```

Użyj `APIRouter` i `include_router`.

## TASK 10 - Dependency Injection: API key (średnie)

Stwórz dependency:

```python
verify_api_key
```

Dependency ma sprawdzać nagłówek:

```text
X-API-Key
```

Użyj tej dependency w trzech endpointach.

## TASK 11 - Modele zagnieżdżone (średnie)

Stwórz modele:

- `Author` z polami `name` i `email`,
- `Book` z polami `title`, `author: Author`, `price`.

Dodaj endpoint:

```text
POST /books
```

Endpoint ma przyjmować zagnieżdżony JSON.

## TASK 12 - Custom validators (średnie)

Stwórz model `Product` z walidatorami:

- `name` może zawierać tylko litery i cyfry,
- `price` musi być większe od `0` i nie większe niż `10000`,
- `category` musi być jedną z wartości: `Electronics`, `Books`, `Clothing`.

<p style="color:red"><strong>Komentarz mentora:</strong> Jeśli używasz Pydantic v2, zrób to przez `@field_validator`. W starszych materiałach możesz spotkać `@validator`.</p>

## TASK 13 - SQLAlchemy Integration (trudne)

Przepisz API książek tak, aby używało asynchronicznego SQLAlchemy.

Wymagania:

- model ORM `Book`,
- schematy Pydantic do tworzenia i odpowiedzi,
- dependency do sesji bazy danych,
- pełny CRUD.

## TASK 14 - Relacja one-to-many (trudne)

Dodaj relację:

```text
Author -> wiele Books
```

Dodaj endpoint:

```text
GET /authors/{id}/books
```

Użyj eager loading, na przykład:

```python
selectinload()
```

## TASK 15 - Background Tasks (średnie)

Rozbuduj API książek:

- po utworzeniu książki zapisz informację email/log do pliku,
- po usunięciu książki zaktualizuj statystyki.

Użyj `BackgroundTasks`.

## TASK 16 - Middleware Logging (średnie)

Dodaj middleware, które:

- loguje metodę requestu,
- loguje ścieżkę,
- mierzy czas obsługi,
- dodaje nagłówek `X-Request-ID`,
- zapisuje logi do pliku `requests.log`.

## TASK 17 - Startup/Shutdown Events (średnie)

Dodaj logikę startu i zamknięcia aplikacji:

- przy starcie zainicjalizuj bazę danych,
- przy starcie wczytaj cache z pliku JSON,
- przy zamknięciu zapisz cache do pliku,
- przy zamknięciu zamknij połączenia z bazą.

<p style="color:red"><strong>Komentarz mentora:</strong> W nowych projektach FastAPI sprawdź mechanizm `lifespan`. `startup` i `shutdown` przez `on_event` są często w starszych przykładach.</p>

## TASK 18 - Pagination i filtering (trudne)

Rozbuduj endpoint:

```text
GET /books
```

Dodaj parametry:

- `skip`,
- `limit`,
- `category`,
- `min_price`,
- `max_price`,
- `sort_by`, na przykład `price` albo `title`.

## TASK 19 - Blog API (projekt)

Stwórz mini Blog API.

Wymagania:

- CRUD użytkowników,
- CRUD postów,
- tylko autor może edytować swój post,
- dodawanie komentarzy do postów,
- endpoint `GET /posts/{id}/with-comments`,
- eager loading dla komentarzy,
- background task wysyłający email po nowym komentarzu.

## TASK 20 - AI Integration (projekt)

Rozbuduj Blog API o funkcje AI:

- `POST /posts/{id}/summarize` - podsumowanie posta przez OpenAI API albo symulację,
- background task analizujący sentyment komentarzy,
- middleware automatycznie wykrywające wulgaryzmy lub niedozwoloną treść.

<p style="color:red"><strong>Komentarz mentora:</strong> Jeśli używasz prawdziwego OpenAI API, sprawdź aktualny styl SDK i endpointów. Do ćwiczenia architektury wystarczy też symulacja odpowiedzi.</p>
