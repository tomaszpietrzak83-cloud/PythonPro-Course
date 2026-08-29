# Lekcja 26: Middleware, JWT i uwierzytelnianie w Django REST Framework

`#lekcja` `#python` `#django` `#drf` `#jwt` `#middleware` `#uwierzytelnianie` `#api`

W tej lekcji zajmiemy się jednym z najważniejszych aspektów każdej aplikacji webowej: uwierzytelnianiem i autoryzacją.

Poznamy dwa kluczowe tematy:

- **Django Middleware** - mechanizm pozwalający globalnie modyfikować zapytania i odpowiedzi,
- **JWT (JSON Web Tokens)** - standard uwierzytelniania w bezstanowych aplikacjach, takich jak API.

Na końcu połączymy tę wiedzę, aby zbudować system rejestracji i logowania w projekcie Django REST Framework.

<p style="color:red"><strong>Komentarz mentora:</strong> JWT nie zastępuje całego systemu bezpieczeństwa. Rozwiązuje głównie problem przekazania informacji o zalogowanym użytkowniku w API.</p>

## 1. Django Middleware

Zanim przejdziemy do uwierzytelniania, musimy zrozumieć, jak Django przetwarza każde zapytanie przychodzące do serwera.

Wyobraź sobie linię produkcyjną. Zapytanie HTTP (`request`) wchodzi na jednym końcu, a odpowiedź (`response`) wychodzi z drugiego. Middleware to kolejne elementy tej linii. Każdy z nich może wykonać jakąś operację na requestach albo response'ach.

W pliku `settings.py` projektu znajdziesz listę `MIDDLEWARE`. Jej kolejność ma duże znaczenie.

> [!definition]
>
> Middleware, czyli oprogramowanie pośredniczące, to framework "haków" w procesie przetwarzania zapytań i odpowiedzi w Django. To system niskopoziomowych "wtyczek", które globalnie wpływają na dane wejściowe i wyjściowe aplikacji.

Przykładowa lista middleware:

```python
# settings.py

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # zarządza sesjami
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # ochrona CSRF
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # dodaje request.user
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

## 2. Jak działa middleware?

Proces przetwarzania requestu można przedstawić jako dwie ścieżki:

1. **Zapytanie (`Request`)** - przechodzi przez middleware od góry do dołu, zanim dotrze do widoku.
2. **Odpowiedź (`Response`)** - po wygenerowaniu przez widok przechodzi przez middleware od dołu do góry.

Schemat:

```text
Zapytanie HTTP
    -> Middleware 1
    -> Middleware 2
    -> ...
    -> Widok
    <- ...
    <- Middleware 2
    <- Middleware 1
Odpowiedź HTTP
```

Możemy też tworzyć własne komponenty middleware, na przykład do:

- logowania każdego zapytania,
- dodawania specjalnych nagłówków,
- blokowania dostępu z określonych adresów IP.

> [!info]
>
> Jednym z najważniejszych middleware jest `AuthenticationMiddleware`. To ono sprawdza informacje o sesji lub tokenach i dołącza obiekt `request.user` do każdego zapytania. Dzięki temu w widokach możemy sprawdzić, czy użytkownik jest zalogowany.

Przykład prostego własnego middleware:

```python
# my_app/middleware.py

class SimpleLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Jednorazowa konfiguracja i inicjalizacja

    def __call__(self, request):
        # Kod wykonywany przed widokiem
        print(f"Przetwarzam zapytanie do ścieżki: {request.path}")

        response = self.get_response(request)

        # Kod wykonywany po widoku
        print(f"Zwracam odpowiedź z kodem statusu: {response.status_code}")
        return response
