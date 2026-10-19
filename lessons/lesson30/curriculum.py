"""A distinct learning objective per task; no repeated introductions."""
import ast
import re
from pathlib import Path

from code_notes import details
from teaching import QUESTIONS, TERMS
from assignments import assignment

ROOT = Path(__file__).resolve().parent


def pair(pl, en):
    return {"pl": pl, "en": en}


# title, introduction, observation prompt, interpretation, caveat, Q/A
ROWS = [('Pierwszy wątek|First thread',
  'Program może rozpocząć dodatkowy tok wykonania. Wątek główny i nowy wątek dzielą process, lecz '
  'dochodzą do końca w różnym czasie.|A program can start another flow of execution. The main and '
  'new threads share a process but reach the end at different times.',
  'Uruchom i obserwuj dwa tory: dodatkowy wątek śpi 3 s, a główny czeka przy join().|Run and watch '
  'both lanes: the new thread sleeps for 3 s while the main thread waits at join().',
  'start() uruchamia pracę. join() wyznacza miejsce, przed które główny wątek nie przejdzie, '
  'dopóki wskazany wątek nie skończy.|start() starts work. join() marks the point the main thread '
  'cannot pass until the selected thread finishes.',
  'Bez join() główny wątek może wykonać kolejne instrukcje wcześniej. Zwykły wątek niedemoniczny '
  'nadal powstrzymuje zakończenie programu.|Without join(), the main thread can continue earlier. '
  'A normal non-daemon thread still prevents program exit.',
  'Czy utworzenie Thread uruchamia funkcję?|Does constructing Thread start the function?',
  'Nie. Dopiero start() rozpoczyna wykonanie w osobnym wątku.|No. start() begins execution in a '
  'separate thread.'),
 ('Pięć wątków|Five threads',
  'Ta sama funkcja może obsługiwać kilka niezależnych wywołań. Każdemu przekazujemy inny numer '
  'przez arguments.|The same function can handle several independent calls. We pass a different '
  'number to each through arguments.',
  'Pięć pasków nakłada się w czasie. Porównaj numery w logu z kolejnością ich pojawiania się.|Five '
  'bars overlap. Compare their numbers with the order in which messages appear.',
  'Najpierw startujemy wszystkie wątki, potem na wszystkie czekamy. join() w pętli uruchamiającej '
  'ograniczyłby współbieżność.|Start all threads first, then wait for all of them. Calling join() '
  'in the start loop would limit concurrency.',
  'Krótkie sleep(0.6) to dodatek obserwacyjny. Nie oznacza, że drukowanie numeru wymaga tyle '
  'czasu.|The short sleep(0.6) is an observation aid. Printing a number does not require that '
  'long.',
  'Dlaczego args=(number,) ma przecinek?|Why does args=(number,) have a comma?',
  'To jednoelementowa krotka argumentów. Samo (numer) jest tylko wyrażeniem w nawiasach.|It is a '
  'one-element tuple of arguments. (number) alone is just a parenthesized expression.'),
 ('Czekanie a czas|Waiting versus time',
  'Gdy zadanie czeka na dane, procesor nie musi bezczynnie czekać razem z nim. Inne zadania mogą w '
  'tym okresie postępować.|When a task waits for data, other tasks can make progress during that '
  'wait.',
  'Porównaj trzy paski ustawione kolejno z trzema nakładającymi się. Powinieneś zobaczyć około 6 s '
  'i około 2 s.|Compare three consecutive bars with three overlapping ones. Expect roughly 6 s and '
  '2 s.',
  'Skrócenie wynika z nakładania oczekiwania, a nie z szybszego wykonania pojedynczego tasks.|The '
  'saving comes from overlapping waits, not from making each individual task faster.',
  'sleep symuluje czekanie na I/O. Nie mierzymy tu pobierania przez Internet ani obliczeń '
  'CPU.|sleep simulates I/O waiting. This does not measure Internet downloads or CPU work.',
  'Czy każdy z trzech wątków śpi krócej?|Does each thread sleep for less time?',
  'Nie: każdy nadal około 2 s, lecz te okresy zachodzą na siebie.|No: each still sleeps for about '
  '2 s, but those periods overlap.'),
 ('Utracony przyrost|Lost update',
  'Poprawna długość wspólnej listy nie dowodzi bezpieczeństwa dowolnej operacji. Odczyt i '
  'późniejszy zapis licznika tworzą inny problem.|A correct shared-list length does not prove all '
  'operations are safe. Reading and later writing a counter is a different problem.',
  'Najpierw zobacz listę 200 000 elementów. Potem dwa odczyty zera i dwa zapisy jedynki: '
  'oczekiwaliśmy 2.|First see a list of 200,000 elements. Then two reads of zero and two writes of '
  'one: we expected 2.',
  'Bariera celowo dopuszcza oba wątki do odczytu przed zapisem. To kontrolowany przykład utraconej '
  'aktualizacji.|A barrier deliberately lets both threads read before writing. This is a '
  'controlled lost-update example.',
  'Samo append i prosty counter += 1 nie muszą ujawnić błędu podczas konkretnego uruchomienia '
  'CPythona. Kontrola kolejności służy nauce.|append and a simple counter += 1 may not expose a '
  'bug in a particular CPython run. Controlled scheduling is used for teaching.',
  'Dlaczego oba dodania dały 1?|Why did two increments produce 1?',
  'Każdy wątek policzył 0 + 1 na podstawie tego samego starego odczytu.|Both threads computed 0 + '
  '1 from the same old value.'),
 ('Sekcja krytyczna|Critical section',
  'Blokada chroni cały fragment wymagający spójności. Tutaj odczyt, zmiana i zapis muszą należeć '
  'do jednej sekcji krytycznej.|A lock protects an entire operation that must remain consistent. '
  'Here read, modify and write must share one critical section.',
  'Paski posiadania Lock nie nakładają się. Drugi wątek odczytuje już 1, więc kończymy z 2.|The '
  'Lock ownership bars do not overlap. The second thread reads 1, so the final result is 2.',
  'with zdobywa blokadę i zwalnia ją również przy wyjątku. Wewnątrz tego obszaru pracuje jeden '
  'uczestnik naraz.|with acquires the lock and releases it even on exceptions. Only one '
  'participant occupies the protected region at a time.',
  'Chronimy też append zgodnie z poleceniem, ale jego wynik może być taki sam jak bez Lock. '
  'Różnicę mechanizmu pokazuje counter.|We also protect append as requested, but its result may be '
  'unchanged. The counter demonstrates the mechanism.',
  'Czy wystarczy blokować wyłącznie zapis?|Is locking only the write sufficient?',
  'Nie. Inny wątek mógł już wcześniej odczytać nieaktualną wartość.|No. Another thread may already '
  'have read a stale value.'),
 ('Pierwszy process|First process',
  'Proces jest osobnym uruchomionym programem z własną pamięcią. PID pozwala odróżnić rodzica i '
  'potomka.|A process is a separate running program with its own memory. PID distinguishes parent '
  'and child.',
  'W logach znajdź dwa PID i wynik 10! = 3 628 800. Wątek i process to różne poziomy organizacji '
  'pracy.|Find two PIDs and the result 10! = 3,628,800 in the log. Threads and processes are '
  'different levels of execution.',
  'Potomek oblicza wynik, rodzic czeka i sprawdza kod zakończenia. join nie przekazuje wartości '
  'zwróconej przez funkcję.|The child computes, the parent waits and checks the exit code. join '
  "does not transfer a function's return value.",
  'Na Windowsie nowy interpreter importuje moduł. Blok __main__ oddziela definicje od '
  'uruchamiania.|On Windows a fresh interpreter imports the module. The __main__ guard separates '
  'definitions from startup.',
  "Czy return z funkcji potomka trafi do rodzica?|Does a child's return value reach the parent?",
  'Nie automatycznie. Potrzebujemy np. Queue, Pipe albo puli zwracającej results.|Not '
  'automatically. Use Queue, Pipe or a pool that returns results.'),
 ('Argumenty procesu|Process arguments',
  'Do procesu przekazujemy dane wejściowe. Funkcja robocza jest zdefiniowana na poziomie modułu, '
  'aby można było odnaleźć ją po imporcie.|We pass input data to a process. The worker is defined '
  'at module level so it can be found after import.',
  'Uruchom 5³, potem wybierz 8³. Zmienia się argument i wynik, a mechanizm procesu pozostaje ten '
  'sam.|Run 5³, then select 8³. The argument and result change while the process mechanism stays '
  'the same.',
  'target wskazuje funkcję, args przekazuje jej dane w kolejności parametrów. Funkcja zostanie '
  'wywołana w potomku.|target identifies the function; args supplies positional data. The function '
  'is called in the child.',
  'Przy spawn dane i funkcja muszą nadawać się do serializacji. Lokalna lambda nie jest dobrym '
  'target dla tego przykładu.|With spawn, the function and data must be serializable. A local '
  'lambda is not a suitable target here.',
  'Dlaczego target=calculate_power, a nie calculate_power(5, 3)?|Why target=calculate_power '
  'instead of calculate_power(5, 3)?',
  'Nawiasy wykonałyby funkcję od razu w rodzicu i przekazały jej wynik zamiast '
  'funkcji.|Parentheses would call it immediately in the parent and pass its result instead of the '
  'function.'),
 ('Wiadomość w Queue|Queue message',
  'Oddzielna pamięć procesów wymaga jawnego przesłania danych. Kolejka służy do przekazywania '
  'wiadomości.|Separate process memory requires explicit data transfer. A queue carries messages.',
  'Wybierz gotowe imię. Zobacz put w potomku, następnie powitanie z get w rodzicu.|Select a '
  'prepared name. Observe put in the child, then the greeting from get in the parent.',
  'get czeka na wiadomość, a timeout ogranicza oczekiwanie. Odbieramy wynik przed join, żeby nie '
  'blokować przesyłania większych danych.|get waits for a message; timeout bounds the wait. '
  'Receive before join to avoid blocking transfers of larger data.',
  'Wariant UI zastępuje input formularzem. Proces potomny nie ma tu interaktywnej konsoli. To '
  'jawna adaptacja tasks.|The UI replaces input with a form. The child has no interactive console '
  'here. This is an explicit adaptation.',
  'Czy Queue jest wspólną zwykłą listą?|Is Queue a shared ordinary list?',
  'Nie. Zapewnia komunikację między procesami; obiekt jest serializowany i przesyłany.|No. It '
  'provides interprocess communication; objects are serialized and transferred.'),
 ('Częściowa suma|Partial sums',
  'Najpierw liczymy niezależne wyniki lokalne, potem krótko łączymy je pod blokadą. Ograniczamy '
  'czas zajmowania wspólnego zasobu.|Compute independent local results first, then combine them '
  'briefly under a lock. This limits time holding a shared resource.',
  'Znajdź cztery sumy częściowe i porównaj sumę końcową ze wzorem n(n−1)/2.|Find four partial sums '
  'and compare the final total with n(n−1)/2.',
  'Blokada jest potrzebna przy wspólnym akumulatorze, a nie przy lokalnej zmiennej partial_sum. '
  'Poprawność nie oznacza przyspieszenia.|The shared accumulator needs a lock; the local partial '
  'does not. Correctness does not imply a speedup.',
  'Domyślnie milion elementów; variant pełny ma 10 milionów i zużywa więcej pamięci. sum może '
  'długo wykonywać pracę bez przełączania wątków.|Default: one million elements. Full mode uses '
  'ten million and more memory. sum may work for a long time without switching threads.',
  'Dlaczego sum nie jest wewnątrz Lock?|Why is sum outside the Lock?',
  'Dane wejściowe tylko czytamy, wynik jest lokalny. Chronimy jedynie wspólną aktualizację.|Inputs '
  'are read-only and the result is local. Only the shared update is protected.'),
 ('Słowa w plikach|Words in files',
  'Jedno zadanie przypada na jeden file. Najpierw musimy precyzyjnie określić, co liczymy jako '
  'słowo.|One task handles one file. First we must define exactly what counts as a word.',
  'Dla python wynik to 4. Pythonista nie jest trafieniem. Wybierz code, aby zobaczyć inną liczbę '
  'bez edycji plików.|For python the result is 4. Pythonista does not match. Select code for '
  'another count without editing files.',
  'casefold normalizuje wielkość liter; wyrażenie regularne wydziela słowa; count zlicza całe '
  'tokens.|casefold normalizes letter case; a regular expression extracts words; count counts '
  'complete tokens.',
  'Trzy małe pliki tworzymy w katalogu tymczasowym. Praca może być za krótka, aby jej '
  'współbieżność była zauważalna na osi czasu.|Three small files are created in a temporary '
  'directory. Work may be too short for concurrency to be visible on the timeline.',
  "Czemu nie text.count('python')?|Why not text.count('python')?",
  'To zliczałoby też fragmenty słów, np. początek Pythonista.|That would also count substrings '
  'such as the beginning of Pythonista.'),
 ('Producent i consume|Producer and consumer',
  'Producent dostarcza element co 1 s, consume obsługuje go przez 1,5 s. Kolejka oddziela ich '
  'tempo pracy.|The producer supplies an item every 1 s; the consumer needs 1.5 s per item. A '
  'queue decouples their rates.',
  'Przez 10 s obserwuj listę wiadomości + i − oraz rosnący bilans oczekujących. Wolniejszy consume '
  'tworzy zaległość.|For 10 s watch the + and − messages and the pending-item balance. A slower '
  'consumer creates a backlog.',
  'Po 10 s zatrzymujemy produkcję. Kończymy bieżącą obsługę, odkładamy oczekujące i wysyłamy None '
  'jako sygnał zakończenia.|After 10 s production stops. Finish the current item, set pending '
  'items aside and send None as a shutdown signal.',
  'Zamykanie może potrwać dodatkowo do około 1,5 s. None jest sygnałem umownym; nie zwykłym '
  'zadaniem.|Shutdown can take about 1.5 s extra. None is a convention for shutdown, not a normal '
  'task.',
  'Co się stanie, gdy produce pozostanie szybszy?|What if the producer stays faster?',
  'Kolejka będzie rosła. Można ograniczyć jej pojemność i wprowadzić oczekiwanie producenta.|The '
  'queue grows. Bound its capacity to make the producer wait.'),
 ('GIL i pomiary|GIL and measurement',
  'W zwykłym CPythonie z GIL kilka wątków nie wykonuje jednocześnie kodu Pythona na wielu '
  'rdzeniach. Procesy mają osobne interpretery.|In a normal GIL-enabled CPython, several threads '
  'do not execute Python code on multiple cores at once. Processes have separate interpreters.',
  'Porównaj trzy słupki czasu. W każdym wariancie wykonujemy dwa identyczne obliczenia. Zwiększ '
  'rozmiar, gdy koszt startu dominuje.|Compare three time bars. Every mode performs two identical '
  'calculations. Increase the size if startup costs dominate.',
  'Wątki mogą mieć nakładające się okresy życia bez równoległego wykonywania bytecode. Oś pokazuje '
  'czas zadania, nie pomiar użycia rdzenia.|Thread lifetimes can overlap without parallel bytecode '
  'execution. The timeline shows task duration, not core utilization.',
  'Nie obiecujemy kolejności zwycięzców. Liczba rdzeni, obciążenie i limity Dockera zmieniają '
  'results. Istnieją też buildy bez GIL.|No winning order is promised. Core count, load and Docker '
  'limits affect results. Free-threaded builds also exist.',
  'Czy nakładające się paski dowodzą równoległości CPU?|Do overlapping bars prove CPU parallelism?',
  'Nie. Wątki mogą przeplatać pracę na jednym rdzeniu. Trzeba uwzględnić interpreter i '
  'pomiary.|No. Threads may interleave on one core. Consider the interpreter and measurements.'),
 ('Pula i liczby pierwsze|Pool and primes',
  'Pula utrzymuje ograniczoną liczbę procesów i rozdziela między nie wiele zadań. Nie tworzymy stu '
  'procesów dla stu liczb.|A pool keeps a limited number of processes and distributes many tasks '
  'among them. One hundred numbers do not mean one hundred processes.',
  'Zobacz przypisania liczb do procesów i tabelę par liczba–wynik w logu. Losowanie ma stałe '
  'ziarno.|See numbers assigned to processes and number–result pairs in the log. Random generation '
  'uses a fixed seed.',
  'map zachowuje kolejność wyników zgodną z wejściem. Bool jest też liczbą: sum listy True/False '
  'zlicza trafienia.|map preserves input order in the results. Booleans also act as numbers: '
  'summing True/False counts matches.',
  'Liczby do 1000 są tanie do sprawdzenia. Ten przykład uczy podziału pracy, nie gwarantuje '
  'przyspieszenia.|Numbers up to 1000 are cheap to test. This teaches work distribution, not '
  'guaranteed speedup.',
  'Dlaczego dzielniki sprawdzamy do pierwiastka?|Why test divisors only up to the square root?',
  'Jeżeli n ma parę dzielników, przynajmniej jeden nie przekracza pierwiastka z n.|If n has a pair '
  'of divisors, at least one is no greater than its square root.'),
 ('Kopie w tle|Background copies',
  'Niezależne pliki można kopiować osobnymi wątkami. Zakończenie pracy potwierdzamy dopiero po '
  'oczekiwaniu na wszystkie kopie.|Independent files can be copied by separate threads. Confirm '
  'completion only after waiting for every copy.',
  'Śledź start i koniec każdego pliku. Po join pojawi się liczba kopii i kontrola ich '
  "zgodności.|Track each file's start and finish. After join see the number of copies and their "
  'integrity check.',
  'copy2 kopiuje zawartość i próbuje zachować metadane. Hash po kopiowaniu potwierdza zgodność '
  'zawartości.|copy2 copies content and attempts to preserve metadata. A post-copy hash checks '
  'content equality.',
  'Kopiujemy cztery pliki po 2 MB w katalogu tymczasowym. Dysk i cache wpływają na czas; nie '
  'dodajemy sztucznego spowolnienia.|Four 2 MB files are copied in a temporary directory. Disk and '
  'cache affect timing; no artificial slowdown is added.',
  'Dlaczego sukces drukujemy po join wszystkich wątków?|Why report success after joining all '
  'threads?',
  'Wcześniej część plików mogłaby nadal być kopiowana.|Some files might still be copying before '
  'that point.'),
 ('Crawler i duplikaty|Crawler and duplicates',
  'Crawler odkrywa kolejne zadania podczas pracy. Dwie strony mogą wskazywać ten sam URL, więc '
  'sprawdzenie i rezerwacja muszą być wspólne.|A crawler discovers more work as it runs. Two pages '
  'can link to the same URL, so checking and reserving must be atomic together.',
  'Na lokalnej witrynie zobacz rozgałęzienie / → /a i /b → /c. Każdy adres powinien zostać pobrany '
  'tylko raz.|On the local site watch / branch into /a and /b, then /c. Each URL should be fetched '
  'once.',
  'Lock chroni zbiór visited, Queue rozdziela pracę, a task_done z join pilnują zakończenia '
  'dynamicznie dodawanych zadań.|Lock protects visited URLs, Queue distributes work, and task_done '
  'with join tracks dynamically added tasks.',
  'Prawdziwe HTTP obsługuje lokalny server z jawnym opóźnieniem 0,35 s. Internet nie jest '
  'potrzebny. Limit to 50 URL, witryna ma 4.|Real HTTP is served locally with an explicit 0.35 s '
  'delay. No Internet is needed. The limit is 50 URLs; the site has 4.',
  'Dlaczego samo if url not in set nie wystarczy?|Why is if url not in set alone insufficient?',
  'Dwa wątki mogą jednocześnie stwierdzić brak URL. Sprawdzenie i dodanie trzeba objąć jedną '
  'blokadą.|Two threads may both observe an absent URL. Protect the check and insertion with one '
  'lock.'),
 ('Odciski plików|File fingerprints',
  'SHA256 zamienia dowolnie długą zawartość na skrót. Czytanie blokami pozwala uniknąć ładowania '
  'całego pliku do pamięci.|SHA256 turns arbitrary content into a digest. Reading chunks avoids '
  'loading the entire file into memory.',
  'Obserwuj nazwy procesów i cztery skróty. Pliki mają tę samą długość, lecz różną '
  'zawartość.|Observe process names and four digests. The files have equal lengths but different '
  'contents.',
  'iter z funkcją i znacznikiem końca powtarza read do pustych bajtów. update dokłada kolejny blok '
  'do stanu obliczenia.|iter with a callable and sentinel repeats read until empty bytes. update '
  'adds each chunk to the running hash.',
  'To nie szyfrowanie. hashlib może zwalniać GIL dla większych bloków; tego przykładu nie używamy '
  'do dowodzenia ograniczeń wątków.|This is not encryption. hashlib may release the GIL for larger '
  'chunks; do not use this example as proof of thread limitations.',
  'Czy można odzyskać plik z hasha?|Can the file be recovered from the hash?',
  'Nie jest to odwracalny zapis danych. Skrót służy tu do porównywania zawartości.|It is not a '
  'reversible encoding. The digest is used here to compare content.'),
 ('Rozmowa przez Pipe|Pipe conversation',
  'Pipe udostępnia dwa końce połączenia. Rodzic wysyła dane, potomek odpowiada krotką z sumą i '
  'średnią.|Pipe provides two connection endpoints. The parent sends data; the child replies with '
  'a tuple of sum and mean.',
  'Wybierz listę i znajdź w logu wysłanie, odpowiedź oraz result. Własna lista nie może być '
  'pusta.|Choose a list and find the send, reply and result in the log. A custom list must not be '
  'empty.',
  'send i recv przenoszą obiekty. poll pozwala sprawdzić nadejście odpowiedzi z limitem czasu, '
  'zanim wywołamy blokujące recv.|send and recv transfer objects. poll waits with a timeout before '
  'calling blocking recv.',
  'Porządek logów z różnych procesów może odbiegać od porządku przyczynowego: wiadomość może '
  'dotrzeć przed logiem nadawcy.|Log order across processes may differ from causal order: a '
  'message may arrive before its sender logs the send.',
  'Co zwraca Pipe bez duplex=False?|What does Pipe return without duplex=False?',
  'Dwa końce połączenia dwukierunkowego. Każdy może wysyłać i odbierać.|Two endpoints of a duplex '
  'connection. Each can send and receive.'),
 ('Spójność konta|Account consistency',
  'Wypłata to sprawdzenie warunku i zmiana stanu. Te czynności muszą tworzyć jedną chronioną '
  'operację.|Withdrawal combines checking a condition and changing state. These must form one '
  'protected operation.',
  'Śledź kolejne salda i ewentualne odmowy. Na końcu porównaj saldo z 200 + sumą zaakceptowanych '
  'operacji.|Follow successive balances and any declines. Finally compare balance with 200 plus '
  'accepted transactions.',
  'Chronimy też historię, aby odpowiadała faktycznie wykonanym zmianom. Odmówiona wypłata nie '
  'trafia do sumy operacji.|Protect the history too so it matches actual changes. A declined '
  'withdrawal is excluded from accepted transactions.',
  'Kwoty mają stałe ziarno losowania, kolejność zależy od wątków. Krótkie opóźnienia uwidaczniają '
  'zdarzenia. To nie system bankowy.|Amounts use a fixed seed; order depends on threads. Short '
  'delays make events visible. This is not a banking system.',
  'Dlaczego warunek saldo >= kwota jest pod Lock?|Why is balance >= amount inside the Lock?',
  'Inna wypłata mogłaby zmienić saldo między sprawdzeniem a odjęciem.|Another withdrawal could '
  'change the balance between checking and subtracting.'),
 ('Pula zapytań AI|AI request pool',
  'ThreadPoolExecutor ogranicza liczbę równoczesnych zadań. Future reprezentuje pracę, której '
  'wynik może jeszcze nie być gotowy.|ThreadPoolExecutor bounds concurrent tasks. A Future '
  'represents work whose result may not yet be ready.',
  'Uruchom pulę 5, potem 10. Porównaj długość przebiegu i liczbę nakładających się oczekiwań.|Run '
  'a pool of 5, then 10. Compare duration and the number of overlapping waits.',
  'as_completed oddaje gotowe Future w kolejności ukończenia. result odbiera wynik lub zgłasza '
  'wyjątek tasks.|as_completed yields ready Futures in completion order. result retrieves the '
  "value or raises the task's exception.",
  'To symulacja: sleep udaje API, etykiety są losowe ze stałym ziarnem. Nie analizujemy znaczenia '
  'zdań i nie wysyłamy ich do AI.|This is simulated: sleep imitates an API; labels are seeded '
  'random choices. No sentence meaning is analysed and no AI service is called.',
  'Czy wyniki przyjdą w kolejności zdań?|Will results arrive in sentence order?',
  'Nie przy as_completed. Dlatego wynik zawiera też zdanie, którego dotyczy.|Not with '
  'as_completed. Each result therefore includes its source sentence.'),
 ('Obrazy i koszt IPC|Images and IPC cost',
  'Rozdzielenie obliczeń wymaga także przesłania danych do procesów i odebrania wyników. Przy '
  'prostym filtrze ten koszt może przeważyć.|Distributing calculations also requires sending data '
  'to processes and receiving results. This cost may dominate a simple filter.',
  'Porównaj czasy i zgodność wyników. Wybierz pełne 1000×1000, aby zobaczyć wpływ większych '
  'danych.|Compare times and result equality. Select the full 1000×1000 case to see the effect of '
  'larger data.',
  'Mierzymy pulę wraz z uruchomieniem i przesyłaniem obrazów. Wynik wolniejszych procesów jest '
  'poprawną obserwacją, a nie błędem demonstracji.|The pool timing includes startup and image '
  'transfer. Slower processes are a valid observation, not a demo failure.',
  'Domyślnie 10 obrazów 300×300; pełne 1000×1000 może zużyć ponad 1 GB. Nie używamy modelu AI, '
  'tylko mnożymy piksele.|Default: ten 300×300 images. Full 1000×1000 may use over 1 GB. No AI '
  'model is used; pixels are simply multiplied.',
  'Czemu procesy mogą być wolniejsze mimo wielu rdzeni?|Why can processes be slower despite '
  'multiple cores?',
  'Start interpreterów, serializacja, przesyłanie i odtwarzanie list mogą kosztować więcej niż sam '
  'filtr.|Interpreter startup, serialization, transfer and reconstruction may cost more than the '
  'filter itself.')]

