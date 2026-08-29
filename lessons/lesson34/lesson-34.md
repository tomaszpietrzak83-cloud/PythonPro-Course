# Lekcja 34: WebSockets i GraphQL - komunikacja w czasie rzeczywistym

`#lekcja` `#python` `#websockets` `#graphql` `#real-time` `#async`

W tej lekcji poznasz dwie technologie używane przy bardziej zaawansowanej komunikacji między klientem a serwerem:

- **WebSocket** - protokół do dwukierunkowej komunikacji w czasie rzeczywistym,
- **GraphQL** - język zapytań do API, w którym klient dokładnie określa, jakie dane chce dostać.

WebSocket przydaje się wtedy, gdy serwer ma wysyłać dane do klienta natychmiast, bez ciągłego odpytywania. GraphQL przydaje się wtedy, gdy REST zaczyna wymagać zbyt wielu endpointów albo zwraca za dużo lub za mało danych.

## 1. WebSockets

HTTP działa w modelu request-response:

```text
klient -> request -> serwer -> response
```

Klient musi za każdym razem rozpocząć komunikację. Jeśli chce sprawdzić, czy są nowe dane, musi cyklicznie wysyłać requesty. To podejście nazywa się **polling**.

WebSocket działa inaczej. Połączenie zostaje otwarte raz, a potem obie strony mogą wysyłać wiadomości w dowolnym momencie:

```text
klient <-> serwer
```

### Definicja

**WebSocket** to protokół komunikacyjny zapewniający pełnodupleksową, czyli dwukierunkową, komunikację między klientem a serwerem przez jedno długotrwałe połączenie TCP.

Najważniejsze cechy WebSocketów:

- komunikacja dwukierunkowa,
- niskie opóźnienia,
- mniej narzutu niż ciągłe requesty HTTP,
- jedno aktywne połączenie zamiast wielu krótkich requestów,
- możliwość wysyłania danych przez serwer bez czekania na request klienta.

Typowe zastosowania:

- czaty,
- gry online,
- powiadomienia live,
- dashboardy z danymi w czasie rzeczywistym,
- streaming danych.

## 2. HTTP polling vs WebSocket

Przykład polling HTTP:

```python
import time

import requests


def http_polling():
    url = "http://example.com/api/messages"

    while True:
        response = requests.get(url)
        messages = response.json()

        for message in messages:
            print(f"Nowa wiadomość: {message}")

        time.sleep(2)
```

Problem: nawet jeśli nie ma nowych wiadomości, klient nadal wysyła requesty. Jeśli polling odbywa się co 2 sekundy, wiadomość może pojawić się z opóźnieniem do 2 sekund.

Przykład klienta WebSocket:

```python
import aiohttp


async def websocket_connection():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://example.com/ws") as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(f"Nowa wiadomość: {msg.data}")
                    await ws.send_str("Otrzymałem wiadomość!")
```

Tutaj klient nie odpytuje serwera w pętli. Nasłuchuje wiadomości, które przychodzą natychmiast po wysłaniu przez serwer.

## 3. Handshake WebSocket

Połączenie WebSocket zaczyna się od zwykłego requestu HTTP. Klient prosi serwer o zmianę protokołu.

Przykładowy request klienta:

