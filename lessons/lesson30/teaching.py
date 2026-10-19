"""New vocabulary only. Earlier mechanisms are not reintroduced in every task."""
TERMS = {1: [('Wątek główny / Main thread',
      'Tok wykonania rozpoczęty przy starcie programu. Może uruchamiać inne wątki.|The execution '
      'flow created at program startup. It can start other threads.'),
     ('target',
      'Funkcja przekazana do późniejszego wywołania. Jej nazwa bez () oznacza sam obiekt '
      'funkcji.|A function passed for a later call. Its name without () denotes the function '
      'object.')],
 2: [('args',
      'Krotka argumentów pozycyjnych funkcji. Pierwszy element odpowiada pierwszemu parametrowi.|A '
      'tuple of positional function arguments. The first item binds the first parameter.'),
     ('Współdzielony kod / Shared code',
      'Każdy wątek wywołuje tę samą funkcję, ale ma własny parametr numer i lokalny przebieg.|Each '
      'thread calls the same function but has its own number argument and execution flow.')],
 3: [('I/O-bound',
      'Zadanie spędza dużo czasu czekając na wejście lub wyjście, np. odpowiedź serwera.|A task '
      'spends much of its time waiting for input or output, such as a server response.'),
     ('Współbieżność / Concurrency',
      'Zadania postępują w nakładających się okresach. Równoległość oznacza wykonywanie pracy w '
      'tym samym momencie, np. na dwóch rdzeniach.|Tasks progress during overlapping periods. '
      'Parallelism means work is executed at the same instant, for example on two cores.')],
 4: [('Race condition',
      'Wynik zależy od kolejności przeplatania operacji uczestników. Poprawne pojedyncze operacje '
      "nie muszą tworzyć poprawnej całości.|The result depends on participants' operation "
      'interleaving. Individually correct operations may not compose safely.'),
     ('Barrier',
      'Punkt spotkania: każdy uczestnik czeka, aż dotrze ustalona liczba uczestników.|A '
      'rendezvous: each participant waits until the configured number arrives.')],
 5: [('Lock',
      'Wspólna blokada wpuszcza do chronionego obszaru jednego wykonawcę naraz.|A shared lock '
      'admits one worker at a time into the protected region.'),
     ('Sekcja krytyczna / Critical section',
      'Fragment, którego operacje na wspólnym stanie muszą być spójne jako całość.|A region whose '
      'shared-state operations must remain consistent as a whole.')],
 6: [('Proces / Process',
      'Instancja programu z własną przestrzenią pamięci; system rozpoznaje ją po PID.|A program '
      'instance with its own memory space, identified by a PID.'),
     ('spawn',
      'Nowy interpreter importuje moduł i uruchamia wskazaną funkcję. Stąd wymóg ochrony części '
      'startowej przez __main__.|A fresh interpreter imports the module and runs the target '
      'function. This is why startup needs the __main__ guard.')],
 7: [('Serializacja / Serialization',
      'Przekształcenie obiektu do postaci nadającej się do przesłania i odtworzenia w drugim '
      'procesie.|Converting an object to a transferable form that another process can '
      'reconstruct.'),
     ('Poziom modułu / Module level',
      'Funkcja znajduje się poza inną funkcją. Interpreter potomka może odnaleźć ją przez import '
      'modułu.|The function is defined outside other functions. The child interpreter can find it '
      'by importing the module.')],
 8: [('IPC',
      'Komunikacja między procesami: jawne przesyłanie danych przez Queue, Pipe lub inne '
      'mechanizmy.|Interprocess communication: explicitly sending data through Queue, Pipe or '
      'other mechanisms.'),
     ('Blokujące get / Blocking get',
      'Odbiorca zatrzymuje swój dalszy przebieg do nadejścia wiadomości albo upłynięcia '
      'timeout.|The receiver pauses its progress until a message arrives or timeout expires.')],
 9: [('Akumulator / Accumulator',
      'Wspólna zmienna zbierająca wyniki częściowe. Tu total_sum.|A shared variable collecting '
      'partial results, here total_sum.'),
     ('Wycinek / Slice',
      'dane[a:b] wybiera indeksy od a do b bez b. Dla listy powstaje nowa lista.|data[a:b] selects '
      'indices from a up to but excluding b. For a list, it creates a new list.')],
 10: [('Token',
       'Jedno wydzielone słowo. Liczenie tokenów odróżnia Python od Pythonista.|One extracted '
       'word. Counting tokens distinguishes Python from Pythonista.'),
      ('casefold / \\w+',
       'casefold ujednolica litery. Wzorzec \\w+ wybiera kolejne ciągi znaków słowa.|casefold '
       'normalizes letter case. The pattern \\w+ matches sequences of word characters.')],
 11: [('queue.Queue',
       'Kolejka do komunikacji wątków. get czeka na dane, task_done potwierdza obsłużenie '
       'elementu.|A queue for thread communication. get waits for data; task_done acknowledges an '
       'item.'),
      ('Event / sentinel',
       'Event sygnalizuje zatrzymanie produkcji. Sentinel None jest specjalną wiadomością kończącą '
       'konsumenta.|Event signals production to stop. The None sentinel is a special message that '
       'shuts down the consumer.')],
 12: [('CPU-bound',
       'Czas dominuje wykonywanie obliczeń. Samo nakładanie czekania nie pomoże.|Computation '
       'dominates duration. Overlapping waits alone will not help.'),
      ('GIL',
       'W używanym standardowym CPythonie jeden wątek naraz wykonuje kod Pythona. Biblioteki '
       'natywne mogą zwalniać tę blokadę.|In the standard CPython used here, one thread executes '
       'Python code at a time. Native libraries can release this lock.')],
 13: [('Pool',
       'Stała liczba procesów wielokrotnie pobiera kolejne tasks. Koszt uruchomienia jest '
       'współdzielony przez wiele zadań.|A fixed number of processes repeatedly takes tasks. '
       'Startup cost is shared across many jobs.'),
      ('map',
       'Funkcja zostaje zastosowana do każdego elementu. Wyniki zachowują kolejność wejścia, choć '
       'praca kończy się w różnej kolejności.|A function is applied to each item. Results preserve '
       'input order even if execution finishes out of order.')],
 14: [('shutil.copy2',
       'Kopiuje plik i próbuje zachować metadane. Nie gwarantuje skopiowania wszystkich atrybutów '
       'systemowych.|Copies a file and attempts to preserve metadata. Not all system attributes '
       'are guaranteed to be copied.'),
      ('Kontrola integralności / Integrity check',
       'Porównujemy zawartość źródła i kopii przez ich skróty po zakończeniu kopiowania.|Compare '
       'source and copy content using digests after copying finishes.')],
 15: [('Rezerwacja URL / URL reservation',
       'Dodajemy URL do zbioru już przy zlecaniu. Inne wątki wiedzą, że adres został '
       'przydzielony.|Add the URL to the set when scheduling it, so other threads know it is '
       'already assigned.'),
      ('Queue.join',
       'Czeka, aż każde put uzyska odpowiadające task_done. To oczekiwanie na zadania, a nie na '
       'zakończenie wątków.|Waits until each put has a matching task_done. This waits for tasks, '
       'not for threads to exit.')],
 16: [('SHA256',
       'Skrót ma 256 bitów; hexdigest prezentuje je jako 64 znaki szesnastkowe.|A 256-bit digest; '
       'hexdigest displays it as 64 hexadecimal characters.'),
      ('iter(funkcja, koniec)',
       'Wywołuje funkcję wielokrotnie, dopóki nie zwróci wartości równej znacznikowi koniec.|Calls '
       'a function repeatedly until its return value equals the stop sentinel.')],
 17: [('Pipe',
       'Para końców kanału komunikacyjnego. Domyślnie kanał jest dwukierunkowy.|A pair of '
       'communication endpoints. By default the channel is duplex.'),
      ('Rozpakowanie / Unpacking',
       'suma, average = wynik przypisuje dwa elementy krotki do dwóch zmiennych.|total, average = '
       'result assigns two tuple items to two variables.')],
 18: [('Niezmiennik / Invariant',
       'Warunek, który ma pozostawać prawdziwy: saldo = saldo początkowe + zaakceptowane '
       'operacje.|A condition that must remain true: balance = opening balance + accepted '
       'transactions.'),
      ('Sprawdź i zmień / Check then act',
       'Sprawdzenie dostępności środków i ich odjęcie są jedną logiczną operacją.|Checking '
       'available funds and subtracting them form one logical operation.')],
 19: [('Future',
       'Uchwyt do przyszłego wyniku. Może oznaczać pracę oczekującą, trwającą lub zakończoną.|A '
       'handle to a future result. It can represent pending, running or completed work.'),
      ('as_completed',
       'Pozwala odbierać wyniki w kolejności gotowości zamiast czekać na wolniejsze wcześniejsze '
       'task.|Lets results be received in readiness order rather than waiting for an earlier slow '
       'task.')],
 20: [('Koszt IPC / IPC cost',
       'Przenoszenie dużych list wymaga serializacji, przesłania i odtworzenia '
       'obiektów.|Transferring large lists requires serialization, transfer and object '
       'reconstruction.'),
      ('Pomiar całości / End-to-end timing',
       'Wliczamy start puli i odebranie wyników, bo użytkownik czeka także na te '
       'czynności.|Include pool startup and result collection because the user waits for those '
       'too.')]}