# Marker -> explanation of the *actual highlighted block*, not a fixed offset.
STEPS = {1: {'worker': 'Funkcja work opisuje zadanie, ale sama definicja go nie uruchamia. time to moduł '
               'standardowy; time.sleep(3) usypia bieżący wątek na około 3 sekundy. span i event '
               'zapisują ten przebieg dla UI.|work defines the task but defining it does not '
               'execute it. time is a standard module; time.sleep(3) pauses the current thread for '
               'about three seconds. span and event record the execution for the UI.',
     'create': 'Thread tworzy obiekt. target=work przekazuje funkcję bez jej wywołania.|Thread '
               'constructs an object. target=work passes the function without calling it.',
     'start': 'start zleca wykonanie work w nowym wątku; główny wątek może iść dalej.|start '
              'schedules work in a new thread; the main thread can continue.',
     'join': 'span zapisuje przedział oczekiwania do UI. Właściwe czekanie wykonuje '
             'worker_thread.join().|span records the wait interval for the UI. '
             'worker_thread.join() performs the actual waiting.'},
 2: {'args': 'range(1, 6) daje 1–5. args=(number,) przekazuje jeden argument. append zachowuje '
             'uchwyt; start rozpoczyna pracę.|range(1, 6) yields 1–5. args=(number,) supplies one '
             'argument. append retains the handle; start begins work.',
     'join': 'Pętla przechodzi przez zachowane obiekty i czeka na każdy z nich. Nie tworzy '
             'kolejnych wątków.|The loop waits for each retained thread object. It does not create '
             'any more threads.'},
 3: {'sequential': 'Wywołujemy funkcję bez Thread. Następne pobranie zaczyna się dopiero po '
                   'powrocie poprzedniego.|Call the function without Thread. The next retrieval '
                   'starts only after the previous call returns.',
     'concurrent': 'Lista tworzy trzy obiekty Thread. Osobna pętla startuje wszystkie, dopiero '
                   'następna czeka.|The list creates three Thread objects. One loop starts all of '
                   'them; the next waits.'},
 4: {'append': 'Sto tysięcy dopisań w każdym wątku realizuje treść zadania z listą. Sam poprawny '
               'wynik nie rozstrzyga o innych operacjach.|One hundred thousand appends per thread '
               'implement the list exercise. A correct result says nothing about other operations.',
     'read': 'Każdy wątek kopiuje bieżący counter do własnej lokalnej zmiennej previous.|Each '
             'thread copies the current counter to its own local variable previous.',
     'barrier': 'Barrier(2) czeka na obu uczestników. Dzięki temu żaden nie zapisze, zanim obaj '
                'odczytają zero.|Barrier(2) waits for both participants so neither writes before '
                'both have read zero.',
     'write': 'Każdy zapisuje własne previous + 1. Oba stare odczyty to zero, więc tracimy jeden '
              'przyrost.|Each writes its own previous + 1. Both old reads are zero, so one '
              'increment is lost.'},
 5: {'listlock': 'with zdobywa wspólną blokadę na czas jednego append i automatycznie ją '
                 'zwalnia.|with acquires the shared lock for one append and releases it '
                 'automatically.',
     'critical': 'Blokada obejmuje odczyt, oczekiwanie i zapis. Drugi wątek wejdzie dopiero po '
                 'wyjściu pierwszego.|The lock covers read, wait and write. The second thread '
                 'enters only after the first exits.'},
 6: {'factorial': 'math.factorial(10) oblicza iloczyn liczb 1–10 i zwraca liczbę '
                  'całkowitą.|math.factorial(10) computes the product of integers 1–10 and returns '
                  'an integer.',
     'process': 'Process przechowuje funkcję do uruchomienia w potomku. To osobny process, nie '
                'Thread.|Process holds the function to run in a child. This is a separate process, '
                'not a Thread.',
     'guard': '__name__ ma wartość __main__ przy uruchomieniu pliku. Import w nowym interpreterze '
              'nie uruchomi launch ponownie.|__name__ is __main__ when running the file. Importing '
              'it in a fresh interpreter does not launch it again.'},
 7: {'worker': 'Parametry number i exponent dostaną wartości z args. ** jest operatorem '
               'potęgowania.|The parameters number and exponent receive values from args. ** is '
               'exponentiation.',
     'args': 'config.get pobiera liczbę z formularza albo domyślne 5. Krotka (number, 3) wiąże dwa '
             'argumenty pozycyjne.|config.get reads the form value or defaults to 5. The tuple '
             '(number, 3) binds two positional arguments.'},
 8: {'put': 'put umieszcza imię w kolejce międzyprocesowej. Rodzic otrzyma przesłaną wartość.|put '
            'places the name in the interprocess queue. The parent receives the transferred value.',
     'queue': 'mp.Queue tworzy kanał wiadomości, którego uchwyt przekażemy potomkowi.|mp.Queue '
              'creates a message channel whose handle is passed to the child.',
     'get': 'get czeka najwyżej 10 sekund na jedną wiadomość. Timeout zgłosi wyjątek zamiast '
            'nieskończonego czekania.|get waits up to 10 seconds for one message. Timeout raises '
            'an exception instead of waiting forever.'},
 9: {'local': 'sum czyta fragment listy i zapisuje wynik lokalnie. Nie zmienia wspólnego '
              'akumulatora.|sum reads a list chunk and stores a local result. It does not change '
              'the shared accumulator.',
     'merge': 'with zdobywa blokadę na czas dodania partial_sum do wspólnej total_sum. Po wyjściu '
              'z tego bloku inny wątek może wykonać swoją aktualizację.|with holds the lock while '
              'adding partial_sum to the shared total_sum. After the block another thread can '
              'perform its update.',
     'chunks': 'Granice i*n//4 i (i+1)*n//4 dzielą dane także wtedy, gdy długość nie dzieli się '
               'przez 4. Wycinek listy tworzy kopię.|The boundaries i*n//4 and (i+1)*n//4 also '
               'handle lengths not divisible by four. A list slice creates a copy.'},
 10: {'tokens': 'read_text czyta UTF-8, casefold normalizuje litery, findall z wzorcem \\w+ zwraca '
                'listę słów.|read_text reads UTF-8; casefold normalizes case; findall with \\w+ '
                'returns a list of words.',
      'merge': 'Każdy plik ma lokalny result. Tylko dopisanie go do wspólnej sumy wymaga '
               'blokady.|Each file has a local count. Only adding it to the shared total needs a '
               'lock.',
      'files': 'glob wybiera pliki .txt w przygotowanym katalogu. Dla każdego tworzymy osobny '
               'wątek.|glob selects .txt files in the prepared directory. Create one thread for '
               'each.'},
 11: {'put': 'Producent dodaje numer do bezpiecznej wątkowo queue.Queue; nie potrzebuje '
             'dodatkowego Lock dla samego put.|The producer adds a number to a thread-safe '
             'queue.Queue; put needs no extra Lock.',
      'get': 'get blokuje konsumenta, gdy kolejka jest pusta. Zwraca jeden element, a nie całą '
             'kolejkę.|get blocks the consumer when empty. It returns one item, not the entire '
             'queue.',
      'shutdown': 'Po 10 sekundach set ustawia Event. Producent oczekujący przy stop.wait(1) '
                  'obudzi się z True i przerwie pętlę.|After ten seconds set signals the Event. '
                  'The producer waiting at stop.wait(1) wakes with True and breaks its loop.',
      'sentinel': 'None jest umownym końcem pracy. Konsument odbiera je przez get i wychodzi; '
                  'task_done wykona się w finally również dla tego sygnału.|None is the agreed '
                  'shutdown marker. The consumer receives it with get and returns; finally also '
                  'calls task_done for this marker.'},
 12: {'cpu': 'Generator produkuje i*i dla kolejnych i, a sum je sumuje. To rzeczywista praca CPU w '
             'Pythonie.|The generator yields i*i for successive i, and sum adds them. This is real '
             'Python CPU work.',
      'workers': 'Parametr worker_type oznacza Thread albo Process. Ten sam kod organizuje dwa '
                 'zadania z tym samym n.|worker_type is Thread or Process. The same code organizes '
                 'two tasks with the same n.',
      'benchmark': 'measured używa perf_counter. Dwa wywołania w liście są sequential_results: nie '
                   'tworzą dodatkowych wykonawców.|measured uses perf_counter. The two calls in a '
                   'list are sequential: they create no extra workers.'},
 13: {'prime': 'Liczby <2 odrzucamy. all sprawdza brak dzielnika do pierwiastka włącznie i kończy '
               'po pierwszym False.|Reject values below 2. all checks for no divisor through the '
               'square root and stops at the first False.',
      'pool': 'Pool(2) tworzy dwóch wykonawców. map wysyła zadania i zbiera wyniki w kolejności '
              'wejścia. with zamyka pulę.|Pool(2) creates two workers. map dispatches jobs and '
              'collects input-ordered results. with closes the pool.'},
 14: {'copy': 'copy2 kopiuje rzeczywistą zawartość do nowej ścieżki. Operator / na Path łączy '
              'katalog i nazwę.|copy2 copies real content to a new path. The Path / operator joins '
              'a directory and name.',
      'wait': 'Ta pętla uruchamia każdy przygotowany wątek kopiowania. W tym fragmencie nie ma '
              'join: uruchomienie następnej kopii nie czeka na zakończenie poprzedniej.|This loop '
              'starts each prepared copy thread. There is no join in this chunk: starting the next '
              'copy does not wait for the previous one to finish.',
      'verify': 'all wymaga zgodności SHA256 każdej pary źródło–kopia. Porównanie następuje po '
                'join.|all requires equal SHA256 for every source–copy pair. Comparison happens '
                'after join.'},
 15: {'deduplicate': 'Jedna blokada chroni sprawdzenie domeny i limitu, sprawdzenie zbioru oraz '
                     'rezerwację URL. Unikamy podwójnego dodania.|One lock protects domain and '
                     'limit checks, set lookup and URL reservation. This avoids duplicate '
                     'insertion.',
      'fetch': 'urlopen wykonuje HTTP; with zamyka odpowiedź. Parser czyta HTML, ale nie wykonuje '
               'JavaScript.|urlopen performs HTTP; with closes the response. The parser reads HTML '
               'but does not execute JavaScript.',
      'drain': 'Queue.join czeka na task_done dla wszystkich zleconych elementów, także odkrytych '
               'w trakcie. To inny join niż Thread.join.|Queue.join waits for task_done on all '
               'queued items, including newly discovered ones. This is different from '
               'Thread.join.'},
 16: {'init_hash': 'hashlib.sha256() tworzy nowy stan obliczenia skrótu i przypisuje go do digest. '
                   'Ta linia jeszcze nie czyta pliku.|hashlib.sha256() creates a fresh digest '
                   'state and assigns it to digest. This line does not read the file yet.',
      'hash': "Otwieramy plik binarnie. iter wywołuje odczyt bloków aż do b'', a update dodaje "
              'bajty każdego bloku do istniejącego stanu digest.|Open the file in binary mode. '
              "iter repeats chunk reads until b'', and update adds each chunk to the existing "
              'digest state.',
      'digest': 'Zwracamy parę: nazwę pliku oraz digest.hexdigest(), czyli 64-znakowy zapis '
                'szesnastkowy wyliczonego SHA256.|Return a pair: the file name and '
                'digest.hexdigest(), the 64-character hexadecimal representation of the computed '
                'SHA256.',
      'map': 'Funkcja zwraca parę (name, hash). dict zmienia listę takich par w słownik '
             'wyników.|The worker returns a (name, hash) pair. dict converts the list of pairs '
             'into a results dictionary.'},
 17: {'receive': 'recv czeka na obiekt wysłany drugim końcem. Tu otrzymujemy listę liczb.|recv '
                 'waits for an object sent from the other end. Here it receives a list of numbers.',
      'reply': 'send przesyła krotkę. Suma podzielona przez długość daje średnią; dlatego nie '
               'dopuszczamy pustej listy.|send transfers a tuple. Sum divided by length gives the '
               'mean, so an empty list is rejected.',
      'pipe': 'Pipe tworzy dwa połączone końce. Jeden zostaje w rodzicu, drugi przekazujemy '
              'potomkowi.|Pipe creates two connected endpoints. One stays with the parent; the '
              'other goes to the child.'},
 18: {'deposit': 'Lock chroni razem saldo i historię. Najpierw zmieniamy saldo, następnie '
                 'zapisujemy zaakceptowaną kwotę.|Lock protects balance and history together. '
                 'Update the balance, then record the accepted amount.',
      'withdraw': 'Warunek i odjęcie są wewnątrz tej samej blokady. else rejestruje odmowę, bez '
                  'zmiany salda.|The condition and subtraction share one lock. else records a '
                  'decline without changing the balance.',
      'reconcile': '200 to saldo początkowe. sum(account.history) dodaje wyłącznie zaakceptowane '
                   'wpłaty i wypłaty. metric pokazuje niezależnie wyliczone saldo kontrolne.|200 '
                   'is the opening balance. sum(account.history) adds accepted deposits and '
                   'withdrawals only. metric displays this independently reconciled balance.'},
 19: {'simulate': 'rng.uniform(0.5, 2.0) wybiera czas oczekiwania od 0,5 do 2 sekund. time.sleep '
                  'usypia bieżący wątek na ten czas, symulując czekanie na API.|rng.uniform(0.5, '
                  '2.0) selects a waiting time between 0.5 and 2 seconds. time.sleep pauses the '
                  'current thread for that duration, simulating an API wait.',
      'submit': 'enumerate(sentences, 1) tworzy pary numer–zdanie. Dla każdej pary submit zleca '
                'analyze_sentiment i od razu zwraca Future. Lista futures zachowuje wszystkie te '
                'uchwyty.|enumerate(sentences, 1) creates number–sentence pairs. For each pair '
                'submit schedules analyze_sentiment and immediately returns a Future. futures '
                'retains all those handles.',
      'complete': 'as_completed wybiera ukończone Future. result odbiera wynik lub wyjątek; append '
                  'zachowuje odebrane dane.|as_completed picks finished tasks. result retrieves '
                  'the value or exception; append retains the received data.'},
 20: {'filter': 'Zagnieżdżone list comprehensions budują nowy image. Każdy piksel mnożymy przez '
                '1.1; wejścia nie zmieniamy.|Nested list comprehensions build a new image. Each '
                'pixel is multiplied by 1.1; the input is unchanged.',
      'data': 'Trzy poziomy list oznaczają: obrazy, wiersze i piksele. Losowanie wykonujemy przed '
              'pomiarem filtra.|Three list levels mean images, rows and pixels. Random generation '
              'happens before filter timing.',
      'pool': 'Pool(processes=2) tworzy pulę dwóch procesów. Dla każdego obrazu budujemy krotkę '
              '(number, image, etykieta), a map przekazuje ją do apply_filter. return zwraca listę '
              'przefiltrowanych obrazów.|Pool(processes=2) creates a two-process pool. For each '
              'image we build a (number, image, label) tuple; map passes it to apply_filter. '
              'return returns the list of filtered images.'}}


