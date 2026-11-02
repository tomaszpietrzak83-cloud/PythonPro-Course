"""Reviewed learning goals and concrete previews, independent of source formatting."""


def pair(pl, en):
    return {"pl": pl, "en": en}


# title, mechanism, demonstration, expected result, question, answer (PL / ENG).
ROWS = [
    (
        ("Echo przez WebSocket", "WebSocket echo"),
        (
            "WebSocket utrzymuje jedno połączenie. Po handshake serwer i klient mogą wysyłać wiadomości bez kolejnych żądań HTTP.",
            "WebSocket maintains one connection. After the handshake both peers can send messages without further HTTP requests.",
        ),
        (
            "Klient połączy się z /ws, wyśle Hello i zaczeka na odpowiedź. Handler odczyta tekst, doda prefiks i odeśle go tym samym połączeniem.",
            "The client connects to /ws, sends Hello and awaits a reply. The handler reads the text, adds a prefix and sends it through the same connection.",
        ),
        (
            "Otrzymasz dokładnie Server: Hello. prepare() wykonuje handshake; send_str() wysyła wiadomość tekstową.",
            "You receive exactly Server: Hello. prepare() performs the handshake; send_str() sends a text message.",
        ),
        (
            "Co odróżnia prepare() od send_str()?",
            "How does prepare() differ from send_str()?",
        ),
        (
            "prepare() przełącza żądanie HTTP na WebSocket. send_str() działa już na otwartym połączeniu i wysyła tekst.",
            "prepare() upgrades the HTTP request to WebSocket. send_str() sends text through the open connection.",
        ),
    ),
    (
        ("Klient: trzy wiadomości", "Client: three messages"),
        (
            "Klient i serwer wykonują różne role. await oddaje sterowanie pętli zdarzeń, gdy czekamy na dane.",
            "Client and server have different roles. await yields control to the event loop while waiting for data.",
        ),
        (
            "Serwer wystartuje lokalnie. Osobny plik client.py kolejno wyśle Hello, How are you? i Goodbye. Po każdym send odbierze jedną odpowiedź.",
            "A local server starts. The separate client.py sends Hello, How are you? and Goodbye, receiving one reply after each send.",
        ),
        (
            "Zobaczysz trzy odpowiedzi z prefiksem Server: w kolejności wysyłania. async with zamknie sesję i połączenie.",
            "You see three Server: replies in send order. async with closes the session and connection.",
        ),
        ("Dlaczego receive jest wewnątrz pętli?", "Why is receive inside the loop?"),
        (
            "Każda wysłana wiadomość ma własną odpowiedź. Odczyt w tej samej iteracji daje prostą parę pytanie–odpowiedź.",
            "Each sent message has its own reply. Reading in the same iteration creates a simple request–reply pair.",
        ),
    ),
    (
        ("Aktywne połączenia", "Active connections"),
        (
            "Zbiór przechowuje aktywne gniazda. To liczba połączonych klientów, a nie kolejny numer nadawany na zawsze.",
            "A set stores active sockets. Its size counts current clients, rather than assigning permanent sequence numbers.",
        ),
        (
            "Połączymy dwóch klientów. Handler doda każde połączenie do zbioru przed wysłaniem powitania, a w finally usunie rozłączone gniazdo.",
            "Two clients connect. Each handler adds its socket before greeting and removes the disconnected socket in finally.",
        ),
        (
            "Pierwszy klient zobaczy 1, drugi 2. Po zamknięciu obu zbiór ma być pusty.",
            "The first client sees 1, the second sees 2. After both close the set must be empty.",
        ),
        ("Dlaczego usunięcie jest w finally?", "Why remove the socket in finally?"),
        (
            "finally wykona sprzątanie także przy błędzie lub anulowaniu, więc licznik nie powinien zawierać martwych połączeń.",
            "finally runs cleanup on failure or cancellation too, keeping dead sockets out of the count.",
        ),
    ),
    (
        ("GraphQL: jeden użytkownik", "GraphQL: one user"),
        (
            "Schemat opisuje dostępne typy i pola. Klient sam wybiera pola odpowiedzi; resolver dostarcza ich wartości.",
            "The schema defines available types and fields. Clients choose response fields; resolvers supply values.",
        ),
        (
            "Wyślemy query user z ID 1 i poprosimy o id, name, email. Drugie query sprawdzi nieistniejące ID 99.",
            "We query user ID 1 for id, name and email, then query the missing ID 99.",
        ),
        (
            "Pierwszy wynik zawiera Annę. Drugie pole user ma wartość null, bo zwracany typ dopuszcza None.",
            "The first result contains Anna. The second user field is null because the return type permits None.",
        ),
        (
            "Skąd GraphQL wie, jakie pola istnieją?",
            "How does GraphQL know which fields exist?",
        ),
        (
            "Strawberry buduje schemat z dekoratorów i adnotacji typów klas User oraz Query.",
            "Strawberry builds the schema from decorators and type annotations on User and Query.",
        ),
    ),
    (
        ("GraphQL: lista użytkowników", "GraphQL: user list"),
        (
            "Resolver może zwracać listę obiektów. Dla każdego elementu GraphQL wybiera tylko pola zapisane w query.",
            "A resolver can return a list of objects. GraphQL selects requested fields for each element.",
        ),
        (
            "Wyślemy users { id name }. Resolver zwróci fake listę, a GraphQL zbuduje odpowiedź dla dwóch użytkowników.",
            "We send users { id name }. The resolver returns the fake list and GraphQL builds a response for two users.",
        ),
        (
            "Zobaczysz Annę i Jana. Brak email w query oznacza brak email w odpowiedzi.",
            "You see Anna and Jan. No email in the query means no email in the response.",
        ),
        (
            "Czy users musi zwrócić wszystkie pola User?",
            "Must users return all User fields?",
        ),
        (
            "Resolver zwraca obiekty User, ale odpowiedź zawiera tylko pola wybrane przez klienta.",
            "The resolver returns User objects, while the response contains only client-selected fields.",
        ),
    ),
    (
        ("Mutacja createUser", "createUser mutation"),
        (
            "Query czyta dane, a mutation jest przeznaczona do ich zmiany. Lista w pamięci znika po zakończeniu procesu.",
            "Query reads data; mutation is intended to change it. The in-memory list disappears when the process ends.",
        ),
        (
            "Mutacja utworzy Alexa, wyliczy nowe ID i dopisze obiekt do listy. Następne query users sprawdzi, czy wpis rzeczywiście powstał.",
            "A mutation creates Alex, calculates a new ID and appends the object. A subsequent users query verifies the change.",
        ),
        (
            "createUser zwróci ID 3, a users będzie zawierało trzy osoby. create_user w Pythonie staje się createUser w GraphQL.",
            "createUser returns ID 3 and users contains three people. Python create_user becomes GraphQL createUser.",
        ),
        ("Dlaczego odczytujemy listę po mutacji?", "Why read the list after mutation?"),
        (
            "Sama odpowiedź mutacji nie dowodzi zapisu. Osobne query sprawdza widoczny efekt zmiany.",
            "The mutation response alone does not prove storage. A separate query verifies the visible change.",
        ),
    ),
    (
        ("Broadcast do wszystkich", "Broadcast to everyone"),
        (
            "Broadcast to wysłanie jednej wiadomości do wielu połączeń. Serwer musi pamiętać aktywnych odbiorców.",
            "Broadcast sends one message to many connections. The server must track active recipients.",
        ),
        (
            "Dwóch klientów otrzyma Ready. Pierwszy wyśle wiadomość; funkcja broadcast przejdzie po kopii zbioru i wyśle tekst każdemu.",
            "Two clients receive Ready. The first sends a message; broadcast iterates a snapshot of the set and sends text to each socket.",
        ),
        (
            "Tę samą wiadomość otrzymają obaj klienci, również nadawca. Po rozłączeniu zbiór jest czyszczony.",
            "Both clients receive the same message, including the sender. Disconnections remove sockets from the set.",
        ),
        (
            "Dlaczego iterujemy po tuple(connections)?",
            "Why iterate tuple(connections)?",
        ),
        (
            "To migawka zbioru. Usuwanie martwego połączenia w trakcie rozsyłania nie zmienia kolekcji, po której akurat iterujemy.",
            "It snapshots the set. Removing a dead connection during broadcast does not mutate the iterated collection.",
        ),
    ),
    (
        ("Czas połączenia", "Connection duration"),
        (
            "perf_counter mierzy upływ czasu. Różnica dwóch odczytów nadaje się do pomiaru trwania operacji.",
            "perf_counter measures elapsed time. Subtracting readings measures operation duration.",
        ),
        (
            "Klient wykona echo i się rozłączy. Handler zapamięta początek, a w finally obliczy oraz wypisze czas połączenia.",
            "The client performs an echo and disconnects. The handler records the start and computes and prints duration in finally.",
        ),
        (
            "Zobaczysz dodatni czas w sekundach. Obejmuje również oczekiwanie na klienta, nie tylko pracę procesora.",
            "You see a positive duration in seconds. It includes waiting for the client, not only CPU work.",
        ),
        ("Czy ten wynik to zużycie CPU?", "Is this CPU usage?"),
        (
            "Nie. To czas rzeczywisty między startem i końcem obsługi połączenia, łącznie z czekaniem.",
            "No. It is elapsed wall time from handler start to finish, including waiting.",
        ),
    ),
    (
        ("Chat z nickami", "Chat with nicknames"),
        (
            "Protokół aplikacji nadaje znaczenie wiadomościom. Tutaj pierwszy tekst oznacza nick, kolejne oznaczają treść.",
            "An application protocol gives messages meaning. Here the first text is a nickname; later texts are chat content.",
        ),
        (
            "Anna i Jan podadzą nicki i odbiorą Ready. Anna wyśle Hello; serwer zbuduje Anna: Hello i rozgłosi wiadomość.",
            "Anna and Jan send nicknames and receive Ready. Anna sends Hello; the server constructs Anna: Hello and broadcasts it.",
        ),
        (
            "Obaj zobaczą Anna: Hello. Nick ma osobny odczyt przed pętlą wiadomości i limit czasu podania.",
            "Both see Anna: Hello. The nickname is read separately before the message loop, with a timeout.",
        ),
        (
            "Dlaczego nick nie trafia do zwykłego broadcastu?",
            "Why is the nickname not a regular broadcast?",
        ),
        (
            "Pierwszy receive_str konsumuje go przed wejściem do async for, więc pętla widzi dopiero kolejne wiadomości.",
            "The initial receive_str consumes it before async for, so the loop sees subsequent messages only.",
        ),
    ),
    (
        ("GraphQL: relacje User–Post", "GraphQL: User–Post relations"),
        (
            "Zagnieżdżone resolvery łączą obiekty przez identyfikatory. Relacja nie wymaga bazy SQL w tym przykładzie.",
            "Nested resolvers connect objects by IDs. This example does not require a SQL database.",
        ),
        (
            "Query pobierze users, ich posts i author każdego posta. User.posts filtruje po ID użytkownika, Post.author znajduje właściwą osobę.",
            "The query fetches users, their posts and each post author. User.posts filters by user ID; Post.author finds the matching person.",
        ),
        (
            "Anna ma Python i GraphQL, Jan ma Async. Pole author_id jest prywatne w schemacie, ale służy do łączenia danych.",
            "Anna has Python and GraphQL; Jan has Async. author_id is private in the schema but connects the data.",
        ),
        ("Po co Post przechowuje author_id?", "Why does Post store author_id?"),
        (
            "To klucz powiązania z User.id. Resolver author używa go do znalezienia autora.",
            "It connects to User.id. The author resolver uses it to find the author.",
        ),
    ),
    (
        ("Heartbeat ping–pong", "Ping–pong heartbeat"),
        (
            "Osobna korutyna wysyła tekst ping. Odbiór pong odświeża zegar ostatniej odpowiedzi i pozwala wykryć milczącego klienta.",
            "A separate coroutine sends text ping. Receiving pong refreshes the last-response clock and detects silent clients.",
        ),
        (
            "Pierwszy klient odpowie pong na trzy ping. Drugi będzie milczeć i zostanie zamknięty. Pokaz skraca odstępy do 0,05 / 0,15 s.",
            "One client replies pong to three pings. A silent client is closed. The demo accelerates intervals to 0.05 / 0.15 seconds.",
        ),
        (
            "Kod domyślnie używa 30 / 60 sekund. Milczący klient otrzyma zamknięcie 1001. Task heartbeat jest anulowany przy sprzątaniu.",
            "Code defaults to 30 / 60 seconds. The silent client receives close code 1001. Cleanup cancels the heartbeat task.",
        ),
        (
            "Dlaczego heartbeat działa w osobnym Task?",
            "Why run heartbeat in a separate Task?",
        ),
        (
            "Wysyłanie okresowe musi działać równolegle z pętlą odbierania pong. Samo oczekiwanie na wiadomość blokowałoby wysyłanie ping.",
            "Periodic sending must run alongside the pong receive loop. Waiting only for incoming messages would prevent ping sends.",
        ),
    ),
    (
        ("Filtrowanie w GraphQL", "GraphQL filtering"),
        (
            "Argumenty pól trafiają do resolvera. None oznacza brak filtra; casefold pozwala porównywać tekst bez rozróżniania wielkości liter.",
            "Field arguments reach the resolver. None means no filter; casefold enables case-insensitive text comparison.",
        ),
        (
            "Zapytamy o posts autora 2 oraz searchUsers z fragmentem AN. Filtry przejdą po fake listach.",
            "We query posts by author 2 and searchUsers containing AN. Filters scan the fake lists.",
        ),
        (
            "Posty: Async. Użytkownicy: Anna i Jan. GraphQL authorId jest argumentem author_id w Pythonie.",
            "Posts: Async. Users: Anna and Jan. GraphQL authorId maps to Python author_id.",
        ),
        ("Co zwróci posts bez authorId?", "What does posts return without authorId?"),
        (
            "Wszystkie posty: warunek author_id is None przepuszcza każdy element.",
            "All posts: author_id is None allows every element.",
        ),
    ),
    (
        ("Osobne pokoje chatu", "Separate chat rooms"),
        (
            "Słownik mapuje nazwę pokoju na zbiór połączeń. Broadcast wybiera tylko zbiór bieżącego pokoju.",
            "A dictionary maps room names to socket sets. Broadcast selects only the current room.",
        ),
        (
            "Klienci wejdą do one i two. Wiadomość z one nie dotrze do two. Potem drugi klient zmieni pokój na one i odbierze wspólny tekst.",
            "Clients join one and two. A message in one never reaches two. Then the second client joins one and receives a shared message.",
        ),
        (
            "Sprawdzimy brak wycieku między pokojami oraz odbiór po zmianie pokoju. Rozłączenie usuwa klienta i puste pokoje.",
            "We verify isolation and delivery after switching rooms. Disconnect cleanup removes clients and empty rooms.",
        ),
        (
            "Co trzeba zrobić przy zmianie pokoju?",
            "What must happen when changing rooms?",
        ),
        (
            "Usunąć gniazdo z poprzedniego zbioru, zapamiętać nową nazwę i dopisać gniazdo do nowego zbioru.",
            "Remove the socket from its previous set, store the new room name and add it to the new set.",
        ),
    ),
    (
        ("WebSocket i JWT", "WebSocket and JWT"),
        (
            "Podpis JWT potwierdza integralność tokenu. exp ogranicza jego ważność, sub wskazuje użytkownika; serwer dopuszcza wyłącznie HS256.",
            "A JWT signature verifies token integrity. exp limits validity; sub identifies the user. The server allows only HS256.",
        ),
        (
            "Wyślemy w pierwszej wiadomości poprawny token, uszkodzony tekst i token wygasły. Tylko poprawna sesja przejdzie do obsługi chatu.",
            "The first messages contain a valid token, broken text and an expired token. Only the valid session reaches chat handling.",
        ),
        (
            "Poprawny klient dostanie authenticated i echo. Błędne tokeny kończą połączenie kodem 1008. Klucz w kodzie jest wyłącznie demonstracyjny.",
            "The valid client receives authenticated and echo. Invalid tokens close with code 1008. The source key is for demonstrations only.",
        ),
        (
            "Dlaczego nie wystarczy odczytać sub bez weryfikacji?",
            "Why not just read sub without verification?",
        ),
        (
            "Bez sprawdzenia podpisu klient mógłby podmienić tożsamość. decode sprawdza podpis, algorytm, wymagane pola i termin ważności.",
            "Without signature verification a client could replace its identity. decode checks signature, algorithm, required claims and expiry.",
        ),
    ),
    (
        ("GraphQL subscription", "GraphQL subscription"),
        (
            "Subscription utrzymuje strumień wyników. AsyncGenerator czeka na kolejkę i emituje wartość po nowym zdarzeniu.",
            "A subscription keeps a result stream open. An AsyncGenerator awaits a queue and yields a value for each new event.",
        ),
        (
            "Klient uruchomi subscription po protokole graphql-transport-ws. Dopiero po jej gotowości mutacja utworzy Alexa i wstawi go do kolejek subskrybentów.",
            "The client starts a graphql-transport-ws subscription. Once it is ready, a mutation creates Alex and puts him into subscriber queues.",
        ),
        (
            "Po connection_ack dostaniesz next z userRegistered = Alex. Zakończenie subskrypcji usuwa jej kolejkę ze zbioru.",
            "After connection_ack you receive next with userRegistered = Alex. Completing the subscription removes its queue from the set.",
        ),
        (
            "Dlaczego czekamy na gotowość subskrypcji?",
            "Why wait for subscription readiness?",
        ),
        (
            "Zdarzenia nie są tu odtwarzane. Mutacja wykonana przed dodaniem kolejki do subscribers mogłaby zostać pominięta.",
            "Events are not replayed here. A mutation before the queue joins subscribers could be missed.",
        ),
    ),
    (
        ("Chat i historia SQLite", "Chat and SQLite history"),
        (
            "SQLite przechowuje historię, a WebSocket rozsyła nowe wpisy. Parametry SQL oddzielają dane wiadomości od składni zapytania.",
            "SQLite stores history while WebSocket distributes new messages. SQL parameters separate message data from query syntax.",
        ),
        (
            "Anna połączy się z pustą historią i zapisze wiadomość. Jan dołączy później i otrzyma ostatnie wpisy z SQLite. Zapis i odczyt chroni wspólny lock.",
            "Anna connects to empty history and saves a message. Jan joins later and receives recent SQLite rows. A shared lock protects writes and reads.",
        ),
        (
            "Zapisany wpis zawiera nick, body i czas UTC. SELECT pobiera 50 najnowszych, a reversed ustawia je od najstarszego. Każdy pokaz ma własny plik bazy.",
            "The saved row contains nickname, body and UTC time. SELECT fetches the newest 50; reversed puts them oldest first. Each demo has its own database file.",
        ),
        (
            "Dlaczego po ORDER BY id DESC potrzebne jest reversed?",
            "Why use reversed after ORDER BY id DESC?",
        ),
        (
            "DESC wybiera najnowsze 50; odwrócenie prezentuje ten wycinek w naturalnej kolejności chronologicznej.",
            "DESC selects the newest 50; reversing presents that window in chronological order.",
        ),
    ),
    (
        ("DataLoader: mniej pobrań", "DataLoader: fewer fetches"),
        (
            "N+1 powstaje, gdy osobno pobieramy dane dla każdego rodzica. DataLoader zbiera klucze w paczkę i zachowuje kolejność wyników.",
            "N+1 arises when child data is fetched separately for every parent. DataLoader batches keys and preserves result order.",
        ),
        (
            "Porównamy users.naivePosts i users.posts dla trzech użytkowników. Przed każdym query wyzerujemy licznik pobrań.",
            "We compare users.naivePosts and users.posts for three users, resetting the fetch counter before each query.",
        ),
        (
            "Wariant naiwny wykona 3 pobrania postów, DataLoader 1 paczkę. To licznik fake odczytów postów, nie rzeczywistych zapytań SQL. Loader jest nowy dla każdego żądania.",
            "The naive version fetches posts 3 times; DataLoader uses 1 batch. This counts fake post reads, not actual SQL queries. Each request gets a new loader.",
        ),
        (
            "Dlaczego wynik load_posts jest listą list?",
            "Why does load_posts return a list of lists?",
        ),
        (
            "Każdy klucz użytkownika ma własną listę postów. Wynik na pozycji i musi odpowiadać kluczowi keys[i], także gdy ta lista jest pusta.",
            "Each user key has its own post list. Result i must match keys[i], including users with no posts.",
        ),
    ),
    (
        ("Powiadomienia REST → WebSocket", "REST → WebSocket notifications"),
        (
            "REST tworzy powiadomienie, WebSocket dostarcza je odbiorcy. JWT przypisuje gniazdo do ID, a osobny token admin autoryzuje tworzenie.",
            "REST creates a notification; WebSocket delivers it. JWT maps sockets to IDs, while a separate admin token authorizes creation.",
        ),
        (
            "Zalogujemy użytkowników 1 i 2. Żądanie bez tokenu dostanie 401. Admin utworzy powiadomienie dla 1; sprawdzimy odbiór i ciszę u 2.",
            "Users 1 and 2 authenticate. A request without a token receives 401. Admin creates a notification for 1; we verify receipt and silence for 2.",
        ),
        (
            'REST zwróci 201 i sent_to = "1". Wiadomość otrzyma tylko użytkownik 1; ID odbiorcy nie jest wybierane przez jego wiadomości WS.',
            'REST returns 201 and sent_to = "1". Only user 1 receives the message; the recipient identity is not selected by WS chat messages.',
        ),
        ("Dlaczego indeksujemy połączenia po ID?", "Why index connections by ID?"),
        (
            "Możemy wybrać wszystkie sesje konkretnego odbiorcy, nie rozsyłając prywatnego powiadomienia innym użytkownikom.",
            "We can select all sessions of one recipient without exposing a private notification to others.",
        ),
    ),
    (
        ("Historia GraphQL + chat na żywo", "GraphQL history + live chat"),
        (
            "Dwa interfejsy używają wspólnego stanu. GraphQL czyta historię i profile, a WS dopisuje oraz rozsyła wiadomości na żywo.",
            "Two interfaces share state. GraphQL reads history and profiles; WS appends and broadcasts live messages.",
        ),
        (
            "Klient wyśle Live message po WS. Po odebraniu broadcastu query pobierze historię i profile, sprawdzając zapis tej samej wiadomości.",
            "A client sends Live message over WS. After receiving the broadcast a query fetches history and profiles, verifying the same message.",
        ),
        (
            "Tekst z WS znajdzie się też w history. Ten prosty pokaz używa nicku Guest i list w pamięci, bez trwałości i logowania.",
            "The WS text also appears in history. This simple demo uses Guest and in-memory lists, without persistence or login.",
        ),
        ("Co spina query i WebSocket?", "What connects the query and WebSocket?"),
        (
            "Oba czytają tę samą listę messages_db. Handler WS dopisuje obiekt Message, resolver history zwraca jej zawartość.",
            "Both access the same messages_db list. The WS handler appends Message objects; the history resolver returns them.",
        ),
    ),
    (
        ("Multiplayer: kółko i krzyżyk", "Multiplayer: tic-tac-toe"),
        (
            "Serwer jest właścicielem stanu gry. Klient proponuje numer pola, a serwer sprawdza turę, zakres, zajętość i zakończenie.",
            "The server owns game state. Clients propose a cell; the server validates turn, bounds, occupancy and completion.",
        ),
        (
            "Połączymy X i O, sprawdzimy odrzucenie ruchu poza turą i błędnego pola. Sekwencja 0,3,1,4,2 doprowadzi do wygranej X.",
            "X and O connect. We verify rejection of out-of-turn and invalid moves. Sequence 0,3,1,4,2 produces an X win.",
        ),
        (
            "Obaj gracze widzą identyczną planszę i winner:X. Komunikaty błędu trafiają tylko do autora ruchu. Nowy proces tworzy nową partię.",
            "Both players see the same board and winner:X. Errors go only to the player who proposed the move. A new process creates a new game.",
        ),
        (
            "Dlaczego type(cell) is int zamiast isinstance(cell, int)?",
            "Why type(cell) is int instead of isinstance(cell, int)?",
        ),
        (
            "bool jest podklasą int w Pythonie. Ścisłe porównanie odrzuca true jako numer pola; akceptujemy wyłącznie liczby całkowite 0–8.",
            "bool subclasses int in Python. The strict check rejects true as a cell; only integers 0–8 are accepted.",
        ),
    ),
]