```

<p style="color:red"><strong>Komentarz mentora:</strong> Przy własnym middleware najłatwiej pomylić kolejność działania. Kod przed `self.get_response(request)` działa przed widokiem, a kod po tej linii działa po widoku.</p>

## 3. JWT (JSON Web Token)

W tradycyjnych aplikacjach Django stan zalogowania użytkownika jest przechowywany w sesji na serwerze.

W przypadku API, zwłaszcza w architekturze mikroserwisów, często dążymy do bezstanowości, czyli **statelessness**. Oznacza to, że serwer nie musi pamiętać stanu klienta między zapytaniami. Każde zapytanie powinno zawierać informacje potrzebne do jego przetworzenia.

Tu z pomocą przychodzi JWT.

> [!definition]
>
> JSON Web Token (JWT) to otwarty standard (RFC 7519), który definiuje kompaktowy i samowystarczalny sposób bezpiecznej transmisji informacji między stronami w postaci obiektu JSON. Informacje mogą być zweryfikowane, ponieważ token jest cyfrowo podpisany.

Token JWT składa się z trzech części oddzielonych kropkami:

```text
xxxxx.yyyyy.zzzzz
```

Te części to:

1. **Header** - typ tokenu i algorytm haszujący, na przykład `HS256`.
2. **Payload** - dane, czyli tak zwane claims, na przykład ID użytkownika, nazwa, role lub czas wygaśnięcia tokenu.
3. **Signature** - podpis, który pozwala sprawdzić, czy token nie został zmieniony.

> [!tip]
>
> Kluczową zaletą JWT jest to, że serwer nie musi przechowywać informacji o tokenie. Wystarczy, że zna sekretny klucz. Gdy otrzyma token, może zweryfikować jego podpis i odczytać dane z payloadu.

<p style="color:red"><strong>Komentarz mentora:</strong> Payload JWT można odczytać po stronie klienta. Nie wkładaj tam haseł, tokenów API ani innych wrażliwych danych.</p>

## 4. Rejestracja i logowanie z JWT w DRF

Ręczna implementacja systemu JWT byłaby skomplikowana. W tej lekcji używamy dwóch popularnych pakietów:

- `djangorestframework-simplejwt` - do obsługi tokenów JWT,
- `djoser` - do gotowych endpointów rejestracji, logowania, zmiany hasła itd.

### 4.1. Instalacja i konfiguracja

Instalacja bibliotek:

```bash
pip install djangorestframework-simplejwt djoser
```

Konfiguracja `settings.py`:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    # ...
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

Konfiguracja głównego pliku `urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
```

## 5. Rejestracja nowego użytkownika

Dzięki Djoserowi rejestracja jest prosta. Wysyłamy zapytanie `POST` na endpoint:

```text
/auth/users/
```

Body w formacie JSON:

```json
{
  "username": "nowy_uzytkownik",
  "password": "bardzoTrudneHaslo123",
  "email": "test@example.com"
}
```

Jeśli dane są poprawne, Djoser stworzy nowego użytkownika w bazie danych i zwróci odpowiedź z kodem:

```text
201 Created
```

## 6. Logowanie, czyli uzyskiwanie tokenów

Aby się zalogować i uzyskać tokeny JWT, wysyłamy zapytanie `POST` na endpoint:

```text
/auth/jwt/create/
```

Body w formacie JSON:

```json
{
  "username": "nowy_uzytkownik",
  "password": "bardzoTrudneHaslo123"
}
```

W odpowiedzi serwer zwróci dwa tokeny:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

> [!note]
>
> **Access token** jest krótkotrwały, na przykład ważny 5 minut. Używamy go do uwierzytelniania każdego zapytania do chronionych zasobów API.
>
> **Refresh token** jest długotrwały, na przykład ważny 1 dzień. Służy do uzyskania nowego access tokenu bez ponownego logowania użytkownika.

## 7. Dostęp do chronionych zasobów

Mając ważny `access token`, możemy wysyłać zapytania do endpointów wymagających uwierzytelnienia.

Token trzeba umieścić w nagłówku `Authorization` z prefiksem `Bearer`:

```http
Authorization: Bearer <twoj_access_token>
```

Gdy DRF otrzyma takie zapytanie, `JWTAuthentication` automatycznie zweryfikuje token. Jeśli token jest poprawny, użytkownik będzie dostępny w:

```python
request.user
```

<p style="color:red"><strong>Komentarz mentora:</strong> W praktyce błąd `401 Unauthorized` bardzo często wynika z braku słowa `Bearer` albo z użycia starego, wygasłego access tokenu.</p>

## 8. Podsumowanie

W tej lekcji pojawiły się trzy główne elementy:

- `Middleware` - warstwa przetwarzająca requesty i response'y w Django.
- `JWT` - podpisany token używany do bezstanowego uwierzytelniania API.
- `Djoser` i `Simple JWT` - biblioteki, które dają gotową obsługę rejestracji, logowania i tokenów w DRF.
