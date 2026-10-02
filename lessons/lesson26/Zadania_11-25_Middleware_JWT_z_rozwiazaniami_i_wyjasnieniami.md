## **Zadania podstawowe – poziom 1**

#### **11. 🔧 Zadanie 11 – Własny nagłówek w odpowiedzi**

**Treść zadania**

Stwórz middleware, który do każdej odpowiedzi HTTP dodaje nagłówek `X-App-Name` o wartości `DjangoJWT`. Uruchom aplikację i sprawdź w pliku `.http` klienta REST, czy nagłówek pojawia się zarówno dla zwykłego endpointu, jak i dla endpointu uwierzytelniania.

**Rozwiązanie**

`api/middleware.py`:

```python
class AppNameHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response["X-App-Name"] = "DjangoJWT"

        return response
```

Dodaj middleware do `settings.py`:

```python
MIDDLEWARE = [
    # ...
    "api.middleware.AppNameHeaderMiddleware",
]
```

Uruchom serwer i wykonaj np.:

```http
GET http://127.0.0.1:8000/user/
```

oraz:

```http
POST http://127.0.0.1:8000/auth/jwt/create/
```

W zakładce **Headers** odpowiedzi powinien znajdować się:

```text
X-App-Name: DjangoJWT
```

**Dokładne wyjaśnienie**

Najpierw middleware przekazuje request dalej:

```python
response = self.get_response(request)
```

Dopiero po uzyskaniu odpowiedzi dodaje nagłówek:

```python
response["X-App-Name"] = "DjangoJWT"
```

Dzięki temu nagłówek trafia do odpowiedzi niezależnie od tego, który widok ją utworzył. To pokazuje jedną z największych zalet middleware: możliwość zastosowania jednej reguły globalnie.

---

#### **12. 🔧 Zadanie 12 – Sprawdzenie kolejności middleware**

**Treść zadania**

Utwórz `FirstMiddleware` i `SecondMiddleware`. Każdy ma wypisywać komunikat przed oraz po `get_response()`.

**Rozwiązanie**

`api/middleware.py`:

```python
class FirstMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("FIRST: przed get_response")

        response = self.get_response(request)

        print("FIRST: po get_response")
        return response


class SecondMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("SECOND: przed get_response")

        response = self.get_response(request)

        print("SECOND: po get_response")
        return response
```

W `settings.py`:

```python
MIDDLEWARE = [
    # ...
    "api.middleware.FirstMiddleware",
    "api.middleware.SecondMiddleware",
]
```

Przykładowy wynik:

```text
FIRST: przed get_response
SECOND: przed get_response
SECOND: po get_response
FIRST: po get_response
```

**Dokładne wyjaśnienie**

Request przechodzi przez middleware od góry do dołu:

```text
First -> Second -> widok
```

Response wraca w odwrotnej kolejności:

```text
widok -> Second -> First
```

Dlatego mechanizm middleware często porównuje się do cebuli: wchodzimy przez kolejne warstwy i wracamy przez nie w odwrotnej kolejności.

---

#### **13. 🔧 Zadanie 13 – Test błędnych nagłówków Authorization**

**Treść zadania**

Przetestuj cztery warianty nagłówka `Authorization` na chronionym endpointcie.

**Rozwiązanie**

Załóżmy endpoint:

```text
GET /user/
```

Test 1 – brak nagłówka:

```http
GET /user/
```

Oczekiwany rezultat: `401 Unauthorized`.

Test 2 – niepełny nagłówek:

```http
Authorization: Bearer
```

Oczekiwany rezultat: `401 Unauthorized`.

Test 3 – zły prefiks:

```http
Authorization: Token <access_token>
```

Przy konfiguracji z JWT jako mechanizmem uwierzytelniania żądanie nie zostanie poprawnie uwierzytelnione. Dla chronionego endpointu oczekujemy odmowy dostępu, zwykle `401`.

Test 4 – poprawny nagłówek:

```http
Authorization: Bearer <access_token>
```

Oczekiwany rezultat: `200 OK`.

**Dokładne wyjaśnienie**

Simple JWT domyślnie oczekuje schematu:

```text
Bearer <token>
```

Samo słowo `Bearer` nie zawiera tokenu, więc nie wystarcza.

Prefiks `Token` jest używany przez inne mechanizmy uwierzytelniania i nie jest tym samym co `Bearer`.

Dokładna treść odpowiedzi błędu może się różnić zależnie od konfiguracji i wersji bibliotek, ale istotne jest to, że tylko poprawny schemat z prawidłowym access tokenem powinien uwierzytelnić użytkownika.

