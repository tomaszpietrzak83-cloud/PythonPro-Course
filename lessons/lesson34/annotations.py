"""AST-based ranges and reviewed explanations, rendered against the same source text.

No fixed line numbers: formatting changes cannot detach a note from its code.
The AST describes Python structure; the tables explain this lesson's operations.
"""

import ast
import html

from pygments import lex
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from course_content import pair


FUNCTIONS = {
    "create_app": (
        "Buduje aplikację aiohttp, tworzy jej stan i wiąże adresy URL z handlerami. Zwraca app; nie uruchamia jeszcze nasłuchiwania na porcie.",
        "Builds the aiohttp application, initializes state and binds URLs to handlers. Returns app without starting a listening port.",
    ),
    "echo": (
        "Obsługuje jedno połączenie WebSocket: wykonuje handshake, odbiera tekst w pętli i odsyła odpowiedzi. return ws kończy handler po zamknięciu połączenia.",
        "Handles one WebSocket connection: handshake, text receive loop and replies. return ws ends the handler after the connection closes.",
    ),
    "chat": (
        "Obsługuje jednego uczestnika chatu. Przygotowuje połączenie, interpretuje wiadomości i przekazuje je odbiorcom; finally sprząta stan tego klienta.",
        "Handles one chat participant: prepares the connection, interprets messages and delivers them to recipients. finally cleans up this client’s state.",
    ),
    "broadcast": (
        "Wysyła tekst do wszystkich gniazd w podanym zbiorze, także do nadawcy, jeśli jest w zbiorze. Kopia tuple pozwala bezpiecznie usuwać martwe gniazda.",
        "Sends text to every socket in the supplied set, including the sender when present. A tuple snapshot allows dead sockets to be removed safely.",
    ),
    "send_messages": (
        "Otwiera sesję klienta i połączenie WS. Wysyła trzy teksty, po każdym odbiera odpowiedź i zbiera wyniki. async with zamyka zasoby.",
        "Opens a client session and WS connection. Sends three texts, receives a reply after each and collects results. async with closes resources.",
    ),
    "authenticate": (
        "Czeka maksymalnie 5 sekund na pierwszą wiadomość z JWT. Sprawdza podpis HS256, exp i sub oraz znane ID. Zwraca ID albo zamyka WS kodem 1008.",
        "Waits up to 5 seconds for the initial JWT. Checks HS256 signature, exp, sub and known ID. Returns the ID or closes WS with code 1008.",
    ),
    "heartbeat": (
        "Działa równolegle z odbieraniem wiadomości. Po każdym sleep sprawdza czas od ostatniego pong; zamyka milczące połączenie albo wysyła tekst ping.",
        "Runs alongside message receiving. After each sleep checks time since the last pong, closing a silent connection or sending text ping.",
    ),
    "user": (
        "Szuka użytkownika o ID podanym w query. next(..., None) zwraca pierwszy pasujący obiekt albo None, które GraphQL zapisze jako null.",
        "Finds the user requested by ID. next(..., None) returns the first matching object or None, serialized by GraphQL as null.",
    ),
    "users": (
        "Resolver listy użytkowników. Zwraca obiekty User; GraphQL później wybierze z nich pola wskazane w query.",
        "Resolves the user list. Returns User objects; GraphQL then selects the fields requested by the query.",
    ),
    "create_user": (
        "Wylicza kolejne ID, tworzy User i dopisuje go do users_db. Zwraca nowy obiekt. W wersji z subskrypcją przekazuje go również do kolejek odbiorców.",
        "Calculates the next ID, creates User and appends it to users_db. Returns the object; in the subscription version it also puts it in subscriber queues.",
    ),
    "posts": (
        "Resolver postów. W relacji User filtruje po self.id, w Query po opcjonalnym author_id, a w zadaniu DataLoader przekazuje ID do loader.load.",
        "Post resolver. On User it filters by self.id; on Query by optional author_id; in the DataLoader task it passes the ID to loader.load.",
    ),
    "author": (
        "Łączy Post.author_id z User.id i zwraca autora. To obliczane pole relacji, uruchamiane na żądanie z query.",
        "Matches Post.author_id to User.id and returns the author. This computed relationship field runs when requested by a query.",
    ),
    "search_users": (
        "Wyszukuje fragment name w nazwach użytkowników. casefold po obu stronach ignoruje wielkość liter; brak filtra zwraca całą listę.",
        "Searches for name within user names. casefold on both sides ignores case; no filter returns the full list.",
    ),
    "user_registered": (
        "Generator asynchroniczny zakłada kolejkę dla jednego subskrybenta. Czeka na queue.get i yield emituje użytkownika. finally usuwa kolejkę po zakończeniu.",
        "An async generator creates a queue for one subscriber. It awaits queue.get and yields users. finally removes the queue when finished.",
    ),
    "database": (
        "Kontekst życia bazy: otwiera SQLite, tworzy tabelę i udostępnia połączenie aplikacji. yield oddaje obsługę serwerowi; wyjście zamyka bazę.",
        "Database lifecycle context: opens SQLite, creates a table and exposes the connection to the app. yield hands control to the server; exiting closes the database.",
    ),
    "load_posts": (
        "Funkcja paczkowa DataLoadera. Jedno wywołanie obsługuje wiele ID. Dla każdego keys[i] musi zwrócić listę postów na tej samej pozycji i.",
        "DataLoader batch function. One call handles multiple IDs. For each keys[i], its post list must be returned at the same result index i.",
    ),
    "naive_posts": (
        "Dla każdego użytkownika oddzielnie zwiększa licznik i filtruje posts_db. Trzech rodziców daje trzy pobrania — punkt odniesienia dla DataLoadera.",
        "Separately increments the counter and filters posts_db for each user. Three parents cause three fetches: the DataLoader comparison baseline.",
    ),
    "get_context": (
        "Tworzy kontekst nowego żądania GraphQL z własnym DataLoaderem. Cache loadera nie jest współdzielony między różnymi żądaniami.",
        "Creates a GraphQL request context with its own DataLoader. Loader cache is not shared across requests.",
    ),
    "stats": (
        "Odczytuje licznik fetch_count jako JSON. Służy do sprawdzenia liczby wywołań pobierania postów.",
        "Returns fetch_count as JSON, allowing post-fetch calls to be measured.",
    ),
    "reset": (
        "Zeruje globalny licznik pobrań przed porównaniem dwóch query. Zwraca JSON potwierdzający nową wartość.",
        "Resets the global fetch count before comparing queries and returns its new value as JSON.",
    ),
    "notifications": (
        "Uwierzytelnia gniazdo, wiąże je z ID i utrzymuje aktywne połączenie odbiorcy. finally usuwa sesję po rozłączeniu.",
        "Authenticates the socket, maps it to an ID and keeps the recipient connection open. finally removes the session on disconnection.",
    ),
    "create_notification": (
        "Weryfikuje token administratora, odczytuje JSON i wybiera gniazda konkretnego user_id. Wysyła im powiadomienie i zwraca HTTP 201 z ID odbiorcy.",
        "Verifies the admin token, reads JSON and selects sockets for user_id. Delivers notifications and returns HTTP 201 with the recipient ID.",
    ),
    "history": (
        "Zwraca wspólną listę wiadomości dopisywaną przez handler WS. GraphQL wybierze pola każdej wiadomości.",
        "Returns the shared message list updated by the WS handler. GraphQL selects fields on each message.",
    ),
    "profiles": (
        "Zwraca fake profile użytkowników dostępne przez GraphQL; dane są przechowywane w pamięci procesu.",
        "Returns fake user profiles through GraphQL; data lives in process memory.",
    ),
    "__init__": (
        "Inicjalizuje pustą planszę, turę X, status waiting i słownik graczy. Każda instancja Game ma własny stan.",
        "Initializes an empty board, X turn, waiting status and player dictionary. Each Game instance owns its state.",
    ),
    "snapshot": (
        "Buduje słownik aktualnego stanu gry do wysłania jako JSON: plansza, tura, status. Nie wykonuje ruchu.",
        "Builds the current game state dictionary for JSON delivery: board, turn and status. Does not make a move.",
    ),
    "publish": (
        "Przechodzi po podłączonych graczach i wysyła każdemu ten sam aktualny snapshot. Dzięki temu obaj widzą stan serwera.",
        "Iterates connected players and sends the current snapshot to each, keeping both aligned with server state.",
    ),
    "move": (
        "Sprawdza status, turę i pole, zanim zmieni planszę. Potem wykrywa wygraną, remis albo zmienia turę. Zwraca tekst błędu lub None przy sukcesie.",
        "Validates status, turn and cell before changing the board. Then detects a win, draw or changes turns. Returns an error string or None on success.",
    ),
    "play": (
        "Przypisuje klientowi X lub O, odbiera ruchy JSON i przekazuje je do Game.move. Poprawny ruch rozsyła obu graczom; błędny zgłasza tylko nadawcy.",
        "Assigns X or O, receives JSON moves and calls Game.move. Broadcasts valid moves to both; reports invalid moves only to the sender.",
    ),
}

