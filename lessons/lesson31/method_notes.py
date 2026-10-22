"""Reviewed API explanations: arguments, return values and common mistakes."""

METHODS = {
    "asyncio.sleep": (
        "Czas oczekiwania w sekundach; może być ułamkiem. Tworzy korutynę, która po await oddaje sterowanie pętli do czasu wznowienia. Nie blokuje wątku tak jak time.sleep. Zwykle zwraca None. Usunięcie await pozostawi niewykonaną korutynę.",
        "Takes a delay in seconds, including fractions. Creates a coroutine that yields to the loop when awaited until resumption. Unlike time.sleep it does not block the thread. Usually returns None. Omitting await leaves an unexecuted coroutine."),
    "asyncio.gather": (
        "Przyjmuje oddzielne obiekty awaitable: gather(a(), b()). Surowe korutyny planuje jako zadania. Po await daje listę wyników w kolejności argumentów, a nie zakończeń. *lista rozpakowuje listę na oddzielne argumenty. Domyślnie pierwszy wyjątek trafia do oczekującego; pozostałe operacje nie są przez to automatycznie anulowane. return_exceptions=True zbiera także wyjątki jako wyniki.",
        "Accepts separate awaitables: gather(a(), b()). Schedules raw coroutines as tasks. Awaiting returns a result list in argument order, not completion order. *items unpacks a list into arguments. By default the first exception propagates without automatically cancelling the other operations. return_exceptions=True collects exceptions as results too."),
    "asyncio.create_task": (
        "Argument to obiekt korutyny, np. worker(), nie sama nazwa worker. Zwraca Task: uchwyt do zaplanowanej pracy. Zachowujemy go, aby odebrać wynik przez await albo poprosić o cancel. W domyślnym trybie przykładu praca ruszy, gdy bieżąca korutyna odda sterowanie pętli. Samo utworzenie Task nie czeka na wynik.",
        "Takes a coroutine object such as worker(), not the name worker. Returns a Task handle to scheduled work. Retain it to await its result or request cancel. With the default scheduling used here, work starts when the current coroutine yields to the loop. Creating a Task does not wait for its result."),
    "asyncio.wait": (
        "Dostaje kolekcję Task i zwraca po await parę zbiorów (done, pending). FIRST_COMPLETED oznacza powrót, kiedy co najmniej jedno zadanie się zakończy lub zostanie anulowane. wait samo nie anuluje pending i nie zwraca listy wartości return. Wyniki done odbieramy osobno.",
        "Takes a collection of Tasks and yields two sets (done, pending). FIRST_COMPLETED returns when at least one completes or is cancelled. wait does not cancel pending tasks or return their values. Retrieve done results separately."),
    "asyncio.wait_for": (
        "Pierwszy argument to operacja awaitable, timeout to liczba sekund. await zwraca jej wynik, jeśli zdąży. Po przekroczeniu czasu prosi o anulowanie i zgłasza TimeoutError po zakończeniu anulowania. Dlatego czas ścienny może być dłuższy od limitu. Timeout obsługujemy w except.",
        "The first argument is an awaitable; timeout is seconds. await returns its result if ready in time. On expiry it requests cancellation and raises TimeoutError after cancellation completes, so elapsed time can exceed the limit. Handle expiry in except."),
    "asyncio.Lock": (
        "Bez argumentów tworzy jedną blokadę do współpracy korutyn tej samej pętli. async with lock czeka na jej zdobycie i zwalnia ją po wyjściu, również przy błędzie. Wszystkie chronione operacje muszą używać tego samego obiektu Lock. To nie blokada do synchronizacji wątków systemowych.",
        "Creates a lock for coroutines in one event loop. async with lock awaits acquisition and releases on exit, even on errors. All protected operations must share the same Lock object. It is not an OS thread synchronization lock."),
    "asyncio.Queue": (
        "maxsize to maksymalna liczba elementów oczekujących w kolejce. Tworzy kolejkę FIFO. put dodaje, get odbiera, task_done potwierdza obsługę, join czeka na wszystkie potwierdzenia. Ograniczona kolejka spowalnia producenta, gdy jest pełna.",
        "maxsize limits waiting items. Creates a FIFO queue: put adds, get removes, task_done acknowledges processing, join waits for all acknowledgements. A bounded queue slows producers when full."),
    "queue.put": (
        "Argument to pojedynczy element. await dodaje go do kolejki, czekając na miejsce, gdy jest pełna. Zwraca None. Tutaj liczba to praca, a None jest umówionym sygnałem końca dla jednego konsumenta.",
        "Takes one item. Awaiting adds it, waiting if the queue is full. Returns None. Here numbers are work; None is the agreed shutdown marker for one consumer."),
    "queue.get": (
        "Nie ma argumentów. await czeka, aż pojawi się element, usuwa go z kolejki i zwraca. Nie potwierdza przetworzenia: po obsłudze trzeba task_done. Dwa get nie odbiorą tego samego wpisu.",
        "Takes no arguments. await waits for an item, removes and returns it. This does not acknowledge processing: call task_done afterwards. Two get calls do not receive the same entry."),
    "queue.task_done": (
        "Bez await i argumentów zmniejsza licznik niepotwierdzonych elementów. Wywołujemy dokładnie raz po każdym get, również po sygnale None. Zbyt mało potwierdzeń zawiesi join; zbyt dużo spowoduje ValueError.",
        "Without await or arguments, decreases the unfinished-item count. Call exactly once per get, including None markers. Too few acknowledgements leave join waiting; too many raise ValueError."),
    "queue.join": (
        "await czeka, aż każdy dodany przez put element otrzyma task_done. Zwraca None. Pusta kolejka nie wystarcza: konsument mógł już odebrać element i nadal go przetwarzać.",
        "await waits until every put item has a matching task_done and returns None. An empty queue is insufficient: a consumer may have taken an item and still be processing it."),
    "task.cancel": (
        "Bez await prosi o anulowanie Task. Zwraca informację, czy żądanie mogło zostać przyjęte. Nie czeka na sprzątanie i nie gwarantuje anulowania: korutyna może przechwycić wyjątek. Następnie await task pozwala odebrać końcowy stan.",
        "Without await, requests Task cancellation. Returns whether the request could be accepted. Does not wait for cleanup or guarantee cancellation: the coroutine can catch the exception. Await the Task afterwards to observe its final outcome."),
    "task.result": (
        "Bez await odbiera wynik już zakończonego Task. Gdy praca trwa, zgłasza InvalidStateError; gdy zawiodła, ponownie zgłasza jej wyjątek. Używamy dopiero dla elementów done.",
        "Without await, retrieves an already completed Task's result. Raises InvalidStateError if unfinished, or propagates the task exception if it failed. Used only for done tasks here."),
    "task.cancelled": (
        "Zwraca bool: True, jeżeli zadanie rzeczywiście zakończyło się przez anulowanie. Samo wcześniejsze wywołanie cancel nie wystarcza do True.",
        "Returns True only if the task actually finished by cancellation. Merely calling cancel earlier does not guarantee True."),
    "asyncio.get_running_loop": (
        "Zwraca pętlę zdarzeń działającą w bieżącym wątku. Wywołujemy w korutynie; poza działającą pętlą zgłasza RuntimeError. Nie tworzy nowej pętli.",
        "Returns the event loop running in this thread. Called from a coroutine; raises RuntimeError outside a running loop. Does not create a new loop."),
    "loop.time": (
        "Zwraca liczbę sekund monotonicznego zegara pętli. Odejmowanie dwóch odczytów daje upływ czasu. Nie jest to data ani godzina, więc nie wyświetlamy jej jako czasu kalendarzowego.",
        "Returns seconds from the loop's monotonic clock. Subtract readings to measure intervals. It is not a calendar date or time."),
    "asyncio.start_server": (
        "Argumenty: funkcja obsługi klienta, adres i port. await zwraca obiekt Server. Dla nowego połączenia funkcja dostaje StreamReader i StreamWriter. Port 0 zleca systemowi wybór wolnego portu. Nasłuchiwanie zamykamy przez async with server.",
        "Takes a client handler, host and port. await returns a Server. Each new connection supplies StreamReader and StreamWriter to the handler. Port 0 lets the OS choose a free port. async with server closes listening on exit."),
    "asyncio.open_connection": (
        "Adres i port określają serwer TCP. await tworzy połączenie i zwraca parę (reader, writer). Przypisanie do dwóch zmiennych rozpakowuje tę parę. Po użyciu trzeba zamknąć writer.",
        "Host and port identify a TCP server. await connects and returns (reader, writer). Assignment to two variables unpacks this pair. Close writer after use."),
    "reader.readline": (
        "await czeka na jedną linię bajtów zakończoną \\n lub na koniec strumienia. Zwraca bytes, nie str. Gdy klient nie wyśle nowej linii ani nie zamknie połączenia, odczyt może czekać — dlatego klient ma timeout.",
        "await waits for bytes through a newline or end of stream. Returns bytes, not str. Without a newline or connection close, reading can wait, so the client uses a timeout."),
    "writer.write": (
        "Przyjmuje bytes i przekazuje je do bufora wyjściowego TCP. Nie używamy await przy write. Potem await drain obsługuje kontrolę przepływu, gdy bufor się zapełnia.",
        "Takes bytes and buffers TCP output. Do not await write. Follow with await drain for flow control when the buffer fills."),
    "writer.drain": (
        "await czeka na możliwość dalszego pisania zgodnie z kontrolą przepływu. Nie zwraca wiadomości i nie potwierdza, że aplikacja po drugiej stronie ją przetworzyła.",
        "await waits until flow control permits further writing. Returns no message and does not confirm that the peer application processed the data."),
    "writer.close": (
        "Rozpoczyna zamykanie strumienia bez await. Następnie await writer.wait_closed() czeka, aż zamknięcie się zakończy. finally gwarantuje wykonanie również po błędzie.",
        "Starts closing the stream without await. Then await writer.wait_closed() waits for closing to finish. finally ensures execution even on errors."),
    "writer.wait_closed": (
        "await czeka na zakończenie zamykania writer. Wywołujemy po close; nie zastępuje samego close.",
        "await waits for writer closing to finish. Call after close; it does not replace close itself."),
    "aiohttp.ClientSession": (
        "Tworzy sesję z pulą połączeń. timeout ustala ograniczenia żądań. async with zamyka sesję po bloku. Sesję współdzielimy między żądaniami jednej pętli, zamiast tworzyć ją osobno dla każdego URL.",
        "Creates a session with a connection pool. timeout bounds requests. async with closes the session. Share it across requests in one loop instead of recreating it per URL."),
    "aiohttp.ClientTimeout": (
        "total=3 ustala łączny limit żądania na trzy sekundy. Zwraca obiekt konfiguracji, nie uruchamia połączenia. Przekazujemy go do ClientSession.",
        "total=3 sets a three-second overall request limit. Returns configuration without making a connection. Passed into ClientSession."),
    "session.get": (
        "Argument URL jest adresem żądania GET. async with czeka na odpowiedź i potem ją zwalnia. response.status odczytuje liczbę statusu. 404 nie wywoła automatycznie wyjątku bez raise_for_status.",
        "The URL identifies a GET request. async with awaits and then releases its response. response.status reads the numeric status. 404 does not automatically raise without raise_for_status."),
    "aiofiles.open": (
        "Argumenty: ścieżka, tryb (a: dopisywanie, domyślnie r: odczyt), encoding. async with otwiera i zamyka plik. Operacje dyskowe są delegowane do puli wątków, aby nie blokować pętli zdarzeń.",
        "Takes path, mode (a appends, default r reads) and encoding. async with opens and closes the file. Disk operations are delegated to a thread pool to avoid blocking the event loop."),
    "output.write": (
        "Argumentem jest tekst do zapisania. W aiofiles używamy await. Dopisujemy znak \\n, aby każdy wpis był osobnym wierszem. W tym przykładzie wspólny Lock obejmuje także zamknięcie pliku.",
        "Takes text to write. With aiofiles, use await. Append a newline for separate records. Here the shared Lock also covers closing the file."),
    "source.read": (
        "Bez argumentu odczytuje całą zawartość. await daje str, ponieważ plik otwarto tekstowo z encoding=utf-8. Przy wielkich plikach lepiej czytać częściami.",
        "Without a size, reads the entire contents. await returns str because the file uses text mode with UTF-8 encoding. Read large files in chunks."),
    "range": (
        "range(stop) daje liczby od 0 bez stop. range(start,stop,step) zaczyna od start i zmienia liczbę o step. Granica stop zawsze jest wyłączona. Zwraca obiekt zakresu; for bierze z niego kolejne wartości.",
        "range(stop) yields from 0 excluding stop. range(start,stop,step) starts at start and advances by step. stop is always excluded. Returns a range object consumed by for."),
    "rng.uniform": (
        "Dwa argumenty wyznaczają dolną i górną granicę losowego czasu zmiennoprzecinkowego. Wynik jest liczbą, a nie korutyną. Tutaj przekazujemy go do sleep jako opóźnienie.",
        "Two arguments bound a random floating-point duration. Returns a number, not a coroutine. Here it supplies the sleep delay."),
    "rng.randint": (
        "Zwraca losową liczbę całkowitą między dwoma argumentami, włącznie z obiema granicami. W przeciwieństwie do range górna granica nie jest wykluczona.",
        "Returns a random integer including both bounds. Unlike range, the upper bound is included."),
    "random.Random": (
        "Argument 31 to ziarno osobnego generatora. Ten sam ciąg wywołań z tym samym ziarnem pozwala odtworzyć wejścia demonstracji. Nie ustala dokładnej kolejności planowania zadań.",
        "31 seeds a private random generator. Repeating calls with the same seed reproduces demo inputs, not exact task scheduling."),
    "random.uniform": (
        "Zwraca losową liczbę zmiennoprzecinkową z podanego przedziału. W wariancie losowym wynik może zmienić się przy każdym pokazie; nie należy zakładać, że zawsze wystąpi timeout.",
        "Returns a random floating-point number in the given interval. Random-mode inputs can change each run; a timeout is not guaranteed."),
    "len": ("Zwraca liczbę elementów kolekcji. Dla listy wyników liczy wyniki, nie dodaje ich wartości. Dla tekstu liczy znaki.", "Returns the number of collection items. For results it counts values rather than adding them. For a string it counts characters."),
    "sum": ("Dodaje liczby z przekazanej kolekcji i zwraca jedną liczbę. Pusta kolekcja daje domyślnie 0. Nie uruchamia korutyn; potrzebuje gotowych liczb.", "Adds collection numbers into a single number. An empty collection defaults to 0. Does not execute coroutines; requires actual numbers."),
    "all": ("Sprawdza kolejne warunki i zatrzymuje się na pierwszym False. Zwraca True, jeżeli wszystkie są prawdziwe, także dla pustej kolekcji testów.", "Checks conditions and stops on the first False. Returns True if all pass, including an empty collection of checks."),
    "min": ("Zwraca najmniejszą wartość z przekazanej kolekcji lub generatora. W wyścigu done zawiera co najmniej jeden zakończony Task.", "Returns the smallest collection or generator value. In the race done contains at least one completed Task."),
    "max": ("Zwraca największy argument lub element kolekcji. W limiterze max(0,czas) chroni przed ujemnym opóźnieniem; w generatorze wybiera największą liczbę pierwszą.", "Returns the largest argument or collection item. In the limiter max(0,delay) prevents a negative delay; in the generator it selects the largest prime."),
    "int": ("Zamienia wartość na liczbę całkowitą. Przy dodatnim pierwiastku ucina część ułamkową. Dla napisu ze statusem HTTP odczytuje zapis liczby.", "Converts a value to an integer. Truncates the fractional part of a positive square root; parses a numeric HTTP status string."),
    "str": ("Zamienia obiekt w tekst przeznaczony do czytania. Dla listy lub słownika daje ich reprezentację tekstową do logu, a nie strukturę HTML.", "Converts an object into readable text. Lists and dictionaries become textual log representations, not HTML structures."),
    "repr": ("Zwraca reprezentację diagnostyczną. Dla bytes pokaże prefiks b i znak nowej linii jako \\n, dzięki czemu widać faktyczny format wiadomości TCP.", "Returns a diagnostic representation. For bytes it shows b and a visible escaped newline, revealing the TCP message format."),
    "sorted": ("Tworzy nową, posortowaną listę i nie zmienia wejściowej kolekcji. Dzięki temu porównujemy komplet liczb bez wymagania kolejności przetworzenia.", "Creates a sorted list without changing the original collection. Allows checking all numbers regardless of processing order."),
    "set": ("Tworzy zbiór unikalnych wartości. Kolejność nie ma znaczenia, duplikaty znikają; dlatego osobno sprawdzamy liczbę wierszy przez len.", "Creates a set of unique values. Order is irrelevant and duplicates disappear, so line count is checked separately with len."),
    "list": ("Buduje listę z iterable, np. range(1,21). Lista pozwala porównać kolejno wszystkie oczekiwane wartości.", "Builds a list from an iterable such as range(1,21), allowing ordered comparison of expected values."),
    "tempfile.TemporaryDirectory": ("Tworzy prywatny katalog tymczasowy. with usuwa go przy wyjściu z bloku. Odczyt treści do pokazu musi nastąpić przed usunięciem.", "Creates a private temporary directory. with removes it on block exit. Read demo contents before leaving the block."),
    "Path": ("Tworzy obiekt ścieżki z napisu. Operator / dołącza nazwę pliku do katalogu; nie jest tu dzieleniem liczb.", "Creates a path object from text. The / operator appends a file name to a directory; here it is not numeric division."),
    "deque": ("Tworzy kolejkę dwustronną. append dodaje z prawej, popleft usuwa z lewej. Indeks [0] wskazuje najstarszy czas zezwolenia.", "Creates a double-ended queue. append adds on the right; popleft removes on the left. Index [0] is the oldest grant time."),
    "append": ("Dodaje jeden element na końcu listy lub deque i zwraca None. Zmienia istniejącą kolekcję: nie przypisuj wyniku append z powrotem do listy.", "Adds one item to a list or deque and returns None. Mutates the collection: do not assign the result of append back to the list."),
    "popleft": ("Usuwa i zwraca najstarszy element deque. Tutaj usuwamy wygasły czas, zanim policzymy aktywne zezwolenia.", "Removes and returns the oldest deque item. Here it removes an expired timestamp before counting active grants."),
    "splitlines": ("Dzieli tekst na listę wierszy, domyślnie bez znaków końca linii. Pozwala policzyć i sprawdzić każdy wpis pliku osobno.", "Splits text into lines, without line terminators by default. Allows counting and checking each file record separately."),
    "get": ("Dla słownika get(klucz,domyślna) zwraca wartość klucza lub wartość domyślną. Tutaj obsługuje brak parametru port albo delay. Nie myl tego z asynchronicznym queue.get.", "For a dictionary, get(key,default) returns the value or default. Here it handles missing port or delay. This is different from asynchronous queue.get."),
    "getsockname": ("Zwraca adres lokalnego gniazda jako krotkę. Indeks [1] odczytuje numer portu wybranego przez system; [0] byłby adresem IP.", "Returns a socket's local address tuple. Index [1] reads the OS-selected port; [0] would be the IP address."),
    "round": ("round(liczba,3) zaokrągla do trzech miejsc po przecinku na potrzeby prezentacji. Nie zmienia rzeczywistego czasu sleep.", "round(value,3) rounds to three decimal places for display. It does not change the actual sleep delay."),
}