---

#### **14. 🔧 Zadanie 14 – Access token kontra refresh token w praktyce**

**Treść zadania**

Spróbuj użyć refresh tokenu jako tokenu dostępowego, a potem wykonaj to samo zapytanie z access tokenem.

**Rozwiązanie**

Niepoprawny wariant:

```http
GET /user/
Authorization: Bearer <refresh_token>
```

Oczekiwany rezultat: `401 Unauthorized`.

Poprawny wariant:

```http
GET /user/
Authorization: Bearer <access_token>
```

Oczekiwany rezultat: `200 OK`.

**Dokładne wyjaśnienie**

Oba tokeny są JWT, ale mają inne przeznaczenie. W tokenie znajduje się informacja o jego typie, np.:

```json
{
  "token_type": "refresh"
}
```

albo:

```json
{
  "token_type": "access"
}
```

Mechanizm `JWTAuthentication` oczekuje tokenu typu `access`. Refresh token powinien być wysyłany wyłącznie do endpointu odświeżania:

```text
/auth/jwt/refresh/
```

Rozdzielenie obu tokenów zwiększa bezpieczeństwo. Access token jest używany często, ale żyje krótko. Refresh token żyje dłużej, dlatego powinien być używany rzadziej.

---

#### **15. 🔧 Zadanie 15 – Zmienne w pliku HTTP**

**Treść zadania**

W pliku `.http` zdefiniuj `@baseUrl`, a tokeny pobieraj z odpowiedzi nazwanych zapytań. Użyj danych użytkownika, który już istnieje w bazie projektu.

**Rozwiązanie**

W pliku `task15.http` ustaw adres serwera i dane logowania:

```http
@baseUrl = http://127.0.0.1:8000
@username = twoj_uzytkownik
@password = twoje_haslo
```

Żądanie logowania ma nazwę `login`. Kolejne żądania odczytują tokeny bezpośrednio z odpowiedzi:

```http
Authorization: Bearer {{login.response.body.access}}
```

Do odświeżania plik używa `{{login.response.body.refresh}}`, a następnie tokenu z odpowiedzi nazwanej `refresh`.

**Dokładne wyjaśnienie**

Zmienna `@baseUrl` pozwala zmienić adres aplikacji w jednym miejscu. Klient REST może też wstawiać pola odpowiedzi poprzedniego zapytania, dzięki czemu nie trzeba ręcznie kopiować tokenów.

W tym przykładzie access i refresh token są pobierane z odpowiedzi logowania; są ważne tak długo, jak same tokeny.

---

## **Zadania średnie – poziom 2**

#### **16. ⚙️ Zadanie 16 – Pomiar czasu obsługi zapytania przez middleware**

**Treść zadania**

Stwórz middleware mierzący czas obsługi zapytania, dodający `X-Response-Time` i wypisujący wynik w konsoli.

**Rozwiązanie**

`api/middleware.py`:

```python
import time


class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()

        response = self.get_response(request)

        end = time.perf_counter()
        duration_ms = (end - start) * 1000

        response["X-Response-Time"] = f"{duration_ms:.2f} ms"

        print(
            f"{request.method} {request.path} "
            f"obsłużono w {duration_ms:.2f} ms"
        )

        return response
```

`settings.py`:

```python
MIDDLEWARE = [
    # ...
    "api.middleware.ResponseTimeMiddleware",
]
```

**Dokładne wyjaśnienie**

`time.perf_counter()` nadaje się do mierzenia krótkich odcinków czasu.

Pierwszy pomiar jest wykonywany przed przekazaniem requestu do dalszej części aplikacji, a drugi po otrzymaniu response.

Różnica:

```python
end - start
```

jest podana w sekundach, dlatego mnożymy ją przez `1000`, aby uzyskać milisekundy.

Nagłówek może wyglądać tak:

```text
X-Response-Time: 4.37 ms
```

To prosty przykład obserwowalności aplikacji. W prawdziwych systemach czas odpowiedzi często trafia do logów i narzędzi monitorujących.

---

#### **17. ⚙️ Zadanie 17 – Middleware wymagający własnego nagłówka**

**Treść zadania**

Dla ścieżek zaczynających się od `/api/private/` wymagaj nagłówka `X-Client-Id`. Bez niego zwróć `403`.

**Rozwiązanie**

