# Lesson 34 - Zadania

## TASK 01 - Prosty echo server

Stwórz prosty serwer WebSocket, który zwraca każdą otrzymaną wiadomość z prefiksem:

```text
Server:
```

Przykład:

```text
Klient wysyła: Cześć
Serwer odpowiada: Server: Cześć
```

## TASK 02 - Klient wysyłający 3 wiadomości

Napisz klienta WebSocket, który łączy się z serwerem i wysyła trzy wiadomości:

- `Cześć`
- `Jak się masz?`
- `Do widzenia`

Po każdej wiadomości klient powinien odebrać i wypisać odpowiedź serwera.

## TASK 03 - Licznik połączeń

Zmodyfikuj echo server tak, aby przy każdym nowym połączeniu wysyłał klientowi wiadomość:

```text
Jesteś klientem numer X
```

`X` ma oznaczać aktualną liczbę aktywnych połączeń.

## TASK 04 - GraphQL: query użytkownika

Stwórz proste GraphQL API z typem `User`, który ma pola:

- `id`
- `name`
- `email`

Dodaj query:

```graphql
user(id: ID!): User
```

Query powinno zwracać użytkownika z fake listy.

## TASK 05 - GraphQL: lista użytkowników

Rozszerz API z zadania 4 o query:

```graphql
users: [User]
```

Query powinno zwracać listę wszystkich użytkowników.

## TASK 06 - GraphQL: mutation `createUser`

Dodaj mutację:

```graphql
createUser(name: String!, email: String!): User
```

Mutacja powinna:

- utworzyć nowego użytkownika,
- dodać go do fake listy,
- zwrócić utworzonego użytkownika.

## TASK 07 - WebSocket broadcast podstawowy

Stwórz serwer WebSocket, który rozsyła każdą otrzymaną wiadomość do wszystkich podłączonych klientów.

Wskazówka: przechowuj aktywne połączenia w zbiorze `set`.

## TASK 08 - Pomiar czasu połączenia

Zmodyfikuj WebSocket handler tak, aby mierzył czas połączenia każdego klienta.

Serwer powinien:

- zapisać czas połączenia klienta,
- po rozłączeniu obliczyć czas trwania połączenia,
- wypisać wynik w konsoli.

## TASK 09 - Chat z nickami

Stwórz chat room, w którym pierwsza wiadomość od klienta jest jego nickiem.

Kolejne wiadomości mają być broadcastowane w formacie:

```text
Nick: wiadomość
```

## TASK 10 - GraphQL z relacjami

Stwórz GraphQL API z typami:

- `User`
- `Post`

Wymagania:

- `User` ma pole `posts`, które zwraca listę jego postów,
- `Post` ma pole `author`, które zwraca autora posta.

Użyj fake list jako bazy danych.

## TASK 11 - WebSocket ping-pong

Zaimplementuj mechanizm ping-pong.

Wymagania:

- serwer co 30 sekund wysyła do klienta wiadomość `ping`,
- klient musi odpowiedzieć wiadomością `pong`,
- jeśli serwer nie dostanie `pong` przez 60 sekund, rozłącza klienta.

## TASK 12 - GraphQL z filtrowaniem

Rozszerz API z zadania 10 o query:

```graphql
posts(authorId: ID): [Post]
searchUsers(name: String): [User]
```

Wymagania:

- `posts(authorId: ID)` filtruje posty po autorze,
- `searchUsers(name: String)` wyszukuje użytkowników po fragmencie imienia albo nazwy.

## TASK 13 - Pokój chatowy z pokojami

Stwórz system chat rooms.

Klient powinien móc dołączyć do pokoju komendą:

```text
/join pokoj1
```

Wiadomości mają być broadcastowane tylko do klientów znajdujących się w tym samym pokoju.

## TASK 14 - WebSocket z autentykacją

Zaimplementuj autentykację połączenia WebSocket przez token.

Wymagania:

- klient wysyła token JWT w pierwszej wiadomości,
- serwer weryfikuje token,
- jeśli token jest poprawny, serwer pozwala wysyłać kolejne wiadomości,
- jeśli token jest błędny, serwer zamyka połączenie.

## TASK 15 - GraphQL subscription

Zaimplementuj GraphQL subscription, która emituje event, gdy nowy użytkownik się zarejestruje.

Wskazówki:

- użyj `strawberry.subscription`,
- użyj `AsyncGenerator`,
- przetestuj działanie w GraphiQL albo innym kliencie GraphQL.

## TASK 16 - Chat z historią

Rozszerz chat server o zapisywanie historii wiadomości do bazy danych SQLite.

Wymagania:

- zapisuj nick, treść wiadomości i czas wysłania,
- przy połączeniu nowego klienta wyślij mu ostatnie 50 wiadomości,
- nowe wiadomości nadal mają być broadcastowane do aktywnych klientów.

## TASK 17 - GraphQL DataLoader

Zaimplementuj DataLoader pattern w GraphQL, aby ograniczyć problem N+1 queries przy pobieraniu użytkowników i ich postów.

Wskazówka:

```python
strawberry.dataloader
```

Przetestuj, ile razy wykonywane jest pobieranie danych przed dodaniem DataLoadera i po jego dodaniu.

## TASK 18 - Real-time notifications

Stwórz system powiadomień w czasie rzeczywistym.

Aplikacja powinna mieć:

- REST API do tworzenia powiadomień,
- WebSocket endpoint wysyłający powiadomienia do zalogowanych użytkowników,
- prosty mechanizm sprawdzania, który użytkownik powinien dostać daną wiadomość.

## TASK 19 - GraphQL + WebSocket chat

Połącz GraphQL i WebSocket w jednym projekcie.

Wymagania:

- GraphQL służy do pobierania historii chatu,
- GraphQL służy do pobierania profili użytkowników,
- real-time wiadomości są obsługiwane przez WebSocket albo GraphQL subscriptions.

## TASK 20 - Multiplayer game server

Stwórz prosty serwer gry multiplayer, na przykład kółko i krzyżyk.

Wymagania:

- gracze łączą się przez WebSocket,
- serwer przechowuje stan gry,
- serwer waliduje ruchy,
- serwer rozsyła aktualny stan gry do graczy,
- gra obsługuje wygraną, remis i rozłączenie gracza.