def bilingual(text):
    pl, en = text.split("|", 1)
    return pair(pl, en)


PRESETS = {
    7: [("5³", {"number": 5}), ("8³", {"number": 8})],
    8: [("Anna", {"name": "Anna"}), ("Tomasz", {"name": "Tomasz"})],
    9: [("1 000 000", {"size": 1_000_000}),
        ("10 000 000", {"size": 10_000_000})],
    10: [("python", {"word": "python"}), ("code", {"word": "code"})],
    12: [("6 000 000", {"size": 6_000_000}),
         ("20 000 000", {"size": 20_000_000})],
    17: [("[2, 4, 6, 8]", {"numbers": [2, 4, 6, 8]}),
         ("[10, 20, 30]", {"numbers": [10, 20, 30]})],
    19: [("5", {"workers": 5}), ("10", {"workers": 10}),
         ("1", {"workers": 1})],
    20: [("10 × 300 × 300", {"side": 300}),
         ("10 × 1000 × 1000", {"side": 1000})],
}


def lesson(number):
    row = ROWS[number - 1]
    keys = ("title", "intro", "watch", "takeaway", "caveat", "question", "answer")
    data = {key: bilingual(value) for key, value in zip(keys, row)}
    data.update(number=number, presets=[{"label": label, "value": value}
                for label, value in PRESETS.get(number, [("Demo", {})])])
    data["assignment"] = assignment(number)
    data["steps"] = source_steps(number)
    data["terms"] = [{"name": name, "body": bilingual(body)} for name, body in TERMS[number]]
    question, answer = QUESTIONS[number]
    data["extra_question"] = bilingual(question)
    data["extra_answer"] = bilingual(answer)
    return data


def source_steps(number):
    path = ROOT / "examples" / f"task{number:02}.py"
    source = path.read_text(encoding="utf-8")
    rows = source.splitlines()
    statements = [node for node in ast.walk(ast.parse(source))
                  if isinstance(node, ast.stmt)]
    steps = []
    found = set()
    for line, text in enumerate(rows, 1):
        match = re.match(r"\s*# @step (\w+)\s*$", text)
        if not match:
            continue
        key = match.group(1)
        if key in found:
            raise ValueError(f"Duplicate marker: {path.name}:{key}")
        found.add(key)
        # The next complete Python statement, including its nested block.
        candidates = [n for n in statements if n.lineno == line + 1]
        if not candidates or key not in STEPS[number]:
            raise ValueError(f"Invalid code reference: {path.name}:{key}")
        node = max(candidates, key=lambda n: n.end_lineno)
        steps.append(dict(id=key, start=node.lineno, end=node.end_lineno,
                          body=bilingual(STEPS[number][key]),
                          details=details(source, node.lineno, node.end_lineno, number, key,
                                          bilingual(STEPS[number][key]))))
    if found != set(STEPS[number]):
        raise ValueError(f"Missing marker in {path.name}")
    return {"file": path.name, "source": source, "steps": steps}