```python
from django.http import JsonResponse


class ClientIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/private/"):
            client_id = request.headers.get("X-Client-Id")

            if not client_id:
                return JsonResponse(
                    {
                        "detail": "Brak wymaganego nagłówka X-Client-Id."
                    },
                    status=403,
                )

        return self.get_response(request)
```

W `settings.py`:

```python
MIDDLEWARE = [
    # ...
    "api.middleware.ClientIdMiddleware",
]
```

Przykład zaakceptowanego requestu:

```http
GET /api/private/data/
X-Client-Id: frontend-web
```

**Dokładne wyjaśnienie**

Middleware sprawdza najpierw ścieżkę:

```python
request.path.startswith("/api/private/")
```

Jeśli request dotyczy innego endpointu, warunek nie zostaje spełniony i żądanie przechodzi normalnie.

Jeżeli nagłówka brakuje, middleware zwraca `JsonResponse` od razu. Oznacza to, że `self.get_response(request)` nie zostanie wykonane i request nie dotrze do widoku.

To przykład tzw. krótkiego zakończenia requestu na poziomie middleware.

---

#### **18. ⚙️ Zadanie 18 – Endpoint tylko dla administratora**

**Treść zadania**

Utwórz `/api/admin-info/`, dostępny wyłącznie dla administratora.

**Rozwiązanie**

Najprościej użyć `IsAdminUser`:

```python
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


class AdminInfoView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "message": "Witaj w sekcji administratora."
        })
```

`api/urls.py`:

```python
from django.urls import path
from .views import AdminInfoView

urlpatterns = [
    path("admin-info/", AdminInfoView.as_view()),
]
```

Testy:

1. Bez tokenu → odmowa dostępu.
2. Token zwykłego użytkownika → odmowa dostępu.
3. Token użytkownika z `is_staff=True` → `200 OK`.

**Dokładne wyjaśnienie**

`IsAdminUser` w DRF sprawdza, czy użytkownik jest zalogowany i ma ustawione:

```python
user.is_staff == True
```

Nie należy mylić `is_staff` z `is_superuser`. Superuser zazwyczaj ma również `is_staff=True`, ale nie każdy użytkownik staff musi być superuserem.

To zadanie pokazuje różnicę pomiędzy:

- uwierzytelnianiem – kim jesteś,
- autoryzacją – co wolno Ci zrobić.

---

#### **19. ⚙️ Zadanie 19 – Pobieranie danych aktualnego użytkownika przez Djoser**

**Treść zadania**

Wywołaj `/auth/users/me/` z access tokenem, a następnie bez niego.

**Rozwiązanie**

Z tokenem:

```http
GET http://127.0.0.1:8000/auth/users/me/
Authorization: Bearer <access_token>
```

Przykładowa odpowiedź:

```json
{
  "email": "anna@example.com",
  "id": 1,
  "username": "anna"
}
```

Bez tokenu:

```http
GET http://127.0.0.1:8000/auth/users/me/
```

Powinna nastąpić odmowa dostępu.

**Dokładne wyjaśnienie**

Endpoint `users/me/` oznacza „aktualnie uwierzytelniony użytkownik”. Djoser nie potrzebuje ID użytkownika w adresie, ponieważ użytkownik jest ustalany na podstawie mechanizmu uwierzytelniania.

To bardzo typowy wzorzec w API. Frontend może pobrać dane aktualnej osoby bez znajomości jej identyfikatora.

Zakres zwracanych pól może zależeć od konfiguracji serializerów Djosera.

---

#### **20. ⚙️ Zadanie 20 – Automatyzacja logowania w Pythonie**

**Treść zadania**

Napisz skrypt w Pythonie z użyciem `requests`, który loguje użytkownika, pobiera access token i odpytuje chroniony endpoint.

**Rozwiązanie**

Najpierw:

Zależność `requests` jest zapisana w `requirements.txt` lekcji. Zainstaluj ją poleceniem instalacyjnym z pliku `README.md`.

Skrypt:

```python
import os
import requests

BASE_URL = os.getenv("DJANGO_BASE_URL", "http://127.0.0.1:8000")
USERNAME = os.getenv("DJANGO_USERNAME")
PASSWORD = os.getenv("DJANGO_PASSWORD")

login_response = requests.post(
    f"{BASE_URL}/auth/jwt/create/",
    json={
        "username": USERNAME,
        "password": PASSWORD,
    },
)

print("Logowanie:", login_response.status_code)

login_response.raise_for_status()

tokens = login_response.json()
access_token = tokens["access"]

headers = {
    "Authorization": f"Bearer {access_token}"
}

profile_response = requests.get(
    f"{BASE_URL}/user/",
    headers=headers,
)

print("Profil:", profile_response.status_code)
print(profile_response.json())
```