```http
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

Jeśli serwer akceptuje zmianę protokołu, odpowiada:

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

Status `101 Switching Protocols` oznacza, że serwer zgadza się przejść z HTTP na WebSocket.

Po handshake komunikacja wygląda już tak:

```text
Klient -> Serwer: {"type": "message", "text": "Cześć!"}
Serwer -> Klient: {"type": "message", "text": "Witaj!"}
Serwer -> Klient: {"type": "notification", "text": "Nowy użytkownik dołączył"}
```

## 4. Cykl życia połączenia WebSocket

Typowe połączenie WebSocket ma trzy fazy:

1. **Handshake** - klient i serwer uzgadniają zmianę protokołu.
2. **Aktywne połączenie** - strony wysyłają i odbierają wiadomości.
3. **Zamknięcie** - jedna albo obie strony zamykają połączenie.

Przykładowa klasa pokazująca cykl życia:

```python
class WebSocketConnection:
    def __init__(self, websocket):
        self.websocket = websocket
        self.is_connected = False

    async def connect(self):
        self.is_connected = True
        print("Połączono z serwerem WebSocket")
        await self.send_message({"type": "hello", "client": "Python"})

    async def send_message(self, message):
        if self.is_connected:
            await self.websocket.send_json(message)
            print(f"Wysłano: {message}")

    async def receive_messages(self):
        while self.is_connected:
            try:
                message = await self.websocket.receive_json()
                print(f"Otrzymano: {message}")
                await self.handle_message(message)
            except Exception as error:
                print(f"Błąd połączenia: {error}")
                self.is_connected = False
                break

    async def handle_message(self, message):
        msg_type = message.get("type")

        if msg_type == "ping":
            await self.send_message({"type": "pong"})
        elif msg_type == "notification":
            print(f"Powiadomienie: {message.get('text')}")

    async def disconnect(self):
        if self.is_connected:
            await self.websocket.close()
            self.is_connected = False
            print("Rozłączono z serwerem")
```

## 5. Kiedy używać WebSocketów

Używaj WebSocketów, gdy potrzebujesz komunikacji real-time:

- użytkownicy widzą wiadomości natychmiast,
- serwer sam wysyła powiadomienia,
- stan gry musi być synchronizowany,
- dashboard ma aktualizować dane bez odświeżania strony.

Nie używaj WebSocketów do zwykłych operacji CRUD, takich jak:

- pobranie listy produktów,
- dodanie rekordu,
- edycja profilu,
- wyszukiwanie.

Do takich przypadków prostsze i czytelniejsze jest zwykłe HTTP albo REST API.

## 6. WebSocket w Pythonie z `aiohttp`

`aiohttp` obsługuje WebSockety po stronie serwera i klienta. Jest oparte o `asyncio`, dlatego dobrze nadaje się do obsługi wielu jednoczesnych połączeń.

### Definicja

**Aiohttp WebSocket** to asynchroniczna implementacja WebSocketów w bibliotece `aiohttp`, pozwalająca tworzyć serwery i klientów WebSocket w Pythonie.

Instalacja:

```bash
pip install aiohttp
```

## 7. Prosty echo server

Echo server zwraca klientowi wiadomość, którą od niego dostał.

```python
from aiohttp import web


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("Nowy klient połączony")

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            print(f"Otrzymano: {msg.data}")
            await ws.send_str(f"Echo: {msg.data}")
        elif msg.type == web.WSMsgType.ERROR:
            print(f"Błąd WebSocket: {ws.exception()}")

    print("Klient rozłączony")
    return ws


app = web.Application()
app.router.add_get("/ws", websocket_handler)

if __name__ == "__main__":
    print("Serwer WebSocket działa na ws://localhost:8080/ws")
    web.run_app(app, host="localhost", port=8080)
```

Test w konsoli przeglądarki:

```javascript
const ws = new WebSocket("ws://localhost:8080/ws");
ws.onmessage = (event) => console.log(event.data);
ws.send("Cześć!");
```

## 8. Klient WebSocket w `aiohttp`

```python
import asyncio

import aiohttp


async def websocket_client():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://localhost:8080/ws") as ws:
            print("Połączono z serwerem")

            messages = ["Cześć!", "Jak się masz?", "Do widzenia!"]

            for message in messages:
                await ws.send_str(message)
                print(f"Wysłano: {message}")

                response = await ws.receive()
                if response.type == aiohttp.WSMsgType.TEXT:
                    print(f"Otrzymano: {response.data}")

                await asyncio.sleep(1)

            await ws.close()
            print("Połączenie zamknięte")


if __name__ == "__main__":
    asyncio.run(websocket_client())