# Each entry states effects/return values, not merely a restatement of its name.
CALLS = {
    "ClientSession": (
        "Tworzy klienta HTTP/WS aiohttp z pulą połączeń. async with zamyka sesję i jej zasoby po zakończeniu wysyłania.",
        "Creates an aiohttp HTTP/WS client with connection pooling. async with closes the session and its resources after sending.",
    ),
    "dict": (
        "Buduje słownik z nazwanych pól lub par klucz–wartość. W historii SQLite mapuje nazwy kolumn na wartości jednego wiersza.",
        "Builds a dictionary from named fields or key–value pairs. In SQLite history it maps column names to one row’s values.",
    ),
    "zip": (
        "Łączy elementy sekwencji na tych samych pozycjach w pary. Tutaj łączy nazwy kolumn z wartościami wiersza SQLite dla dict.",
        "Pairs items at corresponding positions. Here it pairs SQLite column names with row values for dict.",
    ),
    "dumps": (
        "json.dumps zamienia słownik wiadomości na tekst JSON przed wysłaniem przez broadcast. Odbiorca może odtworzyć pola przez parsowanie JSON.",
        "json.dumps converts a message dictionary into JSON text for broadcast. The receiver can recover fields by parsing JSON.",
    ),
    "isinstance": (
        "Sprawdza, czy obiekt jest instancją podanego typu, uwzględniając podklasy. Tu odrzuca treść powiadomienia, która nie jest str.",
        "Checks whether an object is an instance of a type, including subclasses. Here it rejects notification text that is not str.",
    ),
    "put_nowait": (
        "Dodaje zdarzenie do kolejki natychmiast, bez await. Kolejki subskrybentów są tutaj bez limitu; ograniczona pełna kolejka zgłosiłaby QueueFull.",
        "Immediately enqueues an event without await. Subscriber queues here are unbounded; a full bounded queue would raise QueueFull.",
    ),
    "get_running_loop": (
        "Zwraca aktualnie działającą pętlę asyncio. Jej time() mierzy czas monotoniczny używany do wykrycia braku pong.",
        "Returns the currently running asyncio loop. Its time() provides the monotonic clock used to detect missing pong replies.",
    ),
    "time": (
        "loop.time() zwraca monotoniczny czas pętli w sekundach. Różnica względem last_pong pokazuje, jak długo klient nie odpowiada.",
        "loop.time() returns monotonic loop time in seconds. Subtracting last_pong measures how long the client has been silent.",
    ),
    "removeprefix": (
        "Zwraca tekst bez wskazanego prefiksu, jeśli występuje na początku. Tutaj usuwa Bearer z nagłówka Authorization przed weryfikacją JWT.",
        "Returns text without the supplied leading prefix if present. Here it removes Bearer from Authorization before JWT verification.",
    ),
    "HTTPUnauthorized": (
        "Tworzy wyjątek aiohttp z odpowiedzią HTTP 401 i podanym tekstem. raise przerywa obsługę nieautoryzowanego żądania.",
        "Creates an aiohttp HTTP 401 exception with the supplied text. raise aborts unauthorized request handling.",
    ),
    "HTTPBadRequest": (
        "Tworzy wyjątek aiohttp HTTP 400 dla nieprawidłowych danych wejściowych. raise kończy handler odpowiedzią błędu.",
        "Creates an aiohttp HTTP 400 exception for invalid input. raise ends the handler with an error response.",
    ),
    "InvalidTokenError": (
        "Tworzy wyjątek błędnego JWT. Kod zgłasza go także dla nieznanego sub, żeby przejść do wspólnej obsługi odmowy dostępu.",
        "Creates a JWT validation exception. Code also raises it for an unknown sub to enter the common access-denial branch.",
    ),
    "ValueError": (
        "Tworzy wyjątek dla nieprawidłowej wartości wejściowej. Najbliższy except ValueError zamieni go na kontrolowany błąd protokołu.",
        "Creates an exception for an invalid input value. The nearest except ValueError turns it into a controlled protocol error.",
    ),
    "View": (
        "Tworzy własny widok GraphQL dziedziczący z GraphQLView. Jego get_context zapewnia osobny DataLoader dla każdego żądania.",
        "Creates the custom GraphQLView subclass. Its get_context provides a separate DataLoader per request.",
    ),
    "event": (
        "Rejestruje zdarzenie pomiarowe z czasem, uczestnikiem i dodatkowymi polami. Aplikacja wyświetla je w śladzie wykonania.",
        "Records an observation event with time, actor and extra fields for the app’s execution trace.",
    ),
    "prepare": (
        "Wykonuje handshake HTTP → WebSocket dla request. await czeka na jego zakończenie. Dopiero potem można wysyłać ramki WS.",
        "Performs the HTTP → WebSocket handshake for request. await waits for completion before WS frames can be sent.",
    ),
    "send_str": (
        "Wysyła podany str jako tekstową wiadomość WebSocket. await czeka na operację wysłania, nie na odpowiedź odbiorcy.",
        "Sends the supplied str as a WebSocket text message. await waits for sending, not for the peer’s response.",
    ),
    "send_json": (
        "Serializuje obiekt Pythona do JSON i wysyła go jako tekst WS. Nie zmienia stanu gry ani bazy samo z siebie.",
        "Serializes a Python object to JSON and sends a WS text message. Does not itself change game or database state.",
    ),
    "receive_str": (
        "Czeka na następną tekstową wiadomość WS i zwraca str. Użyte przed pętlą odbiera nick lub token.",
        "Awaits the next WS text message and returns str. Before the loop it consumes a nickname or token.",
    ),
    "ws_connect": (
        "Otwiera połączenie klienta WS i wykonuje handshake z serwerem wskazanym przez URL.",
        "Opens a client WS connection and performs the handshake with the URL’s server.",
    ),
    "close": (
        "Zamyka zasób: dla ws wykonuje zamknięcie WebSocket, code to kod przyczyny. Dla połączenia SQLite zamyka bazę.",
        "Closes a resource: for ws performs WebSocket closure, with code specifying the reason. For SQLite closes the database.",
    ),
    "WebSocketResponse": (
        "Tworzy obiekt serwerowej odpowiedzi WebSocket. Sam konstruktor nie wykonuje handshake; potrzebne jest await prepare(request).",
        "Creates the server WebSocket response object. Construction alone does not perform the handshake: await prepare(request) is required.",
    ),
    "Application": (
        "Tworzy aplikację aiohttp z routerem i stanem. Rejestrujemy w niej trasy i zasoby przed uruchomieniem serwera.",
        "Creates an aiohttp application with a router and state. Routes and resources are registered before starting the server.",
    ),
    "add_get": (
        "Rejestruje handler dla żądania GET pod wskazaną ścieżką. Handler WS zaczyna od GET, a prepare przełącza protokół.",
        "Registers a GET handler at the specified path. A WS handler starts with GET, then prepare upgrades the protocol.",
    ),
    "add_post": (
        "Rejestruje handler HTTP POST. W zadaniach służy do tworzenia powiadomień lub resetowania licznika.",
        "Registers an HTTP POST handler, used here for notifications or resetting a counter.",
    ),
    "add_route": (
        "Wiąże ścieżkę z widokiem. Gwiazdka * dopuszcza różne metody HTTP; GraphQLView obsługuje też upgrade dla subscriptions.",
        "Binds a path to a view. * permits multiple HTTP methods; GraphQLView also supports subscription upgrades.",
    ),
    "Schema": (
        "Buduje schemat Strawberry z klas Query oraz opcjonalnie Mutation i Subscription. Klient może używać tylko pól obecnych w schemacie.",
        "Builds a Strawberry schema from Query and optional Mutation and Subscription classes. Clients can use only schema fields.",
    ),
    "GraphQLView": (
        "Adaptuje schemat Strawberry do aiohttp: wykonuje query i mutation, udostępnia GraphiQL oraz transport subscription.",
        "Adapts the Strawberry schema to aiohttp: executes queries and mutations and exposes GraphiQL and subscription transport.",
    ),
    "type": (
        "W @strawberry.type rejestruje klasę jako typ GraphQL. W type(cell) zwraca dokładny typ obiektu, aby odrzucić bool jako numer pola.",
        "In @strawberry.type registers a GraphQL type. In type(cell) returns the exact object type to reject bool as a cell index.",
    ),
    "field": (
        "Dekorator strawberry.field wystawia metodę jako pole schematu. Resolver uruchamia się, gdy klient wybierze to pole.",
        "strawberry.field exposes a method as a schema field. The resolver runs when a client selects that field.",
    ),
    "mutation": (
        "Oznacza metodę jako operację zmiany danych w GraphQL. Zwracana wartość może być wybrana polami w mutation.",
        "Marks a method as a GraphQL data-changing operation. The mutation can select fields on its returned value.",
    ),
    "subscription": (
        "Oznacza generator asynchroniczny jako źródło strumienia zdarzeń GraphQL. Każde yield przekazuje nowy wynik.",
        "Exposes an async generator as a GraphQL event stream. Each yield emits a new result.",
    ),
    "ID": (
        "Oznacza identyfikator w schemacie GraphQL. W przykładach przechowujemy go jako tekst, nawet gdy zawiera cyfry.",
        "Marks a GraphQL identifier. These examples store IDs as text even when they contain digits.",
    ),
    "append": (
        "Dopisuje jeden element na końcu listy i zwraca None. W fake bazie to moment zmiany przechowywanych danych.",
        "Appends one element to a list and returns None. For the fake database this is the data mutation point.",
    ),
    "add": (
        "Dodaje element do zbioru. Ten sam element nie pojawi się dwukrotnie; używamy tego dla gniazd i kolejek subskrybentów.",
        "Adds an element to a set. Duplicate elements are not stored; used for sockets and subscriber queues.",
    ),
    "discard": (
        "Usuwa element ze zbioru, jeśli istnieje. Brak elementu nie wywołuje KeyError, co ułatwia bezpieczne sprzątanie.",
        "Removes an element from a set if present. Missing elements do not raise KeyError, making cleanup safe.",
    ),
    "pop": (
        "Usuwa i zwraca wartość słownika pod kluczem. Drugi argument None zabezpiecza przypadek, gdy klucz już nie istnieje.",
        "Removes and returns a dictionary value by key. The None default handles an already missing key.",
    ),
    "setdefault": (
        "Zwraca istniejącą wartość pod kluczem albo zapisuje i zwraca domyślną. Pozwala utworzyć zbiór pokoju przy pierwszym wejściu.",
        "Returns an existing dictionary value or inserts and returns the default, creating a room’s set on first join.",
    ),
    "get": (
        "Dla słownika odczytuje klucz z wartością domyślną. Dla asyncio.Queue: await get() czeka na element i zdejmuje go z kolejki.",
        "On a dictionary reads a key with a default. On asyncio.Queue, await get() waits for and removes an item.",
    ),
    "put": (
        "Wstawia element do asyncio.Queue. await może oddać sterowanie, gdy kolejka ma limit i jest pełna; tutaj kolejki nie mają limitu.",
        "Puts an item into asyncio.Queue. await can yield when a bounded queue is full; these queues are unbounded.",
    ),
    "Queue": (
        "Tworzy asynchroniczną kolejkę FIFO. Każdy subskrybent ma własną, aby wszyscy dostali każde zdarzenie.",
        "Creates an async FIFO queue. Each subscriber has its own so every subscriber receives every event.",
    ),
    "Event": (
        "Tworzy sygnał synchronizacji asyncio. W demonstracji potwierdza, że generator dodał już kolejkę subskrybenta.",
        "Creates an asyncio synchronization flag, confirming in the demo that the subscriber queue has been registered.",
    ),
    "set": (
        "Dla Event.set ustawia flagę i budzi oczekujących. Samo set() bez odbiorcy tworzy pusty zbiór.",
        "Event.set sets the flag and wakes waiters. Bare set() creates an empty set.",
    ),
    "sleep": (
        "Oddaje sterowanie na podany czas w sekundach. Pętla zdarzeń może wtedy obsługiwać inne połączenia.",
        "Yields for the supplied duration in seconds, allowing the event loop to serve other connections.",
    ),
    "wait_for": (
        "Czeka na korutynę najwyżej timeout sekund. Przekroczenie limitu anuluje oczekiwanie i zgłasza TimeoutError.",
        "Awaits a coroutine for at most timeout seconds, then cancels the wait and raises TimeoutError.",
    ),
    "create_task": (
        "Planuje korutynę jako niezależny Task w bieżącej pętli zdarzeń. Nie czeka na jej zakończenie.",
        "Schedules a coroutine as an independent Task in the running event loop without waiting for completion.",
    ),
    "cancel": (
        "Zgłasza żądanie anulowania Task. CancelledError pojawi się w korutynie przy oddaniu sterowania; potem trzeba zaczekać na sprzątanie.",
        "Requests Task cancellation. CancelledError is raised when the coroutine yields; cleanup should then be awaited.",
    ),
    "gather": (
        "Czeka na przekazane zadania. return_exceptions=True zbiera również wyjątki, co umożliwia zakończenie sprzątania po cancel.",
        "Waits for the supplied tasks. return_exceptions=True collects exceptions too, allowing cleanup after cancellation.",
    ),
    "monotonic": (
        "Zwraca monotoniczny zegar w sekundach. Zmiana zegara systemowego nie cofa pomiaru czasu od ostatniego pong.",
        "Returns a monotonic clock in seconds, unaffected by wall-clock changes when measuring time since pong.",
    ),
    "perf_counter": (
        "Zwraca dokładny zegar do pomiaru upływu czasu. Czas trwania to odczyt końcowy minus początkowy.",
        "Returns a high-resolution elapsed-time clock. Duration is the final reading minus the initial reading.",
    ),
    "decode": (
        "jwt.decode sprawdza podpis tokenu, dozwolony algorytm HS256 i wymagane exp/sub. Błędny albo wygasły token zgłasza InvalidTokenError.",
        "jwt.decode validates the signature, allowed HS256 algorithm and required exp/sub claims. Invalid or expired tokens raise InvalidTokenError.",
    ),
    "json": (
        "Dekoduje tekst JSON do obiektu Pythona. await request.json czyta body HTTP; message.json parsuje wiadomość WS. Nieprawidłowy JSON może zgłosić ValueError.",
        "Decodes JSON into Python objects. await request.json reads HTTP body; message.json parses a WS message. Malformed JSON may raise ValueError.",
    ),
    "json_response": (
        "Serializuje dane jako JSON i tworzy odpowiedź HTTP; status określa kod HTTP. To nie jest wysyłanie ramki WebSocket.",
        "Serializes data to a JSON HTTP response; status sets its HTTP status code. This does not send a WebSocket frame.",
    ),
    "connect": (
        "aiosqlite.connect otwiera plik SQLite. async with zarządza zamknięciem połączenia po zakończeniu kontekstu.",
        "aiosqlite.connect opens a SQLite file. async with closes the connection when its context exits.",
    ),
    "execute": (
        "Wykonuje zapytanie SQLite. Znaki ? są miejscami na parametry przekazane oddzielnie; INSERT wymaga późniejszego commit.",
        "Executes a SQLite statement. ? placeholders receive separately supplied parameters; INSERT requires a later commit.",
    ),
    "commit": (
        "Zatwierdza bieżącą transakcję SQLite. Dopiero po zatwierdzeniu pokaz rozsyła zapisany wpis.",
        "Commits the current SQLite transaction. The demo broadcasts the saved message after committing.",
    ),
    "fetchall": (
        "Odczytuje wszystkie wiersze wyniku kursora jako listę. W historii SELECT LIMIT 50 ogranicza liczbę tych wierszy.",
        "Reads all cursor result rows as a list. The history query limits this to 50 with SELECT LIMIT 50.",
    ),
    "Lock": (
        "Tworzy asyncio.Lock. async with lock wpuszcza jedną korutynę naraz do chronionego odczytu lub zapisu historii.",
        "Creates asyncio.Lock. async with lock lets one coroutine at a time enter protected history reads or writes.",
    ),
    "DataLoader": (
        "Tworzy loader z funkcją paczkową load_fn. Grupuje klucze i pamięta wyniki w ramach jednej instancji, tutaj jednego żądania.",
        "Creates a loader with batch function load_fn. Batches keys and caches results within this instance, here one request.",
    ),
    "load": (
        "Zgłasza jeden klucz do DataLoadera i zwraca awaitable wyniku. Loader łączy równoczesne load w jedną paczkę load_posts.",
        "Requests one key from DataLoader and returns an awaitable result. Concurrent loads are combined into one load_posts batch.",
    ),
    "next": (
        "Zwraca pierwszy element generatora. Drugi argument None jest wynikiem, gdy nic nie pasuje; bez niego byłby StopIteration.",
        "Returns the first generator item. A None default handles no match; without a default StopIteration would be raised.",
    ),
    "max": (
        "Wybiera największą wartość. Tutaj służy do znalezienia najwyższego ID przed dodaniem 1 dla nowego użytkownika.",
        "Selects the largest value, used here to find the highest ID before adding 1 for a new user.",
    ),
    "casefold": (
        "Zwraca nowy tekst do porównywania bez wielkości liter. Nie zmienia oryginalnej nazwy użytkownika.",
        "Returns text suitable for case-insensitive comparison without changing the original user name.",
    ),
    "strip": (
        "Zwraca tekst bez białych znaków na początku i końcu. Pozwala odrzucić pusty nick złożony ze spacji.",
        "Returns text without leading or trailing whitespace, allowing blank space-only nicknames to be rejected.",
    ),
    "startswith": (
        "Sprawdza prefiks tekstu i zwraca bool. W pokojach rozpoznaje komendę /join zamiast zwykłej wiadomości.",
        "Checks a text prefix and returns bool, recognizing /join as a command rather than a chat message.",
    ),
    "split": (
        "Dzieli tekst na części. maxsplit ogranicza liczbę podziałów, aby wydzielić nazwę pokoju po komendzie.",
        "Splits text into parts. maxsplit limits splitting to extract the room name after the command.",
    ),
    "values": (
        "Zwraca widok wartości słownika. W grze sprawdzamy przypisane symbole, aby nowy gracz dostał wolny X lub O.",
        "Returns a dictionary values view. The game checks assigned symbols to select a free X or O.",
    ),
    "tuple": (
        "Tworzy niezmienną migawkę elementów kolekcji na potrzeby pętli. Późniejsze zmiany zbioru nie zmienią tej migawki.",
        "Creates an immutable collection snapshot for iteration; later set changes do not change this snapshot.",
    ),
    "len": (
        "Zwraca liczbę elementów kolekcji, np. aktywnych klientów. Dla zbioru zawiera tylko unikatowe elementy.",
        "Returns collection size, such as the active client count. Sets contain unique elements only.",
    ),
    "any": (
        "Zwraca True, gdy choć jeden element jest prawdziwy. W grze szuka dowolnej zwycięskiej linii spośród ośmiu.",
        "Returns True when any item is truthy. The game checks whether any of the eight winning lines is complete.",
    ),
    "all": (
        "Zwraca True, gdy wszystkie elementy są prawdziwe. W grze sprawdza komplet symboli w linii lub zapełnienie planszy.",
        "Returns True when every item is truthy, checking a complete winning line or a full board.",
    ),
    "reversed": (
        "Zwraca iterator od końca sekwencji. Odwraca najnowsze wpisy SQLite do kolejności chronologicznej bez zmiany samej listy.",
        "Iterates a sequence backwards, turning recent SQLite rows into chronological order without modifying the list.",
    ),
    "str": (
        "Zwraca tekstową reprezentację wartości. Ujednolica typ ID używany w filtrach i DataLoaderze.",
        "Returns a text representation, keeping ID types consistent in filters and DataLoader.",
    ),
    "int": (
        "Konwertuje wartość na liczbę całkowitą, np. tekst ID przed obliczeniem nowego identyfikatora.",
        "Converts a value to an integer, such as a text ID before calculating the next ID.",
    ),
    "print": (
        "Wypisuje tekst do stdout procesu. W pokazie konsola jest przechwytywana i widoczna w dzienniku zdarzeń.",
        "Writes to process stdout, captured by the demo and displayed in the event log.",
    ),
    "now": (
        "datetime.now(timezone.utc) pobiera aktualny czas ze strefą UTC, aby zapisy historii miały jednoznaczne znaczniki.",
        "datetime.now(timezone.utc) reads the current timezone-aware UTC timestamp for history records.",
    ),
    "isoformat": (
        "Zwraca tekst daty i czasu w formacie ISO 8601. Można go zapisać w SQLite i wysłać w JSON.",
        "Returns an ISO 8601 date/time string for SQLite storage and JSON delivery.",
    ),
    "runtime_file": (
        "Wyznacza plik w katalogu roboczym tego pokazu. Osobny katalog zapobiega mieszaniu historii różnych uruchomień.",
        "Chooses a file in this demo’s work directory, isolating history between runs.",
    ),
    "metric": (
        "Rejestruje rzeczywisty pomiar dla aplikacji prezentacyjnej. To instrumentacja pokazu, nie część protokołu WebSocket.",
        "Records an actual measurement for the teaching app. This is demo instrumentation, not part of the WebSocket protocol.",
    ),
}