QUESTIONS = {1: ('Co zrobi bezpośrednie work() zamiast start()?|What does calling work() directly do instead '
     'of start()?',
     'Wykona pracę w bieżącym wątku; następna instrukcja poczeka na jej powrót.|It runs in the '
     'current thread; the next statement waits for the call to return.'),
 2: ('Co zmieni join zaraz po każdym start?|What changes if each start is followed immediately by '
     'join?',
     'Główny wątek zaczeka przed uruchomieniem następnego, więc zadania będą praktycznie '
     'sequential_results.|The main thread waits before starting the next task, making them '
     'effectively sequential.'),
 3: ('Czy trzy razy więcej wątków zawsze da trzy razy krótszy czas?|Do three times as many threads '
     'always cut time by three?',
     'Nie. Decydują rodzaj pracy, ograniczenia zasobów i narzut zarządzania wykonawcami.|No. Work '
     'type, resource limits and worker-management overhead determine the result.'),
 4: ('Czy GIL zastępuje blokadę operacji biznesowej?|Does the GIL replace a lock around a business '
     'operation?',
     'Nie. Wieloetapowe operacje mogą zostać przeplecione. W przykładzie oba odczyty i zapisy są '
     'legalne osobno, ale razem gubią aktualizację.|No. Multi-step operations can interleave. The '
     'reads and writes here are individually valid yet lose an update together.'),
 5: ('Czy każdy wątek może utworzyć własny Lock?|Can each thread create its own Lock?',
     'Własne niezależne blokady nie chronią wspólnej sekcji przed sobą. Uczestnicy muszą używać '
     'tej samej blokady.|Separate private locks do not exclude each other. Participants must use '
     'the same lock.'),
 6: ('Co znaczy exitcode równy zero?|What does an exitcode of zero mean?',
     'Proces zakończył się bez zgłoszonego błędu na poziomie systemu. To nie jest wynik silni.|The '
     'process exited without a reported system-level error. It is not the factorial result.'),
 7: ('Czy zmiana zwykłej globalnej listy w potomku zmieni listę rodzica?|Does changing an ordinary '
     "global list in a child change the parent's list?",
     'Nie. Procesy mają odrębną pamięć; potrzebują IPC lub jawnie współdzielonych zasobów.|No. '
     'Processes have separate memory and need IPC or explicitly shared resources.'),
 8: ('Co się stanie, jeśli nikt nie wyśle imienia?|What if nobody sends a name?',
     'get z timeout zgłosi queue.Empty po upłynięciu limitu. Bez limitu mógłby czekać bez '
     'końca.|get with timeout raises queue.Empty after the limit. Without a timeout it could wait '
     'indefinitely.'),
 9: ('Co się stanie z resztą przy długości niepodzielnej przez cztery?|What happens when the '
     'length is not divisible by four?',
     'Granice wyliczone jako i*n//4 obejmą wszystkie indeksy; długości fragmentów mogą się różnić '
     'o jeden.|Boundaries computed as i*n//4 cover all indices; chunk sizes can differ by one.'),
 10: ('Czy usunięcie casefold zmieni wynik?|Does removing casefold change the result?',
      'Tak dla różnych wielkości liter: Python i python stałyby się różnymi tokenami.|Yes for '
      'mixed case: Python and python would become different tokens.'),
 11: ('Po co task_done znajduje się w finally?|Why is task_done in finally?',
      'Każdy odebrany element ma dostać potwierdzenie także przy wyjściu przez return dla None '
      'albo przy wyjątku.|Every received item must be acknowledged, including a return for None or '
      'an exception.'),
 12: ('Jak uczciwie porównać warianty?|How do we compare the modes fairly?',
      'Ta sama liczba wywołań i danych, brak innych pokazów w tle, podanie środowiska i kosztów '
      'wliczonych do pomiaru. Jeden pomiar nie jest uniwersalną regułą.|Use equal calls and data, '
      'no competing demos, and disclose the environment and included overhead. One run is not a '
      'universal rule.'),
 13: ("Czy map zwróci najpierw wynik najszybszego zadania?|Does map return the fastest task's "
      'result first?',
      'Wyniki map mają kolejność wejścia. Kolejność rzeczywistego ukończenia może być inna.|map '
      'results follow input order. Actual completion order can differ.'),
 14: ('Czy ten przykład skopiuje Twoje dokumenty?|Does this example copy your documents?',
      'Nie. Tworzy własne cztery pliki w katalogu tymczasowym, kopiuje je do drugiego podkatalogu '
      'i sprząta po sobie.|No. It creates four temporary files, copies them to another '
      'subdirectory and cleans up.'),
 15: ('Czy zbiór visited oznacza zawsze udane pobranie?|Does the visited set always mean '
      'successful retrieval?',
      'Tutaj oznacza adresy zarezerwowane do pracy. Produkcyjny crawler rozróżniałby zlecone, '
      'udane i błędne pobrania.|Here it means URLs reserved for work. A production crawler would '
      'distinguish scheduled, successful and failed fetches.'),
 16: ('Dlaczego czytamy rb, a nie zwykły tekst?|Why read rb rather than text?',
      'Hash ma dotyczyć dokładnych bajtów. Dekodowanie tekstu i zmiany zakończeń linii mogłyby '
      'zmienić data.|The hash must cover exact bytes. Text decoding and newline conversion could '
      'change the data.'),
 17: ('Dlaczego poll poprzedza recv w rodzicu?|Why does poll precede recv in the parent?',
      'Pozwala ograniczyć czekanie na odpowiedź do 10 sekund; dopiero gotową wiadomość odbieramy '
      'recv.|It bounds the response wait to ten seconds; recv then receives the ready message.'),
 18: ('Czy odmówioną wypłatę uwzględniamy w historii zmian salda?|Is a declined withdrawal '
      'included in balance-change history?',
      'Nie. Historia kontrolna obejmuje wyłącznie zaakceptowane zmiany; odmowa jest osobnym '
      'komunikatem.|No. Reconciliation history includes accepted changes only; a decline is a '
      'separate message.'),
 19: ('Czy więcej wątków oznacza dokładniejszą analizę AI?|Do more threads make the AI analysis '
      'more accurate?',
      'Nie. Zmieniamy liczbę równoczesnych oczekiwań. Etykiety są tu symulowane i nie wynikają ze '
      'znaczenia tekstu.|No. Only the number of overlapping waits changes. Labels are simulated, '
      'not derived from text meaning.'),
 20: ('Czy użyliśmy tych samych obrazów w obu wariantach?|Did both modes use the same images?',
      'Tak. Obrazy powstają raz przed pomiarem, a filtr tworzy nowe listy zamiast zmieniać '
      'wejściowe piksele.|Yes. Images are created once before timing; the filter builds new lists '
      'instead of mutating inputs.')}