```

## 9. Broadcast do wielu klientów

Broadcast oznacza wysłanie tej samej wiadomości do wielu podłączonych klientów.

Podstawowy pomysł:

1. Trzymamy aktywne połączenia w zbiorze `set`.
2. Gdy klient się połączy, dodajemy jego `ws` do zbioru.
3. Gdy klient wysyła wiadomość, iterujemy po zbiorze i wysyłamy wiadomość do każdego.
4. Gdy klient się rozłącza, usuwamy jego `ws` ze zbioru.

Przykład:

```python
from aiohttp import web

active_connections: set[web.WebSocketResponse] = set()


async def broadcast_message(message: str, sender: web.WebSocketResponse | None = None):
    for connection in active_connections:
        if connection != sender and not connection.closed:
            try:
                await connection.send_str(message)
            except Exception as error:
                print(f"Błąd wysyłania do klienta: {error}")


async def chat_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    active_connections.add(ws)
    print(f"Nowy klient. Aktywne połączenia: {len(active_connections)}")

    await broadcast_message(
        f"Nowy użytkownik dołączył. Aktywnych: {len(active_connections)}",
        sender=ws,
    )

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                await broadcast_message(f"Użytkownik: {msg.data}")
            elif msg.type == web.WSMsgType.ERROR:
                print(f"Błąd WebSocket: {ws.exception()}")
    finally:
        active_connections.discard(ws)
        print(f"Klient rozłączony. Zostało: {len(active_connections)}")
        await broadcast_message(
            f"Użytkownik opuścił chat. Aktywnych: {len(active_connections)}"
        )

    return ws


app = web.Application()
app.router.add_get("/chat", chat_handler)

if __name__ == "__main__":
    print("Chat server działa na ws://localhost:8080/chat")
    web.run_app(app, host="localhost", port=8080)
```

Ważne: używaj `try/finally`, żeby usuwać rozłączonych klientów ze zbioru. Bez tego możesz zostawić w pamięci nieaktywne połączenia.

## 10. Typy wiadomości WebSocket

W `aiohttp` najczęściej spotkasz:

- `TEXT` - wiadomość tekstowa,
- `BINARY` - dane binarne, na przykład plik albo obraz,
- `CLOSE` - zamknięcie połączenia,
- `ERROR` - błąd połączenia.

Przykład obsługi kilku typów:

```python
from aiohttp import web


async def advanced_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            await ws.send_str(f"Otrzymałem tekst: {msg.data}")
        elif msg.type == web.WSMsgType.BINARY:
            await ws.send_bytes(msg.data)
        elif msg.type == web.WSMsgType.CLOSE:
            print("Klient zamyka połączenie")
            break
        elif msg.type == web.WSMsgType.ERROR:
            print(f"Błąd: {ws.exception()}")

    return ws
```

Najczęściej w aplikacjach wysyła się JSON jako tekst. `aiohttp` ma do tego wygodne metody:

```python
await ws.send_json({"type": "message", "text": "Cześć"})
data = await ws.receive_json()
```

## 11. GraphQL

GraphQL to alternatywne podejście do projektowania API.

W REST zwykle masz wiele endpointów:

```text
GET /api/users/123
GET /api/users/123/posts
GET /api/posts/1/comments
```

W GraphQL najczęściej masz jeden endpoint:

```text
POST /graphql
```

To klient w treści zapytania mówi, jakie dane chce otrzymać.

### Definicja

**GraphQL** to język zapytań do API, który pozwala klientowi precyzyjnie określić strukturę odpowiedzi. W przeciwieństwie do REST endpoint nie musi zwracać zawsze tego samego zestawu pól.

## 12. Problemy REST, które rozwiązuje GraphQL

GraphQL często pomaga przy dwóch problemach REST API.

### Over-fetching

Over-fetching oznacza, że API zwraca więcej danych niż potrzebujesz.

Przykład: chcesz tylko `name`, `email` i tytuły postów, ale endpoint użytkownika zwraca też adres, telefon, datę utworzenia konta i wiele innych pól.

### Under-fetching

Under-fetching oznacza, że jeden endpoint zwraca za mało danych i musisz wykonać kilka requestów.

Przykład: najpierw pobierasz użytkownika, potem jego posty, potem komentarze do postów.

## 13. REST vs GraphQL

Przykład REST:

```python
# Request 1:
# GET /api/users/123
user_response = {
    "id": 123,
    "name": "Jan Kowalski",
    "email": "jan@example.com",
    "age": 30,
    "address": "ul. Główna 1",
    "phone": "+48 123 456 789",
    "created_at": "2020-01-01",
}

