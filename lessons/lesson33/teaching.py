"""Semantic statement explanations: detailed source walkthrough and brief compilation."""

import ast


def pair(pl, en):
    return {"pl": pl, "en": en}


FUNCTIONS = {
    "root": ("Zwraca stałą wiadomość powitalną.", "Returns a fixed greeting."),
    "current_time": (
        "Odczytuje czas UTC i zwraca go jako tekst ISO w JSON.",
        "Reads UTC time and returns ISO text in JSON.",
    ),
    "random_number": (
        "Losuje liczbę całkowitą 1–100, włącznie z obiema granicami.",
        "Draws an integer from 1 through 100, including both bounds.",
    ),
    "greet": (
        "Otrzymuje imię ze ścieżki, już po walidacji minimum dwóch znaków.",
        "Receives a path name after minimum-length validation.",
    ),
    "calculate": (
        "Wybiera działanie według operation i odrzuca dzielenie przez zero.",
        "Selects an operation and rejects division by zero.",
    ),
    "product_total": (
        "Otrzymuje zwalidowany Product i oblicza cenę razy ilość.",
        "Receives a validated Product and multiplies price by quantity.",
    ),
    "list_books": (
        "Zwraca kolekcję książek; zapytanie SQL może ją ograniczać i sortować.",
        "Returns the book collection; SQL queries may filter and order it.",
    ),
    "get_book": (
        "Wyszukuje książkę po ID i obsługuje brak przez 404.",
        "Finds a book by ID and handles absence with 404.",
    ),
    "create_book": (
        "Otrzymuje dane książki; tworzy rekord lub odsyła zwalidowany model, zależnie od tego ćwiczenia.",
        "Receives book data; creates a record or echoes the validated model, depending on this exercise.",
    ),
    "delete_book": (
        "Usuwa książkę po sprawdzeniu jej istnienia i zwraca status określony w trasie.",
        "Deletes an existing book and returns the route’s specified status.",
    ),
    "replace_book": (
        "Pełna aktualizacja PUT zastępuje pola książki danymi z modelu wejściowego.",
        "A full PUT update replaces book fields with the input model.",
    ),
    "create_user": (
        "Otrzymuje model użytkownika zwalidowany przez Pydantic.",
        "Receives a user model validated by Pydantic.",
    ),
    "list_users": (
        "Odczytuje użytkowników i przygotowuje ich publiczne ID oraz nazwy.",
        "Reads users and prepares their public IDs and names.",
    ),
    "get_user": (
        "Odczytuje jednego użytkownika albo zwraca 404.",
        "Reads one user or returns 404.",
    ),
    "replace_user": (
        "Sprawdza właściciela konta i zapisuje nową nazwę użytkownika.",
        "Checks account ownership and saves the new user name.",
    ),
    "delete_user": (
        "Sprawdza właściciela i usuwa konto; klucze obce obsługują usuwanie zależnych danych.",
        "Checks ownership and deletes the account; foreign keys handle dependent data.",
    ),
    "list_authors": (
        "Zwraca listę autorów z tego modułu routera.",
        "Returns the authors from this router module.",
    ),
    "verify_api_key": (
        "Dependency sprawdza nagłówek X-API-Key przed uruchomieniem endpointu.",
        "This dependency checks X-API-Key before the endpoint runs.",
    ),
    "stats": (
        "Zwraca demonstracyjne statystyki po pomyślnym sprawdzeniu klucza.",
        "Returns demonstration statistics after key verification.",
    ),
    "validate_name": (
        "Walidator pola odrzuca nazwy zawierające inne znaki niż litery i cyfry.",
        "The field validator rejects names containing anything except letters and digits.",
    ),
    "create_product": (
        "Otrzymuje Product po wykonaniu wszystkich reguł walidacji.",
        "Receives Product after all validation rules have run.",
    ),
    "create_author": (
        "Zapisuje nowego autora i odbiera ID nadane przez bazę.",
        "Saves a new author and receives the database-generated ID.",
    ),
    "author_books": (
        "Odczytuje autora i jego książki przez eager loading, zanim sesja zostanie zamknięta.",
        "Reads an author and books with eager loading before the session closes.",
    ),
    "append_notification": (
        "Zapisuje symulację powiadomienia do pliku po wysłaniu odpowiedzi HTTP.",
        "Writes a simulated notification after the HTTP response is sent.",
    ),
    "update_stats": (
        "Zapisuje aktualną liczbę książek do pliku statystyk.",
        "Writes the current book count to the statistics file.",
    ),
    "log_request": (
        "Middleware otacza obsługę żądania: mierzy czas, nadaje ID i zapisuje log.",
        "Middleware wraps request handling: measures time, assigns an ID and writes a log.",
    ),
    "append_log": (
        "Dopisuje jeden wiersz JSON do pliku dziennika.",
        "Appends one JSON line to the request log.",
    ),
    "lifespan": (
        "Kod przed yield uruchamia zasoby; kod w finally zapisuje cache przy zamykaniu aplikacji.",
        "Code before yield starts resources; finally saves cache when the application closes.",
    ),
    "get_cache": (
        "Odczytuje współdzielony cache ze stanu tej aplikacji.",
        "Reads this application’s shared cache.",
    ),
    "put_cache": (
        "Zmienia wartość cache wskazaną przez klucz ze ścieżki.",
        "Changes the cache value identified by the path key.",
    ),
    "get_actor": (
        "Rozpoznaje użytkownika przez jawny klucz demonstracyjny i osobną sesję odczytu.",
        "Identifies a user using an explicit demo key and a separate read session.",
    ),
    "post_data": (
        "Zamienia obiekt Post na zwykły słownik gotowy do JSON.",
        "Converts a Post object into a plain JSON-ready dictionary.",
    ),
    "notify_author": (
        "Zapisuje lokalny ślad powiadomienia zamiast wysyłać prawdziwy email.",
        "Records a local notification instead of sending real email.",
    ),
    "create_post": (
        "Przypisuje nowy post do użytkownika ustalonego przez dependency.",
        "Assigns the new post to the user resolved by the dependency.",
    ),
    "list_posts": (
        "Odczytuje posty w stabilnej kolejności ID.",
        "Reads posts in stable ID order.",
    ),
    "get_post": (
        "Odczytuje post po ID lub zwraca 404.",
        "Reads a post by ID or returns 404.",
    ),
    "replace_post": (
        "Przed zmianą posta porównuje ID autora z ID rozpoznanego użytkownika.",
        "Compares author ID with the authenticated user ID before editing.",
    ),
    "delete_post": (
        "Usuwa post wyłącznie na żądanie jego autora.",
        "Deletes a post only when requested by its author.",
    ),
    "add_comment": (
        "Zapisuje komentarz, następnie planuje powiadomienie i ewentualną analizę w tle.",
        "Saves a comment, then schedules notification and optional analysis in the background.",
    ),
    "post_with_comments": (
        "Pobiera post wraz z komentarzami przez selectinload i zwraca zagnieżdżony JSON.",
        "Fetches a post and comments with selectinload and returns nested JSON.",
    ),
    "analyze_sentiment": (
        "Przypisuje sentyment prostą regułą słów great/bad. To jawna symulacja, nie model AI.",
        "Assigns sentiment using the words great/bad. This is an explicit simulation, not an AI model.",
    ),
    "summarize": (
        "Zwraca pierwsze 12 słów posta jako lokalną symulację podsumowania.",
        "Returns the first 12 post words as a local summary simulation.",
    ),
    "moderate": (
        "Middleware odczytuje body i odrzuca demonstracyjnie zabronione słowo przed endpointem.",
        "Middleware reads the body and rejects a demo forbidden word before the endpoint.",
    ),
    "conflict": (
        "Zamienia konflikt ograniczeń bazy, np. powtórzoną nazwę, na odpowiedź 409.",
        "Converts a database constraint conflict, such as a duplicate name, into response 409.",
    ),
}