def expression(node):
    return ast.unparse(node)


def describe(node):
    """Explain one actual statement; function/call notes add operation-specific detail."""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        if node.name == "create_user" and "subscribers" not in expression(node):
            return pair(
                "Resolver mutacji tworzy User z kolejnym ID, dopisuje go do users_db i zwraca nowy obiekt. Ten zapis jest widoczny dla kolejnych query w tym samym procesie.",
                "The mutation resolver creates User with the next ID, appends it to users_db and returns it. Subsequent queries in this process see the change.",
            )
        if node.name == "posts":
            body = expression(node)
            if "posts_loader" in body:
                return pair(
                    "Resolver pola User.posts przekazuje tekst self.id do DataLoadera z kontekstu tego żądania. await load czeka na wynik wspólnej paczki; zwracana jest lista tytułów tej osoby.",
                    "The User.posts resolver passes text self.id to the request context DataLoader. await load waits for a batch result and returns this user’s post titles.",
                )
            if "author_id is None" in body:
                return pair(
                    "Resolver Query.posts zwraca posty wskazanego author_id. Brak argumentu daje None i przepuszcza wszystkie posty. GraphQL nazywa argument authorId.",
                    "Query.posts returns posts matching author_id. Omission yields None and includes all posts. GraphQL exposes the argument as authorId.",
                )
            return pair(
                "Resolver User.posts filtruje posts_db: zostawia posty, których author_id równa się self.id bieżącego użytkownika. Zwraca listę obiektów Post, również pustą przy braku postów.",
                "User.posts filters posts_db to posts whose author_id matches the current user’s self.id. Returns Post objects, or an empty list if there are none.",
            )
        return pair(
            *FUNCTIONS.get(
                node.name,
                (
                    "Definiuje funkcję obsługującą poniższy blok. Argumenty są wejściem, return oddaje wynik wywołującemu.",
                    "Defines the function below. Arguments are inputs; return passes results to the caller.",
                ),
            )
        )
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return pair(
            f"Import udostępnia nazwy: {expression(node)}. Python ładuje moduł raz na proces; użyte niżej nazwy wskazują jego obiekty.",
            f"This import exposes names: {expression(node)}. Python loads a module once per process; the names below refer to its objects.",
        )
    if isinstance(node, ast.ClassDef):
        purpose = {
            "User": (
                "dane użytkownika i pola relacji",
                "user data and relationship fields",
            ),
            "Post": ("dane posta i jego autora", "post data and its author"),
            "Query": ("operacje odczytu GraphQL", "GraphQL read operations"),
            "Mutation": (
                "operacje zmiany danych GraphQL",
                "GraphQL data-changing operations",
            ),
            "Subscription": ("strumienie zdarzeń GraphQL", "GraphQL event streams"),
            "Game": (
                "stan jednej partii i reguły ruchów",
                "one game’s state and move rules",
            ),
            "View": (
                "kontekst żądania z DataLoaderem",
                "a request context with DataLoader",
            ),
        }.get(node.name, ("strukturę danych", "a data structure"))
        return pair(
            f"Klasa {node.name} grupuje {purpose[0]}. Pola i metody poniżej określają jej dane oraz zachowanie.",
            f"Class {node.name} groups {purpose[1]}. The fields and methods below define its data and behavior.",
        )
    if isinstance(node, ast.If):
        condition = expression(node.test)
        return pair(
            f"Sprawdza warunek `{condition}`. Gdy jest prawdziwy, wykonuje wcięty blok; w przeciwnym razie przechodzi do elif / else albo za ten blok.",
            f"Tests `{condition}`. When true, executes the indented branch; otherwise proceeds to elif / else or beyond this block.",
        )
    if isinstance(node, (ast.For, ast.AsyncFor)):
        target, source = expression(node.target), expression(node.iter)
        return pair(
            f"Pętla przypisuje kolejne elementy `{source}` do `{target}` i wykonuje blok dla każdego. "
            + (
                "async for czeka na wiadomości bez blokowania innych połączeń; zamknięcie WS kończy iterację."
                if isinstance(node, ast.AsyncFor)
                else "continue przechodzi do kolejnego elementu; break zakończyłby pętlę."
            ),
            f"Assigns successive items from `{source}` to `{target}` and executes the body. "
            + (
                "async for awaits messages without blocking other connections; WS closure ends iteration."
                if isinstance(node, ast.AsyncFor)
                else "continue proceeds to the next item; break would exit the loop."
            ),
        )
    if isinstance(node, ast.While):
        return pair(
            f"Powtarza blok, dopóki `{expression(node.test)}` jest prawdziwe. W generatorze subskrypcji await czeka na zdarzenie, a yield emituje kolejne dane.",
            f"Repeats while `{expression(node.test)}` is true. In the subscription generator await waits for events and yield emits data.",
        )
    if isinstance(node, (ast.With, ast.AsyncWith)):
        contexts = ", ".join(expression(i.context_expr) for i in node.items)
        return pair(
            f"Wchodzi do kontekstu `{contexts}`. Wyjście z bloku uruchamia sprzątanie także przy wyjątku. Dla lock to zwolnienie blokady; dla bazy lub sesji — zamknięcie zasobu.",
            f"Enters context `{contexts}`. Exiting runs cleanup even on exceptions. A lock is released; a database or session resource is closed.",
        )
    if isinstance(node, ast.Try):
        return pair(
            "Wykonuje blok try. Pasujące except obsłuży wyjątek, a finally wykona się niezależnie od sukcesu. W handlerze to gwarantowane miejsce usunięcia klienta lub anulowania zadania.",
            "Runs try. A matching except handles an exception; finally executes on success or failure. In a handler this guarantees client removal or task cancellation.",
        )
    if isinstance(node, ast.ExceptHandler):
        return pair(
            f"Obsługuje wyjątki {expression(node.type) if node.type else 'wszystkich typów'}. Wykonuje ten blok zamiast przerywać handler nieobsłużonym błędem.",
            f"Handles {expression(node.type) if node.type else 'all'} exceptions, running this block instead of allowing an unhandled failure to escape.",
        )
    if isinstance(node, ast.Return):
        value = expression(node.value) if node.value else "None"
        return pair(
            f"Kończy bieżące wywołanie i zwraca `{value}`. W resolverze wynik stanie się danymi GraphQL; return ws oddaje zakończoną odpowiedź aiohttp.",
            f"Ends this call and returns `{value}`. A resolver result becomes GraphQL data; return ws returns the completed aiohttp response.",
        )
    if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
        target = (
            ", ".join(expression(i) for i in node.targets)
            if isinstance(node, ast.Assign)
            else expression(node.target)
        )
        value = expression(node.value) if node.value else None
        if value is None:
            return pair(
                f"Adnotacja pola `{target}` ma typ `{expression(node.annotation)}`. Strawberry używa typów do budowy schematu; samo wskazanie typu nie przypisuje wartości.",
                f"Field `{target}` has type `{expression(node.annotation)}`. Strawberry uses annotations to build the schema; an annotation alone does not assign a value.",
            )
        verb = (
            ("Aktualizuje", "Updates")
            if isinstance(node, ast.AugAssign)
            else (
                "Oblicza prawą stronę i zapisuje wynik w",
                "Evaluates the right-hand side and stores the result in",
            )
        )
        extra = (
            (
                " await czeka na wynik, oddając sterowanie pętli zdarzeń.",
                " await waits for the result while yielding to the event loop.",
            )
            if any(isinstance(n, ast.Await) for n in ast.walk(node.value))
            else ("", "")
        )
        if isinstance(node.value, (ast.ListComp, ast.GeneratorExp)):
            extra = (
                " Comprehension buduje wynik z elementów przechodzących warunek if; kolejność pochodzi ze źródłowej kolekcji.",
                " The comprehension builds results from items passing if; ordering follows the source collection.",
            )
        return pair(
            f"{verb[0]} `{target}`: `{value}`.{extra[0]}",
            f"{verb[1]} `{target}`: `{value}`.{extra[1]}",
        )
    if isinstance(node, ast.Expr):
        inner = node.value
        if isinstance(inner, ast.Yield):
            return pair(
                f"yield oddaje `{expression(inner.value) if inner.value else 'sterowanie'}` i zawiesza generator. W subskrypcji emituje zdarzenie; w cleanup_ctx rozdziela start od sprzątania.",
                f"yield hands off `{expression(inner.value) if inner.value else 'control'}` and suspends the generator. In subscriptions it emits an event; in cleanup_ctx it separates startup from cleanup.",
            )
        if isinstance(inner, ast.Constant) and isinstance(inner.value, str):
            return pair(
                "Tekst dokumentujący cel tego fragmentu; nie jest wysyłany do klienta.",
                "Documentation text describing this fragment; it is not sent to the client.",
            )
        awaited = isinstance(inner, ast.Await)
        call = inner.value if awaited else inner
        if isinstance(call, ast.Call):
            name = (
                call.func.attr
                if isinstance(call.func, ast.Attribute)
                else getattr(call.func, "id", "")
            )
            if name in FUNCTIONS or name in CALLS:
                note = pair(*(FUNCTIONS.get(name) or CALLS[name]))
                if awaited:
                    note = pair(
                        "await oddaje sterowanie do czasu zakończenia operacji. "
                        + note["pl"],
                        "await yields until the operation finishes. " + note["en"],
                    )
                return note
        return pair(
            f"Wykonuje `{expression(inner)}` dla efektu ubocznego; wynik nie jest przypisany do zmiennej.",
            f"Evaluates `{expression(inner)}` for its side effect; no result is assigned.",
        )
    if isinstance(node, ast.Continue):
        return pair(
            "Pomija resztę tej iteracji i wraca do początku najbliższej pętli. Tak ignorujemy inne typy ramek niż tekst.",
            "Skips the remainder of this iteration and returns to the nearest loop, ignoring non-text frames here.",
        )
    if isinstance(node, ast.Global):
        return pair(
            f"global {', '.join(node.names)} kieruje późniejsze przypisania do zmiennej modułu, zamiast tworzyć lokalną zmienną funkcji.",
            f"global {', '.join(node.names)} makes later assignments target module state instead of creating a function-local variable.",
        )
    if isinstance(node, ast.Raise):
        return pair(
            f"Zgłasza wyjątek `{expression(node.exc)}`. Bieżący normalny przepływ zostaje przerwany; wykonają się pasujące except i finally.",
            f"Raises `{expression(node.exc)}`, interrupting normal flow and entering matching except and finally blocks.",
        )
    return pair(
        f"Instrukcja `{expression(node)}` jest częścią otaczającego bloku. Prześledź jej wartości w kontekście funkcji.",
        f"Statement `{expression(node)}` belongs to the surrounding block. Trace its values within the function.",
    )