# Request 2:
# GET /api/users/123/posts
posts_response = {
    "posts": [
        {
            "id": 1,
            "title": "Mój pierwszy post",
            "content": "...",
            "author_id": 123,
            "created_at": "2024-01-01",
            "likes": 15,
        }
    ]
}
```

Przykład GraphQL:

```graphql
query {
  user(id: 123) {
    name
    email
    posts {
      title
    }
  }
}
```

Przykładowa odpowiedź:

```json
{
  "data": {
    "user": {
      "name": "Jan Kowalski",
      "email": "jan@example.com",
      "posts": [
        {
          "title": "Mój pierwszy post"
        }
      ]
    }
  }
}
```

GraphQL pozwala pobrać dokładnie te pola, o które prosisz.

## 14. Podstawowe elementy GraphQL

GraphQL składa się z kilku głównych elementów.

### Schema

Schema opisuje typy danych oraz dostępne operacje.

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
  posts: [Post]
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User
}
```

Znak `!` oznacza, że pole jest wymagane i nie powinno zwracać `null`.

### Query

Query służy do pobierania danych. Jest odpowiednikiem operacji typu `GET` w REST.

```graphql
type Query {
  user(id: ID!): User
  users: [User]
  post(id: ID!): Post
}
```

Przykład:

```graphql
query {
  users {
    name
    email
  }
}
```

### Mutation

Mutation służy do modyfikacji danych. Jest odpowiednikiem operacji takich jak `POST`, `PUT`, `PATCH` albo `DELETE` w REST.

```graphql
type Mutation {
  createUser(name: String!, email: String!): User
  createPost(title: String!, content: String!, authorId: ID!): Post
}
```

Przykład:

```graphql
mutation {
  createUser(name: "Anna Nowak", email: "anna@example.com") {
    id
    name
    email
  }
}
```

## 15. GraphQL w Pythonie ze Strawberry

`Strawberry` to biblioteka do budowania GraphQL API w Pythonie. Korzysta z type hints i klas Pythona.

Instalacja:

```bash
pip install "strawberry-graphql[aiohttp]"
```

Przykładowe API:

```python
from typing import Optional

import strawberry
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView


@strawberry.type
class Post:
    id: int
    title: str
    content: str
    author_id: int


@strawberry.type
class User:
    id: int
    name: str
    email: str

    @strawberry.field
    def posts(self) -> list[Post]:
        return [
            post
            for post in fake_posts_db
            if post.author_id == self.id
        ]


fake_users_db = [
    User(id=1, name="Jan Kowalski", email="jan@example.com"),
    User(id=2, name="Anna Nowak", email="anna@example.com"),
]

fake_posts_db = [
    Post(id=1, title="Python jest super", content="...", author_id=1),
    Post(id=2, title="GraphQL tutorial", content="...", author_id=1),
    Post(id=3, title="Asynchroniczność", content="...", author_id=2),
]


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        for user in fake_users_db:
            if user.id == id:
                return user
        return None

    @strawberry.field
    def users(self) -> list[User]:
        return fake_users_db

    @strawberry.field
    def post(self, id: int) -> Optional[Post]:
        for post in fake_posts_db:
            if post.id == id:
                return post
        return None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, email: str) -> User:
        new_id = max(user.id for user in fake_users_db) + 1
        new_user = User(id=new_id, name=name, email=email)
        fake_users_db.append(new_user)
        return new_user


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = web.Application()
app.router.add_route("*", "/graphql", GraphQLView(schema=schema, graphiql=True))

if __name__ == "__main__":
    print("GraphQL API działa na http://localhost:8000/graphql")
    web.run_app(app, host="localhost", port=8000)
```

Po uruchomieniu aplikacji możesz wejść na:

```text
http://localhost:8000/graphql
```