CALLS = {
    "EmailStr": (
        "Typ Pydantic sprawdza składnię adresu email. Nie wysyła wiadomości i nie potwierdza istnienia skrzynki.",
        "This Pydantic type checks email syntax. It neither sends email nor verifies mailbox existence.",
    ),
    "FastAPI": (
        "Tworzy aplikację; lifespan określa start i zamknięcie zasobów, a metadane opisują dokumentację.",
        "Creates the application; lifespan defines resource startup/shutdown, while metadata describes the docs.",
    ),
    "APIRouter": (
        "Tworzy grupę tras ze wspólnym prefiksem i tagiem.",
        "Creates a route group with a shared prefix and tag.",
    ),
    "Field": (
        "Określa reguły pola, np. długość tekstu, zakres liczby i przykłady do dokumentacji.",
        "Defines field rules such as text length, number bounds and documentation examples.",
    ),
    "Query": (
        "Pobiera parametr query i ustala wartość domyślną oraz granice walidacji.",
        "Reads a query parameter and defines its default and validation bounds.",
    ),
    "Path": (
        "Definiuje walidację parametru pochodzącego z fragmentu URL.",
        "Defines validation for a parameter captured from the URL path.",
    ),
    "Depends": (
        "Zleca FastAPI wywołanie dependency przed endpointem i przekazanie jej wyniku.",
        "Asks FastAPI to call a dependency before the endpoint and pass its result.",
    ),
    "Header": (
        "Pobiera nagłówek HTTP; x_api_key odpowiada nazwie X-API-Key.",
        "Reads an HTTP header; x_api_key corresponds to X-API-Key.",
    ),
    "ConfigDict": (
        "from_attributes=True pozwala modelowi odpowiedzi czytać atrybuty obiektu ORM.",
        "from_attributes=True lets response models read ORM object attributes.",
    ),
    "database_lifespan": (
        "Pomocnik tworzy osobny schemat PostgreSQL, tabele i fabrykę sesji; po pokazie zamyka je i usuwa schemat.",
        "The helper creates a separate PostgreSQL schema, tables and session factory, then closes them and removes the schema after the demo.",
    ),
    "model_dump": (
        "Zamienia zwalidowany model Pydantic na słownik. ** rozpakowuje jego klucze jako argumenty lub pola nowego słownika.",
        "Converts a validated Pydantic model to a dictionary. ** unpacks keys as arguments or dictionary fields.",
    ),
    "select": (
        "Buduje opis SELECT, jeszcze bez komunikacji z bazą.",
        "Builds a SELECT description without contacting the database yet.",
    ),
    "execute": (
        "Wysyła zapytanie do bazy; await czeka na wynik, oddając sterowanie pętli zdarzeń.",
        "Sends the query to the database; await waits for its result while yielding to the event loop.",
    ),
    "get": (
        "Pobiera wartość po kluczu. W db.get(Model, id) odczytuje rekord po kluczu głównym; brak wyniku daje None.",
        "Looks up a key. db.get(Model, id) retrieves a primary-key row; absence returns None.",
    ),
    "add": (
        "Dołącza obiekt ORM do sesji. Nie wykonuje jeszcze INSERT i nie potrzebuje await.",
        "Adds an ORM object to the session. It does not execute INSERT yet and needs no await.",
    ),
    "flush": (
        "Wysyła oczekujące INSERT/UPDATE i pobiera wygenerowane ID. To jeszcze nie commit; wyjątek nadal może wycofać zapis.",
        "Sends pending INSERT/UPDATE statements and retrieves generated IDs. This is not commit; an exception can still roll back the write.",
    ),
    "delete": (
        "Oznacza obiekt ORM do usunięcia; transakcja zatwierdzi DELETE przy poprawnym wyjściu.",
        "Marks an ORM object for deletion; the transaction commits DELETE on successful exit.",
    ),
    "begin": (
        "Otwiera zakres transakcji: normalne wyjście zatwierdza, wyjątek uruchamia rollback.",
        "Opens a transaction scope: successful exit commits; an exception triggers rollback.",
    ),
    "scalars": (
        "Wyciąga obiekty modelu z wierszy wyniku SELECT.",
        "Extracts model objects from SELECT result rows.",
    ),
    "all": (
        "Zbiera dostępne elementy wyniku do listy.",
        "Collects available result items into a list.",
    ),
    "scalar_one_or_none": (
        "Zwraca jeden obiekt albo None. Więcej niż jeden wynik jest błędem.",
        "Returns one object or None. Multiple results are an error.",
    ),
    "selectinload": (
        "Pobiera relację osobnym zbiorczym SELECT; zapobiega leniwemu I/O przy późniejszym czytaniu kolekcji.",
        "Loads a relationship with a separate batched SELECT, avoiding lazy I/O when the collection is accessed later.",
    ),
    "relationship": (
        "Definiuje powiązanie obiektów ORM; back_populates wskazuje drugą stronę relacji.",
        "Defines an ORM object relationship; back_populates identifies its other side.",
    ),
    "ForeignKey": (
        "Łączy kolumnę z kluczem innej tabeli; ondelete=CASCADE usuwa zależne rekordy w bazie.",
        "Links a column to another table’s key; ondelete=CASCADE deletes dependent database rows.",
    ),
    "mapped_column": (
        "Definiuje kolumnę SQL. Mapped opisuje typ atrybutu ORM, a primary_key oznacza klucz główny.",
        "Defines an SQL column. Mapped describes the ORM attribute type; primary_key marks the primary key.",
    ),
    "where": (
        "Dodaje warunek SQL. Wartości są przekazywane jako parametry, bez składania SQL z wejścia klienta.",
        "Adds an SQL condition. Values are bound as parameters rather than concatenated into SQL.",
    ),
    "order_by": (
        "Ustala kolejność; dodatkowe ID rozstrzyga remisy przy sortowaniu i paginacji.",
        "Defines order; an extra ID resolves ties for sorting and pagination.",
    ),
    "offset": (
        "Określa liczbę rekordów pomijanych przed stroną wyników.",
        "Sets how many rows to skip before the result page.",
    ),
    "limit": (
        "Ogranicza maksymalną liczbę pobranych rekordów.",
        "Bounds the maximum number of retrieved rows.",
    ),
    "include_router": (
        "Rejestruje trasy osobnego routera w aplikacji. Funkcje endpointów nie są jeszcze wywoływane.",
        "Registers another router’s routes in the application. Endpoints do not run yet.",
    ),
    "add_task": (
        "Planuje wykonanie funkcji po wysłaniu odpowiedzi. Przekazujemy funkcję bez (), a dalej jej argumenty.",
        "Schedules a function after the response is sent. Pass the function without (), followed by its arguments.",
    ),
    "HTTPException": (
        "Przerywa endpoint odpowiedzią o podanym statusie i detail; dalsze instrukcje tej gałęzi nie wykonają się.",
        "Stops the endpoint with the given status and detail; remaining statements in this branch do not run.",
    ),
    "JSONResponse": (
        "Tworzy odpowiedź JSON z jawnie ustawionym statusem, np. 409 przy konflikcie.",
        "Creates a JSON response with an explicit status, such as 409 for conflicts.",
    ),
    "Response": (
        "Tworzy odpowiedź HTTP. Przy 204 body musi pozostać puste.",
        "Creates an HTTP response. Status 204 must have an empty body.",
    ),
    "call_next": (
        "Przekazuje żądanie do kolejnego middleware lub endpointu i czeka na odpowiedź.",
        "Passes the request to the next middleware or endpoint and awaits its response.",
    ),
    "body": (
        "Odczytuje body żądania jako bytes. W tym middleware sprawdzamy treść przed endpointem.",
        "Reads the request body as bytes. This middleware checks content before the endpoint.",
    ),
    "to_thread": (
        "Wykonuje blokującą operację plikową w osobnym wątku, aby nie blokować event loop.",
        "Runs blocking file work in another thread rather than blocking the event loop.",
    ),
    "runtime_file": (
        "Zwraca ścieżkę w osobnym katalogu danych tego pokazu. Nie zapisujemy w plikach kursu ani w danych innych lekcji.",
        "Returns a path in this demo’s own data directory. Course sources and other lessons’ data are not modified.",
    ),
    "open": (
        "Otwiera plik; tryb a dopisuje dane. with dopilnuje zamknięcia uchwytu.",
        "Opens a file; mode a appends data. with ensures the handle closes.",
    ),
    "write": (
        "Zapisuje tekst do otwartego pliku; \\n oddziela wpisy dziennika.",
        "Writes text to an open file; \\n separates log records.",
    ),
    "write_text": (
        "Zastępuje zawartość pliku podanym tekstem i kodowaniem UTF-8.",
        "Replaces file contents with the supplied text using UTF-8.",
    ),
    "read_text": (
        "Odczytuje zawartość pliku jako tekst; kodowanie określamy jawnie.",
        "Reads file contents as text with an explicit encoding.",
    ),
    "loads": (
        "Parsuje tekst JSON do obiektu Pythona.",
        "Parses JSON text into a Python object.",
    ),
    "dumps": (
        "Koduje obiekt Pythona jako tekst JSON do zapisu w pliku.",
        "Encodes a Python object as JSON text for file storage.",
    ),
    "perf_counter": (
        "Odczytuje zegar monotoniczny do pomiaru czasu trwania; różnica dwóch odczytów daje sekundy.",
        "Reads a monotonic duration clock; subtracting readings gives seconds.",
    ),
    "uuid4": (
        "Tworzy losowy identyfikator żądania; hex zamienia go na tekst.",
        "Creates a random request ID; hex converts it to text.",
    ),
    "compare_digest": (
        "Porównuje klucz z wartością demonstracyjną metodą przeznaczoną do porównań sekretów.",
        "Compares the key with the demo value using a secret-comparison method.",
    ),
    "isalnum": (
        "Sprawdza niepusty tekst złożony tylko z liter i cyfr; spacje i interpunkcja są odrzucane.",
        "Checks nonempty text containing only letters and digits; spaces and punctuation are rejected.",
    ),
    "split": (
        "Dzieli tekst na słowa; [:12] wybiera pierwszych dwanaście w symulacji podsumowania.",
        "Splits text into words; [:12] selects the first twelve in the summary simulation.",
    ),
    "join": (
        "Łączy słowa separatorem; tutaj odtwarza krótki tekst podsumowania.",
        "Joins words using a separator; here it rebuilds the short summary.",
    ),
    "lower": (
        "Zamienia litery na małe przed prostym porównaniem treści.",
        "Lowercases letters before a simple content comparison.",
    ),
    "values": (
        "Zwraca wartości słownika books; list(...) zbiera je do listy odpowiedzi.",
        "Returns books dictionary values; list(...) collects them into a response list.",
    ),
    "randint": (
        "Losuje liczbę całkowitą pomiędzy obiema podanymi granicami, włącznie.",
        "Draws an integer between both supplied inclusive bounds.",
    ),
    "now": (
        "Odczytuje czas; timezone.utc nadaje mu jawną strefę UTC.",
        "Reads time; timezone.utc gives it an explicit UTC timezone.",
    ),
    "isoformat": (
        "Zamienia datę na tekst ISO możliwy do zapisania w JSON.",
        "Converts a date to ISO text suitable for JSON.",
    ),
    "Lock": (
        "Tworzy blokadę dla korutyn; zabezpiecza wspólne dopisywanie do pliku dziennika.",
        "Creates a coroutine lock protecting shared log-file writes.",
    ),
    "len": (
        "Zwraca liczbę elementów lub bajtów. W zależności od argumentu jest to liczba książek albo rozmiar body.",
        "Returns the element or byte count: number of books or body size, depending on the argument.",
    ),
    "list": (
        "Zbiera elementy do nowej listy, którą FastAPI może zakodować jako JSON.",
        "Collects elements into a new list that FastAPI can encode as JSON.",
    ),
    "event": (
        "Zapisuje rzeczywiste zdarzenie widoczne w panelu pokazu; nie zmienia danych biznesowych.",
        "Records a real event in the demo panel without changing business data.",
    ),
    "String": (
        "Określa typ tekstowej kolumny i maksymalną długość w bazie.",
        "Defines a text column type and maximum database length.",
    ),
    "exists": (
        "Sprawdza, czy plik cache już istnieje; przy braku zaczynamy od pustego słownika.",
        "Checks whether the cache file exists; otherwise start with an empty dictionary.",
    ),
}