def content(number):
    title, intro, forecast, takeaway, question, answer = [
        pair(*value) for value in ROWS[number - 1]
    ]
    return dict(
        number=number,
        title=title,
        intro=intro,
        forecast=forecast,
        takeaway=takeaway,
        question=question,
        answer=answer,
        watch=forecast,
        pipeline=pair(
            "Połączenie / query → handler / resolver → zmiana lub odczyt stanu → odpowiedź → weryfikacja wyniku",
            "Connection / query → handler / resolver → read or update state → response → verify result",
        ),
        caveat=pair(
            "Pokaz działa lokalnie w osobnym procesie. Fake listy są resetowane po każdym uruchomieniu; SQLite zapisuje do osobnego pliku w .runtime. To przykłady do nauki: pojedynczy proces, bez wielu workerów, limitowania ruchu i wdrożenia produkcyjnego.",
            "Each demo runs locally in its own process. Fake lists reset between runs; SQLite uses a separate .runtime file. These single-process learning examples omit multiple workers, rate limits and production deployment.",
        ),
        extra_question=pair(
            "Wskaż dane wejściowe, moment zmiany stanu i miejsce odesłania wyniku. Co się stanie po rozłączeniu?",
            "Point to input, state mutation and response. What happens after disconnection?",
        ),
        extra_answer=pair(
            "Prześledź handler lub resolver od góry. await to miejsce oczekiwania; append / add / INSERT zmienia stan; return / send / yield przekazuje wynik. W handlerach sprawdź finally, a w bazie cleanup_ctx.",
            "Trace the handler or resolver top to bottom. await waits; append / add / INSERT change state; return / send / yield deliver results. Inspect finally in handlers and cleanup_ctx for database resources.",
        ),
        adaptation=pair(
            "Pokaz automatycznie uruchamia lokalny serwer i klientów oraz sprawdza rzeczywiste odpowiedzi. Teksty demonstracji i identyfikatory są po angielsku. W zadaniu 11 tylko pokaz przyspiesza zegar; domyślny serwer zachowuje 30 / 60 s.",
            "The demo automatically runs a local server and clients and checks actual replies. Demo text and identifiers are English. Only the task 11 demo accelerates time; the default server retains 30 / 60 seconds.",
        ),
        presets=[dict(label="Scenariusz kontrolny / Verified scenario", value={})],
        terms=[],
    )