# These are infrastructure operations; full task blocks explain their purpose.
INFRASTRUCTURE = {
    "web.Application": ("Tworzy aplikację lokalnego serwera HTTP i jej router.", "Creates the local HTTP server application and router."),
    "web.AppRunner": ("Opakowuje aplikację do uruchomienia i posprzątania serwera; setup przygotowuje obsługę, cleanup zwalnia zasoby.", "Wraps an application for server setup and cleanup."),
    "web.Response": ("Buduje odpowiedź HTTP z jawnym argumentem status.", "Builds an HTTP response using the explicit status argument."),
    "add_get": ("Rejestruje ścieżkę i funkcję obsługi GET. {status} przechwytuje fragment URL do request.match_info.", "Registers a GET path and handler; {status} captures a URL segment into request.match_info."),
    "setup": ("await przygotowuje runner przed utworzeniem serwera nasłuchującego.", "await prepares the runner before creating the listening server."),
    "cleanup": ("await zamyka zasoby serwera w finally również po błędzie.", "await closes server resources in finally, including after errors."),
    "create_server": ("await uruchamia serwer TCP używany przez aiohttp. Argumenty to fabryka protokołu, adres i port; 0 wybiera wolny port.", "await starts the TCP server used by aiohttp. Takes protocol factory, host and port; 0 chooses a free port."),
    "rsplit": ("Dzieli napis od prawej. rsplit('/',1)[-1] wybiera ostatni fragment URL do podpisu toru.", "Splits text from the right. rsplit('/',1)[-1] selects the last URL segment to label a lane."),
}