def call_notes(node):
    result = []
    seen = set()
    for call in sorted(
        (n for n in ast.walk(node) if isinstance(n, ast.Call)),
        key=lambda n: (n.lineno, n.col_offset),
    ):
        name = ast.unparse(call.func).rsplit(".", 1)[-1]
        if name in CALLS and name not in seen:
            seen.add(name)
            result.append(CALLS[name])
    return result


def statement_note(node, source):
    text = ast.get_source_segment(source, node) or ""
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        names = ", ".join(alias.name for alias in node.names)
        return pair(
            f"Import udostępnia nazwy: {names}. Biblioteki obsługują HTTP, walidację, bazę lub przygotowanie pokazu; moduły lokalne dzielą rozwiązanie na części. Import przygotowuje definicje, nie wykonuje endpointu.",
            f"Import exposes: {names}. Libraries provide HTTP, validation, database or demo support; local modules split the solution. Imports prepare definitions without executing an endpoint.",
        )
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        pl, en = FUNCTIONS[node.name]
        mechanisms = call_notes(node.args)
        return pair(
            (
                "Definiujemy korutynę. "
                if isinstance(node, ast.AsyncFunctionDef)
                else "Definiujemy zwykłą funkcję. "
            )
            + pl
            + " Parametry opisują dane wejściowe; samo zdefiniowanie funkcji nie uruchamia jej ciała. "
            + " ".join(item[0] for item in mechanisms),
            (
                "Define a coroutine. "
                if isinstance(node, ast.AsyncFunctionDef)
                else "Define an ordinary function. "
            )
            + en
            + " Parameters describe inputs; defining the function does not run its body. "
            + " ".join(item[1] for item in mechanisms),
        )
    if isinstance(node, ast.ClassDef):
        bases = ", ".join(ast.unparse(b) for b in node.bases)
        return pair(
            f"Klasa {node.name} dziedziczy po {bases}. BaseModel definiuje dane wejściowe/wyjściowe Pydantic; Base lub DeclarativeBase dotyczą tabel ORM. Tych dwóch rodzajów modeli nie należy utożsamiać.",
            f"{node.name} inherits {bases}. BaseModel defines Pydantic input/output data; Base or DeclarativeBase defines ORM tables. These are different kinds of models.",
        )
    if isinstance(node, ast.Return):
        lead = pair(
            "return kończy funkcję i oddaje podaną wartość. W endpoincie FastAPI koduje ją jako odpowiedź zgodnie z response_model lub typem wyniku.",
            "return ends the function and returns its value. In an endpoint FastAPI encodes it according to response_model or the result type.",
        )
    elif isinstance(node, (ast.With, ast.AsyncWith)):
        lead = pair(
            "Wchodzimy do zarządzanego bloku. Wcięte instrukcje należą do tego zakresu, a wyjście dopilnuje zamknięcia pliku, sesji, transakcji lub zwolnienia blokady.",
            "Enter a managed block. Indented statements belong to its scope; exiting closes files, sessions, transactions or releases a lock.",
        )
    elif isinstance(node, ast.If):
        condition = ast.unparse(node.test)
        lead = pair(
            f"Sprawdzamy warunek `{condition}`. Jeśli jest prawdziwy, wykonamy wciętą gałąź; w przeciwnym przypadku przejdziemy do else/elif albo dalej. Warunek może zatrzymać niepoprawne żądanie przed zmianą danych.",
            f"Check `{condition}`. If true, execute the indented branch; otherwise continue to else/elif or the next statement. Conditions may stop invalid requests before data changes.",
        )
    elif isinstance(node, ast.Raise):
        lead = pair(
            "raise przerywa bieżący przebieg. HTTPException stanie się odpowiedzią błędu; ValueError wewnątrz walidatora stanie się błędem walidacji 422. W transakcji wyjątek powoduje rollback.",
            "raise interrupts execution. HTTPException becomes an error response; ValueError in a validator becomes validation error 422. An exception inside a transaction triggers rollback.",
        )
    elif isinstance(node, ast.AnnAssign):
        target = ast.unparse(node.target)
        annotation = ast.unparse(node.annotation)
        lead = pair(
            f"Pole `{target}` ma deklarowany typ `{annotation}`. W Pydantic ta deklaracja służy walidacji i dokumentacji; Mapped opisuje atrybut ORM. Brak wartości domyślnej w BaseModel oznacza pole wymagane.",
            f"Field `{target}` declares type `{annotation}`. Pydantic uses it for validation and docs; Mapped describes an ORM attribute. No default in BaseModel means a required field.",
        )
    elif isinstance(node, ast.Assign):
        targets = ", ".join(ast.unparse(t) for t in node.targets)
        lead = pair(
            f"Obliczamy prawą stronę i przypisujemy wynik do `{targets}`. Zmienna zachowuje ten wynik do następnych instrukcji; przypisanie atrybutu obiektu ORM zostanie wykryte przez sesję.",
            f"Evaluate the right-hand side and assign it to `{targets}`. The variable retains the value for subsequent statements; assigning ORM attributes is tracked by the session.",
        )
    elif isinstance(node, ast.AugAssign):
        lead = pair(
            "Aktualizujemy istniejącą wartość. next_id += 1 zwiększa licznik identyfikatorów; usunięcie książki nie cofa licznika, więc ID nie zostanie przypadkowo ponownie użyte.",
            "Update an existing value. next_id += 1 increments the ID counter; deleting a book does not rewind it, avoiding accidental ID reuse.",
        )
    elif isinstance(node, ast.Delete):
        lead = pair(
            "del usuwa wpis ze słownika books. To zmiana w pamięci tego procesu; restart aplikacji odtworzy pusty słownik.",
            "del removes an entry from books. This changes only process memory; restarting restores an empty dictionary.",
        )
    elif isinstance(node, ast.Global):
        lead = pair(
            "global next_id oznacza, że przypisanie w funkcji zmieni licznik na poziomie modułu, zamiast tworzyć zmienną lokalną.",
            "global next_id makes assignment update the module-level counter rather than create a local variable.",
        )
    elif isinstance(node, ast.Try):
        return pair(
            "try wyznacza zakres pracy aplikacji. finally uruchomi zapis cache także wtedy, gdy aplikacja wyjdzie przez wyjątek podczas normalnego zamykania.",
            "try defines the application work scope. finally saves the cache even when normal shutdown unwinds through an exception.",
        )
    elif isinstance(node, ast.Pass):
        return pair(
            "pass to pusta instrukcja wymagana jako ciało klasy Base. Rejestr modeli i metadata pochodzą z klasy bazowej.",
            "pass is the empty body of Base. The model registry and metadata come from its parent class.",
        )
    elif (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    ):
        return pair(
            "Docstring opisuje działanie endpointu. FastAPI może wykorzystać go w automatycznej dokumentacji; nie jest wykonywalną instrukcją biznesową.",
            "The docstring describes the endpoint. FastAPI can use it in automatic documentation; it is not executable business logic.",
        )
    elif isinstance(node, ast.Expr) and isinstance(
        node.value, (ast.Yield, ast.YieldFrom)
    ):
        return pair(
            "yield rozdziela lifespan na start i zamknięcie. Przed yield przygotowujemy zasoby; podczas zawieszenia działa aplikacja; finally wykona sprzątanie.",
            "yield splits lifespan into startup and shutdown. Prepare resources before yield; the application runs while suspended; finally performs cleanup.",
        )
    else:
        lead = pair(
            "Wykonujemy wskazane wywołanie. Przy await bieżąca korutyna czeka na wynik operacji, a pętla może obsługiwać inne gotowe żądania.",
            "Execute this call. With await the current coroutine waits for its result while the loop can serve other ready requests.",
        )
    # Only analyze the header/expression of this statement, not nested function bodies.
    own = node
    if isinstance(node, (ast.If, ast.With, ast.AsyncWith)):
        own = (
            node.test
            if isinstance(node, ast.If)
            else ast.Tuple(
                elts=[item.context_expr for item in node.items], ctx=ast.Load()
            )
        )
    notes = call_notes(own)
    return pair(
        lead["pl"] + " " + " ".join(n[0] for n in notes),
        lead["en"] + " " + " ".join(n[1] for n in notes),
    )


