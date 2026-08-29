# Lesson 26 - Zadania

## TASK 01 - Zadanie 1 - Analiza middleware (proste)

W nowo utworzonym projekcie Django otwórz plik `settings.py`.

Znajdź listę `MIDDLEWARE` i wyjaśnij w jednym zdaniu, za co według Ciebie odpowiadają:

- `SessionMiddleware`
- `AuthenticationMiddleware`

## TASK 02 - Zadanie 2 - Instalacja zależności (proste)

Utwórz nowy projekt Django z wirtualnym środowiskiem.

Zainstaluj w nim Django, Django REST Framework, `djangorestframework-simplejwt` oraz `djoser`.

Zapisz wszystkie zależności do pliku `requirements.txt` za pomocą komendy:

```bash
pip freeze > requirements.txt
```

## TASK 03 - Zadanie 3 - Podstawowa konfiguracja (proste)

W projekcie z poprzedniego zadania skonfiguruj plik `settings.py` zgodnie z instrukcjami z lekcji.

Dodaj odpowiednie wpisy do:

- `INSTALLED_APPS`
- `REST_FRAMEWORK`

## TASK 04 - Zadanie 4 - Konfiguracja URL-i (proste)

Skonfiguruj główny plik `urls.py` swojego projektu, aby zawierał ścieżki URL dostarczane przez bibliotekę Djoser dla uwierzytelniania i obsługi JWT.

## TASK 05 - Zadanie 5 - Rejestracja przez Postmana (proste)

Uruchom serwer deweloperski Django.

Użyj narzędzia Postman lub podobnego, aby wysłać zapytanie `POST` na endpoint:

```text
/auth/users/
```

Zarejestruj nowego użytkownika.

Sprawdź w panelu admina Django, czy użytkownik faktycznie został utworzony.

## TASK 06 - Zadanie 6 - Logowanie i inspekcja tokenu (challenge)

Używając Postmana, wyślij zapytanie `POST` na endpoint:

```text
/auth/jwt/create/
```

Zaloguj użytkownika utworzonego w poprzednim zadaniu.

Skopiuj otrzymany `access token` i wklej go na stronie `jwt.io`.

Przeanalizuj zdekodowane dane w sekcji `Payload`.

Odpowiedz:

- Czy widzisz tam `user_id`?
- Jaki jest czas wygaśnięcia, czyli `exp`?

## TASK 07 - Zadanie 7 - Tworzenie własnego middleware (challenge)

Stwórz proste własne middleware, które dla każdego przychodzącego zapytania będzie dodawało do konsoli informację o metodzie HTTP.

Użyj `print()`.

Przykład:

```text
Otrzymano zapytanie metodą GET
```

Pamiętaj, aby dodać swoje middleware do listy `MIDDLEWARE` w `settings.py`.

## TASK 08 - Zadanie 8 - Chroniony endpoint (challenge)

Stwórz prosty widok w DRF oparty o `APIView`, który będzie dostępny tylko dla zalogowanych użytkowników.

Ustaw:

```python
permission_classes = [IsAuthenticated]
```

Widok powinien zwracać nazwę zalogowanego użytkownika:

```python
request.user.username
```

Przetestuj go w Postmanie:

- najpierw bez tokenu - powinieneś otrzymać błąd `401`,
- potem z poprawnym nagłówkiem `Authorization: Bearer <token>`.

## TASK 09 - Zadanie 9 - Konfiguracja czasu życia tokenu (challenge)

W pliku `settings.py` zmień konfigurację `SIMPLE_JWT` tak, aby `ACCESS_TOKEN_LIFETIME` wynosił:

```python
timedelta(seconds=10)
```

Zaloguj się ponownie, aby uzyskać nowy token.

Spróbuj użyć go do odpytania chronionego endpointu z zadania 8.

Odczekaj 10 sekund i spróbuj ponownie.

Jaką odpowiedź otrzymałeś za drugim razem?

## TASK 10 - Zadanie 10 - Odświeżanie tokenu (challenge)

Wykorzystaj `refresh token`, który otrzymałeś podczas logowania.

Wyślij zapytanie `POST` na endpoint:

```text
/auth/jwt/refresh/
```

Z ciałem:

```json
{
  "refresh": "<twoj_refresh_token>"
}
```

W odpowiedzi powinieneś otrzymać nowy, świeży `access token`.

Sprawdź, czy ten nowy token działa, odpytując chroniony endpoint.