**Dokładne wyjaśnienie**

`requests.post(..., json={...})` automatycznie serializuje słownik do JSON i ustawia odpowiedni `Content-Type`.

`raise_for_status()` zgłosi wyjątek dla odpowiedzi błędnej, np. `400` albo `401`.

Po odczytaniu tokenu:

```python
access_token = tokens["access"]
```

tworzymy standardowy nagłówek JWT:

```python
"Authorization": f"Bearer {access_token}"
```

Skrypt wykonuje żądania do tego samego serwera i użytkownika z istniejącej bazy, co przykłady w plikach `.http`.

---

## **Zadania zaawansowane – poziom 3**

#### **21. 🚀 Zadanie 21 – Automatyczne odświeżenie tokenu w skrypcie**

**Treść zadania**

Jeśli chroniony endpoint zwróci `401`, użyj refresh tokenu, pobierz nowy access token i ponów zapytanie.

**Rozwiązanie**

```python
import os
import requests

BASE_URL = os.getenv("DJANGO_BASE_URL", "http://127.0.0.1:8000")
USERNAME = os.getenv("DJANGO_USERNAME")
PASSWORD = os.getenv("DJANGO_PASSWORD")


def login():
    response = requests.post(
        f"{BASE_URL}/auth/jwt/create/",
        json={
            "username": USERNAME,
            "password": PASSWORD,
        },
    )
    response.raise_for_status()
    return response.json()


def refresh_access_token(refresh_token):
    response = requests.post(
        f"{BASE_URL}/auth/jwt/refresh/",
        json={
            "refresh": refresh_token
        },
    )
    response.raise_for_status()
    return response.json()["access"]


def get_profile(access_token):
    return requests.get(
        f"{BASE_URL}/user/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )


tokens = login()

access_token = tokens["access"]
refresh_token = tokens["refresh"]

response = get_profile(access_token)

if response.status_code == 401:
    print("Access token nie działa. Próbuję go odświeżyć...")

    access_token = refresh_access_token(refresh_token)
    response = get_profile(access_token)

if response.ok:
    print("Sukces:", response.status_code)
    print(response.json())
else:
    print("Błąd:", response.status_code)
    print(response.text)
```

**Dokładne wyjaśnienie**

Program rozdzielono na trzy funkcje:

- `login()` – pobiera oba tokeny,
- `refresh_access_token()` – uzyskuje nowy access token,
- `get_profile()` – wykonuje zapytanie do chronionego API.

Najważniejsza część:

```python
if response.status_code == 401:
```

oznacza, że dopiero po odmowie uwierzytelnienia klient próbuje odświeżyć token.

Po uzyskaniu nowego access tokenu request zostaje wykonany ponownie.

W prawdziwej aplikacji należy uważać, ponieważ `401` może pojawić się także z innych powodów niż samo wygaśnięcie tokenu. Tutaj upraszczamy logikę na potrzeby ćwiczenia.

---

#### **22. 🚀 Zadanie 22 – Identyfikator każdego requestu**

**Treść zadania**

Wygeneruj `request_id`, zapisz go w `request.request_id` i dodaj do nagłówka `X-Request-ID`.

**Rozwiązanie**

`api/middleware.py`:

```python
import uuid


class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.request_id = request_id

        response = self.get_response(request)

        response["X-Request-ID"] = request_id

        return response
```

Widok:

```python
from rest_framework.response import Response
from rest_framework.views import APIView


class RequestIdView(APIView):
    def get(self, request):
        return Response({
            "request_id": request.request_id
        })
```

URL:

```python
path("request-id/", RequestIdView.as_view()),
```

**Dokładne wyjaśnienie**

`uuid.uuid4()` generuje praktycznie unikalny identyfikator.

Przed wywołaniem widoku zapisujemy go jako:

```python
request.request_id
```

Dzięki temu widok i inne elementy aplikacji mogą z niego korzystać.

Po wykonaniu widoku ten sam identyfikator trafia do response:

```python
response["X-Request-ID"] = request_id
```

Wynik może wyglądać tak:

Body:

```json
{
  "request_id": "57a5cf88-c3f2-4dbc-9768-8c8ac9235f07"
}
```

Header:

```text
X-Request-ID: 57a5cf88-c3f2-4dbc-9768-8c8ac9235f07
```