def detailed_steps(file, source):
    tree = ast.parse(source)
    steps = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.stmt):
            continue
        start = node.lineno
        end = node.end_lineno
        if isinstance(
            node,
            (
                ast.ClassDef,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.With,
                ast.AsyncWith,
                ast.If,
                ast.Try,
            ),
        ):
            end = node.body[0].lineno - 1
            end = max(start, end)
        labels = {
            "Import": "Import / Import",
            "ImportFrom": "Import / Import",
            "Assign": "Przypisanie / Assignment",
            "AnnAssign": "Pole i typ / Field and type",
            "Return": "Wynik / Return",
            "If": "Warunek / Condition",
            "Raise": "Błąd / Error",
            "AsyncWith": "Zakres async with / Async context",
            "With": "Zakres with / Context",
            "Expr": "Wywołanie / Expression",
            "Try": "Sprzątanie / Cleanup",
            "Global": "Zmienna modułu / Module variable",
            "Delete": "Usuwanie / Deletion",
            "AugAssign": "Aktualizacja / Update",
            "Pass": "Puste ciało / Empty body",
        }
        name = getattr(
            node, "name", labels.get(type(node).__name__, type(node).__name__)
        )
        for decorator in getattr(node, "decorator_list", []):
            expression = ast.unparse(decorator)
            if expression.endswith("classmethod"):
                note = pair(
                    "classmethod przekazuje klasę jako cls do walidatora; walidacja nie potrzebuje jeszcze gotowego obiektu modelu.",
                    "classmethod passes the class as cls; validation does not need an existing model instance.",
                )
            elif expression == "asynccontextmanager":
                note = pair(
                    "Dekorator pozwala używać funkcji z yield jako menedżera async with. Start i zamknięcie zasobów należą do jednego zakresu.",
                    "This decorator turns a yield function into an async with context manager. Resource startup and shutdown share one scope.",
                )
            elif expression.startswith("field_validator"):
                note = pair(
                    "Rejestrujemy własną regułę dla pola name. FastAPI uruchomi ją podczas walidacji modelu, zanim wywoła endpoint.",
                    "Register a custom rule for name. FastAPI runs it while validating the model, before calling the endpoint.",
                )
            elif ".middleware(" in expression:
                note = pair(
                    "Rejestrujemy middleware HTTP. Wykona kod przed endpointem, a po await call_next może zmienić nagłówki i zapisać pomiar.",
                    "Register HTTP middleware. It runs before the endpoint, then can alter headers and record timing after await call_next.",
                )
            elif ".exception_handler(" in expression:
                note = pair(
                    "Rejestrujemy zamianę wskazanego wyjątku na czytelną odpowiedź HTTP zamiast nieobsłużonego błędu serwera.",
                    "Register conversion of this exception into a readable HTTP response instead of an unhandled server error.",
                )
            else:
                note = pair(
                    f"Dekorator `{expression}` łączy metodę HTTP i ścieżkę z funkcją poniżej. response_model ustala kształt wyjścia, status_code status sukcesu, a tags grupuje dokumentację. Rejestracja nie wykonuje handlera.",
                    f"Decorator `{expression}` binds an HTTP method and path to the function below. response_model defines output, status_code the success status, and tags documentation grouping. Registration does not execute the handler.",
                )
            steps.append(
                dict(
                    file=file,
                    start=decorator.lineno,
                    end=decorator.end_lineno,
                    name="Dekorator / Decorator",
                    body=note,
                    details=[],
                )
            )
        steps.append(
            dict(
                file=file,
                start=start,
                end=end,
                name=f"L{start} · {name}",
                body=statement_note(node, source),
                details=[],
            )
        )
    return sorted(steps, key=lambda step: (step["start"], step["end"]))