def build(source, file):
    tree = ast.parse(source)
    lines = source.splitlines()
    notes = {}
    symbols = {}
    blocks = []

    def add(kind, start, end, title, body, expression_text=None):
        key = f"{file}:{kind}:{len(notes)}"
        notes[key] = dict(
            id=key,
            kind=kind,
            file=file,
            start=start,
            end=end,
            title=title,
            body=body,
            expression=expression_text,
        )
        return key

    definitions = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    nodes = list(ast.walk(tree))
    statements = [n for n in nodes if isinstance(n, (ast.stmt, ast.ExceptHandler))]
    block_types = (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.Try,
        ast.With,
        ast.AsyncWith,
        ast.ExceptHandler,
    )
    for node in statements:
        if isinstance(node, block_types):
            label = (
                node.name
                if hasattr(node, "name") and isinstance(node.name, str)
                else type(node).__name__.replace("Async", "async ")
            )
            key = add("block", node.lineno, node.end_lineno, label, describe(node))
            blocks.append((node.lineno, node.end_lineno, key))
    for node in nodes:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            line = lines[node.lineno - 1]
            col = line.index(
                node.name,
                node.col_offset + (10 if isinstance(node, ast.AsyncFunctionDef) else 4),
            )
            key = add(
                "function",
                node.lineno,
                node.end_lineno,
                node.name + "()",
                describe(node),
                line.strip(),
            )
            symbols.setdefault(node.lineno, []).append((col, col + len(node.name), key))
        elif isinstance(node, ast.Call):
            func = node.func
            name = (
                func.attr
                if isinstance(func, ast.Attribute)
                else getattr(func, "id", None)
            )
            if not name:
                continue
            end_line, end_col = func.end_lineno, func.end_col_offset
            # AST column positions are UTF-8 byte offsets; DOM/Pygments use characters.
            end_col = len(lines[end_line - 1].encode("utf-8")[:end_col].decode("utf-8"))
            start_col = end_col - len(name)
            kind = "method" if isinstance(func, ast.Attribute) else "function"
            body = (
                pair(*(FUNCTIONS.get(name) or CALLS[name]))
                if name in FUNCTIONS or name in CALLS
                else None
            )
            if name == "next" and len(node.args) == 1:
                body = pair(
                    "Zwraca pierwszy pasujący element generatora. Tutaj nie podano wartości domyślnej: brak autora zgłosi StopIteration. Fake dane gwarantują, że każdy post ma autora.",
                    "Returns the first matching generator item. No default is supplied here: a missing author raises StopIteration. The fake data guarantees an author for each post.",
                )
            elif name == "set" and isinstance(func, ast.Name):
                body = pair(
                    "Tworzy pusty zbiór set. Przechowujemy w nim unikatowe aktywne gniazda lub kolejki subskrybentów; add dopisuje, discard usuwa.",
                    "Creates an empty set of unique active sockets or subscriber queues. add inserts and discard removes entries.",
                )
            elif name == "get" and isinstance(func, ast.Attribute):
                body = (
                    pair(
                        "Czeka asynchronicznie na element kolejki i zdejmuje go z niej. W generatorze yield wyemituje otrzymanego użytkownika do jednego subskrybenta.",
                        "Asynchronously waits for and removes a queue item. The generator yields the received user to one subscriber.",
                    )
                    if "queue" in expression(func.value)
                    else pair(
                        "Odczytuje wartość słownika pod wskazanym kluczem. Drugi argument jest wartością domyślną, gdy klucza brakuje; nie usuwa wpisu.",
                        "Reads a dictionary value by key. The second argument is the default when absent; the entry is not removed.",
                    )
                )
            elif (
                name == "close"
                and isinstance(func, ast.Attribute)
                and expression(func.value) == "db"
            ):
                body = pair(
                    "Zamyka połączenie SQLite. W finally funkcji database wykonuje się przy zakończeniu życia aplikacji, również po błędzie.",
                    "Closes the SQLite connection. In database’s finally this runs on application shutdown, including failure.",
                )
            elif (
                name == "values"
                and isinstance(func, ast.Attribute)
                and expression(func.value) == "record"
            ):
                body = pair(
                    "Zwraca wartości record w kolejności dodania pól: nickname, body, sent_at. tuple zamienia je w parametry odpowiadające trzem znakom ? w INSERT.",
                    "Returns record values in insertion order: nickname, body, sent_at. tuple turns them into parameters for the three INSERT placeholders.",
                )
            if body is None:
                if name in {"User", "Post", "Message", "Profile", "Game"}:
                    body = pair(
                        f"Konstruktor {name} tworzy nowy obiekt z podanych pól. Argumenty nazwane wskazują, która wartość trafi do którego pola.",
                        f"The {name} constructor creates an object from the supplied fields. Named arguments map values to their fields.",
                    )
                else:
                    body = pair(
                        f"Wywołanie `{expression(func)}` przekazuje poniższe argumenty i oddaje wynik do otaczającego wyrażenia. Sprawdź definicję/import tej nazwy w pliku.",
                        f"Calling `{expression(func)}` passes the arguments below and returns a value to the surrounding expression. Inspect its definition/import in this file.",
                    )
            # Calls should highlight the call site; function definitions have their whole range.
            key = add(
                kind,
                node.lineno,
                node.end_lineno,
                expression(func) + "()",
                body,
                expression(node),
            )
            symbols.setdefault(end_line, []).append((start_col, end_col, key))

    # Also explain function references passed as callbacks (not only calls).
    for node in nodes:
        if (
            not isinstance(node, ast.Name)
            or not isinstance(node.ctx, ast.Load)
            or node.id not in definitions
        ):
            continue
        row = node.lineno
        col = len(lines[row - 1].encode("utf-8")[: node.col_offset].decode("utf-8"))
        end = col + len(node.id)
        if any(start < end and stop > col for start, stop, _ in symbols.get(row, [])):
            continue
        definition = definitions[node.id]
        key = add(
            "function",
            row,
            row,
            node.id + " · callback",
            pair(
                "Tutaj przekazujemy samą funkcję, bez jej wywołania. Biblioteka uruchomi ją później, np. aiohttp po żądaniu, a DataLoader po zebraniu kluczy. "
                + describe(definition)["pl"],
                "This passes the function itself without calling it. The library invokes it later, e.g. aiohttp on a request or DataLoader after collecting keys. "
                + describe(definition)["en"],
            ),
            node.id,
        )
        symbols.setdefault(row, []).append((col, end, key))

    rows = []
    formatter = HtmlFormatter()
    for number, line in enumerate(lines, 1):
        matching = [n for n in statements if n.lineno <= number <= n.end_lineno]
        node = (
            min(matching, key=lambda n: (n.end_lineno - n.lineno, -n.lineno))
            if matching
            else None
        )
        stripped = line.strip()
        if not stripped:
            body = pair(
                "Pusty wiersz oddziela etapy wizualnie; nie wykonuje żadnej instrukcji.",
                "A blank line visually separates stages and executes no statement.",
            )
        elif stripped.startswith("finally:"):
            body = pair(
                "finally wykona ten blok przy normalnym zakończeniu, wyjątku i anulowaniu. Tutaj zwalniamy zasoby albo usuwamy klienta ze wspólnego stanu.",
                "finally runs on normal completion, exception and cancellation. Here it releases resources or removes the client from shared state.",
            )
        elif stripped.startswith("else:"):
            body = pair(
                "Ten blok wykona się, gdy wcześniejszy warunek if / elif nie był spełniony. W grze oznacza to brak wygranej i remisu: przechodzimy do kolejnej tury.",
                "This branch runs when the preceding if / elif conditions are false. In the game that means no win or draw: continue to the next turn.",
            )
        elif stripped.startswith("@"):
            name = stripped.split(".")[-1].split("(")[0]
            body = pair(
                *CALLS.get(
                    name,
                    (
                        "Dekorator modyfikuje definicję poniżej przy ładowaniu modułu, np. rejestruje pole schematu.",
                        "The decorator modifies the definition below when the module loads, for example registering a schema field.",
                    ),
                )
            )
        elif stripped.startswith("#"):
            body = pair(
                "Komentarz autora: " + stripped.lstrip("# "),
                "Author comment: " + stripped.lstrip("# "),
            )
        else:
            body = (
                describe(node)
                if node
                else pair(
                    "Kontynuacja zapisu wyrażenia z poprzedniej linii.",
                    "Continuation of the expression from the previous line.",
                )
            )
        if (
            node
            and number > node.lineno
            and not isinstance(node, block_types)
            and stripped
            and not stripped.startswith(("#", "@"))
        ):
            body = pair(
                f"To dalszy ciąg instrukcji z linii {node.lineno}. " + body["pl"],
                f"This continues the statement on line {node.lineno}. " + body["en"],
            )
        line_key = add(
            "line", number, number, f"{file} · L{number}", body, line.strip()
        )
        candidates = [b for b in blocks if b[0] <= number <= b[1]]
        block_key = (
            min(candidates, key=lambda b: b[1] - b[0])[2] if candidates else line_key
        )
        spans = sorted(symbols.get(number, []))
        # Split Pygments tokens at symbol boundaries while retaining lexer colors.
        chunks = []
        offset = 0
        for token, value in lex(line, PythonLexer(stripnl=False, ensurenl=False)):
            css = formatter._get_css_class(token)
            boundaries = {0, len(value)}
            for start, end, _ in spans:
                for boundary in (start, end):
                    if offset < boundary < offset + len(value):
                        boundaries.add(boundary - offset)
            ordered = sorted(boundaries)
            for a, b in zip(ordered, ordered[1:]):
                text = html.escape(value[a:b])
                color = f'<span class="{css}">{text}</span>' if css else text
                note = next(
                    (
                        key
                        for start, end, key in spans
                        if start <= offset + a and offset + b <= end
                    ),
                    None,
                )
                if note:
                    color = f'<span class="code-symbol" data-note="{html.escape(note)}" tabindex="0" role="button" aria-label="{html.escape(notes[note]["title"])}">{color}</span>'
                chunks.append(color)
            offset += len(value)
        rows.append(
            dict(
                html="".join(chunks),
                line=number,
                line_note=line_key,
                block_note=block_key,
            )
        )
    return dict(source=source, notes=notes, annotated_rows=rows)