Request ID jest bardzo przydatny przy analizie logów. Jeżeli użytkownik zgłosi błąd i poda identyfikator requestu, można łatwiej znaleźć wszystkie logi dotyczące konkretnego żądania.

---

#### **23. 🚀 Zadanie 23 – Blokowanie wybranych adresów IP**

**Treść zadania**

Dodaj `BLOCKED_IPS` i stwórz middleware zwracający `403`, jeśli adres klienta jest na liście.

**Rozwiązanie**

`settings.py`:

```python
BLOCKED_IPS = [
    "127.0.0.1",
]
```

`api/middleware.py`:

```python
from django.conf import settings
from django.http import JsonResponse


class BlockIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = request.META.get("REMOTE_ADDR")

        if client_ip in settings.BLOCKED_IPS:
            return JsonResponse(
                {
                    "detail": "Dostęp z tego adresu IP został zablokowany."
                },
                status=403,
            )

        return self.get_response(request)
```

Dodaj:

```python
"api.middleware.BlockIpMiddleware",
```

do `MIDDLEWARE`.

**Dokładne wyjaśnienie**

Django udostępnia informacje o połączeniu HTTP w `request.META`.

W prostym środowisku lokalnym:

```python
request.META.get("REMOTE_ADDR")
```

zwykle zwróci np. `127.0.0.1`.

Jeżeli wartość jest na liście:

```python
settings.BLOCKED_IPS
```

request zostaje zakończony przed wejściem do widoku.

W prawdziwej aplikacji stojącej za reverse proxy ustalanie rzeczywistego IP klienta jest bardziej złożone. Nie należy bezwarunkowo ufać nagłówkom takim jak `X-Forwarded-For`, jeżeli infrastruktura nie jest do tego poprawnie skonfigurowana.

---

#### **24. 🚀 Zadanie 24 – Własne dane w tokenie JWT**

**Treść zadania**

Dodaj do payloadu tokenu własny claim, np. `username`.

**Rozwiązanie**

Utwórz własny serializer:

`api/serializers.py`:

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username

        return token
```

Następnie własny widok:

`api/views.py`:

```python
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

URL:

```python
from django.urls import path
from .views import CustomTokenObtainPairView

urlpatterns = [
    path(
        "jwt/custom-create/",
        CustomTokenObtainPairView.as_view(),
        name="custom_token_obtain_pair",
    ),
]
```

Wyślij:

```http
POST /api/jwt/custom-create/
```

z loginem i hasłem.

Po zdekodowaniu access tokenu powinien pojawić się claim:

```json
{
  "username": "anna"
}
```

**Dokładne wyjaśnienie**

Metoda:

```python
get_token(cls, user)
```

tworzy token dla użytkownika.

Najpierw wywołujemy implementację bazową:

```python
token = super().get_token(user)
```

a następnie dokładamy własną informację:

```python
token["username"] = user.username
```

Standardowe pola tokenu pozostają zachowane, dlatego token nadal może być obsługiwany przez `JWTAuthentication`.

Nie należy umieszczać w tokenie haseł, kluczy API ani innych sekretów. Payload JWT można łatwo odczytać bez znajomości sekretnego klucza. Podpis chroni token przed niezauważoną modyfikacją, ale nie szyfruje zawartości.

---

#### **25. 🚀 Zadanie 25 – Mini-system API z pełnym przepływem uwierzytelniania**

**Treść zadania**

Zbuduj moduł `notes`, w którym:

- `/api/status/` jest publiczny,
- zalogowany użytkownik widzi własne notatki,
- nie widzi notatek innych użytkowników,
- administrator może sprawdzić liczbę wszystkich użytkowników,
- każde zapytanie dostaje `X-Request-ID`,
- logowanie i odświeżanie odbywają się przez JWT.

**Rozwiązanie**

### Krok 1 – utworzenie aplikacji

```bash
python manage.py startapp notes
```

Dodaj:

```python
"notes",
```

do `INSTALLED_APPS`.

### Krok 2 – model notatki

`notes/models.py`:

```python
from django.conf import settings
from django.db import models


class Note(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Migracje:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Krok 3 – serializer

`notes/serializers.py`:

```python
from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "created_at",
        ]
```

Celowo nie udostępniamy pola `owner` do ustawienia przez klienta.

### Krok 4 – publiczny status

`notes/views.py`:

```python
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class StatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "status": "ok"
        })
```

### Krok 5 – lista własnych notatek

```python
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Note
from .serializers import NoteSerializer