GraphiQL pozwoli pisać i testować zapytania w przeglądarce.

## 16. Przykładowe zapytania GraphQL

Pobranie użytkownika z postami:

```graphql
query {
  user(id: 1) {
    name
    email
    posts {
      title
    }
  }
}
```

Utworzenie użytkownika:

```graphql
mutation {
  createUser(name: "Piotr Wiśniewski", email: "piotr@example.com") {
    id
    name
    email
  }
}
```

## 17. Kiedy używać GraphQL

GraphQL jest dobrym wyborem, gdy:

- masz złożone relacje między danymi,
- różni klienci potrzebują różnych struktur danych,
- REST wymaga wielu requestów do jednego widoku,
- chcesz, aby klient wybierał pola w odpowiedzi,
- pracujesz z aplikacją webową i mobilną korzystającą z tego samego API.

REST jest często lepszy, gdy:

- API jest proste,
- wykonujesz klasyczne operacje CRUD,
- zależy Ci na prostym HTTP cache,
- chcesz łatwiejszego debugowania requestów,
- zespół dobrze zna REST i nie ma realnego problemu over-fetchingu albo under-fetchingu.

GraphQL nie jest "lepszym REST-em". To inne narzędzie do innych problemów.

## 18. WebSocket + GraphQL + AI

WebSockety i GraphQL można łączyć z AI.

Przykłady:

- chatbot odpowiadający w czasie rzeczywistym przez WebSocket,
- GraphQL query generujące tekst na podstawie tematu,
- system powiadomień, w którym AI analizuje dane i wysyła alerty live,
- aplikacja, w której GraphQL pobiera historię rozmowy, a WebSocket przesyła nowe wiadomości.

Przykładowy szkic handlera WebSocket dla chatbota:

```python
import os

import aiohttp
from aiohttp import web


async def ai_chat_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async with aiohttp.ClientSession() as session:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                user_message = msg.data

                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                    },
                    json={
                        "model": "gpt-4",
                        "messages": [
                            {"role": "user", "content": user_message},
                        ],
                    },
                ) as response:
                    data = await response.json()
                    ai_reply = data["choices"][0]["message"]["content"]
                    await ws.send_str(ai_reply)

    return ws
```

Ten przykład pokazuje ideę architektury, ale w prawdziwej aplikacji trzeba dodać obsługę błędów, limity, autoryzację, walidację danych i bezpieczną konfigurację kluczy API.

## 19. Najczęstsze pułapki

- Używanie WebSocketów tam, gdzie wystarczy zwykły request HTTP.
- Brak obsługi rozłączenia klienta i zostawianie starych połączeń w pamięci.
- Trzymanie aktywnych WebSocketów w zwykłym globalnym zbiorze bez myślenia o skalowaniu na wiele procesów.
- Wysyłanie nieustrukturyzowanych stringów zamiast JSON-a z polem `type`.
- Brak walidacji danych przychodzących przez WebSocket.
- Traktowanie GraphQL jako obowiązkowego zamiennika REST.
- Tworzenie GraphQL API bez limitów głębokości zapytań.
- Problem N+1 queries przy zagnieżdżonych polach w GraphQL.
- Brak autoryzacji na resolverach GraphQL.

## 20. Do zapamiętania

- WebSocket daje stałe, dwukierunkowe połączenie klient-serwer.
- HTTP jest dobre do prostych requestów, CRUD i wyszukiwania.
- WebSocket jest dobry do real-time: czatów, gier, dashboardów i powiadomień.
- `aiohttp` pozwala pisać asynchroniczne serwery i klientów WebSocket.
- Broadcast wymaga przechowywania aktywnych połączeń i sprzątania ich po rozłączeniu.
- GraphQL pozwala klientowi wybrać dokładnie potrzebne pola.
- GraphQL ma schema, queries i mutations.
- Strawberry pozwala pisać GraphQL API w Pythonie z użyciem type hints.
- REST i GraphQL rozwiązują różne problemy. Wybór powinien wynikać z potrzeb aplikacji, nie z mody.