class MyNotesView(ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(
            owner=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

### Krok 6 – pojedyncza notatka tylko właściciela

```python
from rest_framework.generics import RetrieveUpdateDestroyAPIView


class MyNoteDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(
            owner=self.request.user
        )
```

Dzięki filtrowaniu querysetu użytkownik nie uzyska dostępu do obiektu należącego do innej osoby.

### Krok 7 – endpoint administratora

```python
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser


class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        User = get_user_model()

        return Response({
            "users_count": User.objects.count()
        })
```

### Krok 8 – URL-e

`notes/urls.py`:

```python
from django.urls import path

from .views import (
    AdminStatsView,
    MyNoteDetailView,
    MyNotesView,
    StatusView,
)

urlpatterns = [
    path("status/", StatusView.as_view()),
    path("notes/", MyNotesView.as_view()),
    path("notes/<int:pk>/", MyNoteDetailView.as_view()),
    path("admin-stats/", AdminStatsView.as_view()),
]
```

W głównym `urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),

    path("api/", include("notes.urls")),
]
```

### Krok 9 – Request ID

Możesz wykorzystać middleware z zadania 22:

```python
import uuid


class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.request_id = request_id

        response = self.get_response(request)

        response["X-Request-ID"] = request_id
        return response
```

i dodać go do `MIDDLEWARE`.

### Krok 10 – testy

Przykładowa tabela:

| Endpoint | Metoda | Dostęp | Oczekiwany rezultat |
|---|---|---|---|
| `/api/status/` | GET | każdy | `200` |
| `/api/notes/` | GET | zalogowany | `200` |
| `/api/notes/` | GET | niezalogowany | odmowa dostępu |
| `/api/notes/` | POST | zalogowany | `201` |
| `/api/notes/<id>/` | GET | właściciel | `200` |
| `/api/notes/<id>/` | GET | inny użytkownik | brak dostępu do obiektu, typowo `404` przy takim filtrowaniu querysetu |
| `/api/admin-stats/` | GET | zwykły użytkownik | odmowa dostępu |
| `/api/admin-stats/` | GET | administrator/staff | `200` |
| `/auth/jwt/create/` | POST | poprawny login i hasło | `200` |
| `/auth/jwt/refresh/` | POST | poprawny refresh token | `200` |

Projekt używa skonfigurowanej już bazy. Po dodaniu aplikacji `notes` zastosuj migrację, aby utworzyć tabelę w tej bazie. Przykładowe rekordy można dodać użytkownikom, którzy już istnieją:

```bash
python manage.py migrate
python manage.py seed_notes --username istniejący_użytkownik
```

Polecenie `seed_notes` nie tworzy kont ani nowej bazy. Możesz uruchomić je dla dwóch różnych istniejących użytkowników, aby sprawdzić, że każdy widzi wyłącznie własne notatki.

**Dokładne wyjaśnienie**

To zadanie łączy wszystkie najważniejsze elementy lekcji.

Publiczny endpoint korzysta z:

```python
permission_classes = [AllowAny]
```

Lista notatek używa:

```python
permission_classes = [IsAuthenticated]
```

Najważniejszy mechanizm ochrony danych użytkowników znajduje się w:

```python
Note.objects.filter(owner=self.request.user)
```

Nie pobieramy wszystkich notatek, a potem nie sprawdzamy właściciela ręcznie. Już sam queryset zawiera wyłącznie dane aktualnego użytkownika.

Podczas tworzenia notatki właściciel jest ustawiany po stronie serwera:

```python
serializer.save(owner=self.request.user)
```

Dzięki temu klient nie może przesłać dowolnego `owner_id` i stworzyć notatki przypisanej do innego użytkownika.

Endpoint administratora wykorzystuje `IsAdminUser`, czyli autoryzację opartą na uprawnieniach użytkownika.

`RequestIdMiddleware` pokazuje zastosowanie middleware do funkcjonalności przekrojowej – identyfikator jest dodawany globalnie, a nie osobno w każdym widoku.

Cały przepływ klienta wygląda następująco:

```text
1. POST /auth/jwt/create/
        ↓
2. access + refresh
        ↓
3. Authorization: Bearer <access>
        ↓
4. GET/POST /api/notes/
        ↓
5. access token wygasa
        ↓
6. POST /auth/jwt/refresh/
        ↓
7. nowy access token
        ↓
8. ponowne zapytanie do /api/notes/
```

W praktyce jest to podstawowy schemat uwierzytelniania wielu aplikacji typu SPA, aplikacji mobilnych i innych klientów korzystających z REST API.
