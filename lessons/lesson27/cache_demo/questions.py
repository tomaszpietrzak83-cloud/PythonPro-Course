"""Bilingual oral-exam questions, followed by simpler practice questions.

The first two entries appear immediately. The remaining entries are revealed
one at a time under an opened answer; no questions are selected at random.
"""


def question(en_question, pl_question, en_answer, pl_answer):
    """Give every entry the same shape for the independent browser module."""
    return {"question": {"en": en_question, "pl": pl_question},
            "answer": {"en": en_answer, "pl": pl_answer}}


QUESTION_BANK = {
    1: [
        question("Why cannot another Python process read this LocMem entry?", "Dlaczego inny proces Python nie odczyta tego wpisu LocMem?",
                 "LocMem stores entries in this process's RAM. Another Django process has its own store, even if its cache configuration uses the same location name.", "LocMem przechowuje wpisy w RAM tego procesu. Inny proces Django ma własny magazyn, nawet jeśli konfiguracja cache używa tej samej nazwy lokalizacji."),
        question("What happens to LocMem entries when I stop and restart this server?", "Co dzieje się z wpisami LocMem po zatrzymaniu i ponownym uruchomieniu tego serwera?",
                 "They disappear with the stopped process. The new process starts with an empty memory cache, so its first read cannot reuse the old entries.", "Znikają razem z zatrzymanym procesem. Nowy proces rozpoczyna z pustym cache pamięci, więc pierwszy odczyt nie wykorzysta starych wpisów."),
        question("Where does LocMem store its data?", "Gdzie LocMem przechowuje dane?", "In the Python process's memory, not in the SQLite database.", "W pamięci procesu Python, a nie w bazie SQLite."),
        question("Which setting chooses the cache implementation?", "Które ustawienie wybiera implementację cache?", "The BACKEND entry inside the CACHES dictionary in settings.py.", "Wpis BACKEND w słowniku CACHES w settings.py."),
        question("Does checking the backend automatically cache every view?", "Czy sprawdzenie backendu automatycznie cachuje każdy widok?", "No. A view must use cache_page or explicit operations such as cache.set and cache.get.", "Nie. Widok musi używać cache_page albo jawnych operacji, takich jak cache.set i cache.get."),
    ],
    2: [
        question("Which request does the toolbar describe?", "Którego żądania dotyczy toolbar?", "It describes its captured or selected request. The initial HTML page and later demo POST actions are different requests; the initial page's Cache panel does not automatically represent every later click.", "Opisuje przechwycone lub wybrane żądanie. Początkowa strona HTML i późniejsze operacje POST demonstracji to różne żądania; panel Cache początkowej strony nie opisuje automatycznie każdego kolejnego kliknięcia."),
        question("Why show both SQL counts and cache results?", "Dlaczego pokazujemy zarówno liczbę zapytań SQL, jak i wyniki cache?", "Together they show what work was avoided. A full-response HIT can skip the view's queries, while a selective-cache HIT still executes the simple queries.", "Razem pokazują, jakiej pracy uniknięto. HIT całej odpowiedzi może pominąć zapytania widoku, natomiast HIT cache częściowego nadal wykonuje proste zapytania."),
        question("Which toolbar panel helps inspect cache operations?", "Który panel toolbaru pomaga sprawdzać operacje cache?", "The Cache panel.", "Panel Cache."),
        question("Is Debug Toolbar the cache backend?", "Czy Debug Toolbar jest backendem cache?", "No. It observes operations; LocMem, FileBased or Redis stores the cached entries.", "Nie. Obserwuje operacje; wpisy przechowuje LocMem, FileBased lub Redis."),
        question("Does a short duration prove a cache HIT?", "Czy krótki czas dowodzi trafienia HIT?", "No. Use the recorded HIT/MISS result and cache diagnostics. An uncached operation can also be fast.", "Nie. Sprawdź zapisany wynik HIT/MISS i diagnostykę cache. Operacja bez cache też może być szybka."),
    ],
    3: [
        question("Does the database query execute on HIT?", "Czy przy HIT wykonuje się zapytanie do bazy?", "The product query inside this cached view does not execute on HIT: cache_page returns the stored response. Other parts of request handling can still do their own work.", "Zapytanie produktów wewnątrz tego widoku nie wykonuje się przy HIT: cache_page zwraca zapisaną odpowiedź. Pozostałe części obsługi żądania mogą nadal wykonywać własną pracę."),
        question("Why can changed products remain invisible until expiration?", "Dlaczego zmienione produkty mogą być niewidoczne do wygaśnięcia?", "The cache contains an older complete response. A database change does not automatically invalidate that response in this exercise; expiration or a fresh demo namespace causes a new query.", "Cache zawiera starszą, kompletną odpowiedź. Zmiana w bazie nie unieważnia jej automatycznie w tym ćwiczeniu; wygaśnięcie lub nowa przestrzeń demonstracji powoduje nowe zapytanie."),
        question("What does MISS mean?", "Co oznacza MISS?", "No usable cached response was found, so the view must execute.", "Nie znaleziono użytecznej odpowiedzi w cache, więc widok musi się wykonać."),
        question("What does HIT mean?", "Co oznacza HIT?", "A valid cached response was found and reused.", "Znaleziono ważną odpowiedź w cache i użyto jej ponownie."),
        question("Does every HIT start a fresh lifetime?", "Czy każdy HIT rozpoczyna nowy czas ważności?", "No. This demo keeps the original expiration deadline until a new response is generated.", "Nie. Demonstracja zachowuje pierwotny termin wygaśnięcia aż do wygenerowania nowej odpowiedzi."),
    ],
    4: [
        question("What does cache.get return after expiration?", "Co zwraca cache.get po wygaśnięciu?", "Without an explicit default, it returns None. The entry is no longer usable; reading it does not recreate it.", "Bez jawnie podanej wartości domyślnej zwraca None. Wpis nie nadaje się już do użycia; odczyt nie tworzy go ponownie."),
        question("Why can None be ambiguous in a cache lookup?", "Dlaczego None może być niejednoznaczne przy odczycie cache?", "None may mean a missing entry, but it can also be the value you stored. If you need to distinguish them, pass a unique sentinel object as cache.get's default.", "None może oznaczać brak wpisu, ale może też być zapisaną wartością. Jeśli musisz je rozróżnić, przekaż unikalny obiekt znacznikowy jako wartość domyślną cache.get."),
        question("Which method stores a value?", "Która metoda zapisuje wartość?", "cache.set(key, value, timeout).", "cache.set(key, value, timeout)."),
        question("What is a cache key?", "Czym jest klucz cache?", "A name identifying the stored value, such as my_key.", "Nazwą identyfikującą zapisaną wartość, na przykład my_key."),
        question("Does reading the value extend its lifetime here?", "Czy odczyt wartości przedłuża tu jej ważność?", "No. Only a new write starts a new lifetime in this exercise.", "Nie. W tym ćwiczeniu dopiero nowy zapis rozpoczyna nowy czas ważności."),
    ],
    5: [
        question("How does delete(key) differ from clear()?", "Czym delete(key) różni się od clear()?", "delete removes one key. clear removes every entry in the selected cache store. This demonstration gives clear its own sandbox so it cannot clear other tasks.", "delete usuwa jeden klucz. clear usuwa wszystkie wpisy wybranego magazynu cache. Demonstracja daje clear osobny magazyn, aby nie czyściło innych zadań."),
        question("Is there a universal built-in manage.py command for clearing cache?", "Czy istnieje uniwersalna wbudowana komenda manage.py do czyszczenia cache?", "No. Standard Django provides cache.clear(), which you can call in the Django shell. A project may add its own management command.", "Nie. Standardowe Django udostępnia cache.clear(), które można wywołać w Django shell. Projekt może dodać własną komendę zarządzającą."),
        question("What happens to the two sample values after Clear?", "Co dzieje się z dwiema przykładowymi wartościami po Clear?", "Both reads return None because the sandbox no longer contains those keys.", "Oba odczyty zwracają None, ponieważ magazyn zadania nie zawiera już tych kluczy."),
        question("Does clearing this sandbox delete database rows?", "Czy czyszczenie tego magazynu usuwa rekordy bazy?", "No. Cached entries and database records are different data stores.", "Nie. Wpisy cache i rekordy bazy znajdują się w różnych magazynach."),
        question("Must I wait for TTL after explicitly clearing a key?", "Czy po jawnym usunięciu klucza muszę czekać na TTL?", "No. The key is immediately unavailable to the next lookup.", "Nie. Klucz od razu jest niedostępny przy następnym odczycie."),
    ],
    6: [
        question("Does an existing file prove that its entry is still valid?", "Czy obecność pliku dowodzi ważności wpisu?", "No. A file may contain an expired entry. The backend checks validity when accessing the entry; physical file removal is not the same event as logical expiration.", "Nie. Plik może zawierać wygasły wpis. Backend sprawdza ważność przy dostępie; fizyczne usunięcie pliku i logiczne wygaśnięcie to różne zdarzenia."),
        question("Why are cache files not readable product JSON?", "Dlaczego pliki cache nie są czytelnym JSON produktów?", "The backend writes its own serialized cache representation, including expiration information. A full-view entry contains the cached response rather than just the product list.", "Backend zapisuje własną serializowaną reprezentację cache, wraz z informacją o wygaśnięciu. Wpis całego widoku zawiera odpowiedź, a nie tylko listę produktów."),
        question("Where does this backend store entries?", "Gdzie ten backend przechowuje wpisy?", "In the configured cache directory on disk.", "W skonfigurowanym katalogu cache na dysku."),
        question("Which setting identifies that directory?", "Które ustawienie wskazuje ten katalog?", "LOCATION in the selected CACHES entry.", "LOCATION we wpisie wybranego cache w CACHES."),
        question("Can a valid file entry survive a Django process restart?", "Czy ważny wpis plikowy może przetrwać restart procesu Django?", "Yes, if the same directory and keys are used and the entry has not expired or been removed.", "Tak, jeśli używane są ten sam katalog i klucze, a wpis nie wygasł ani nie został usunięty."),
    ],
    7: [
        question("Which part still executes on HIT?", "Która część nadal wykonuje się przy HIT?", "The simple product count and name queries execute on every request. Only the expensive statistics result is reused from cache.", "Proste zapytania o liczbę produktów i ich nazwy wykonują się przy każdym żądaniu. Tylko wynik kosztownych statystyk pochodzi ponownie z cache."),
        question("Why can simple data be fresh while statistics are older?", "Dlaczego proste dane mogą być świeże, a statystyki starsze?", "They follow different paths: simple data is read from the database now, while statistics may come from an earlier calculation. This is a deliberate trade-off of selective caching.", "Korzystają z różnych ścieżek: proste dane są teraz odczytywane z bazy, a statystyki mogą pochodzić z wcześniejszych obliczeń. To świadomy kompromis cache częściowego."),
        question("What does time.sleep(3) simulate?", "Co symuluje time.sleep(3)?", "An expensive calculation taking about three seconds.", "Kosztowne obliczenia trwające około trzech sekund."),
        question("Is the entire response cached here?", "Czy cachowana jest tutaj cała odpowiedź?", "No. Only the complex statistics are stored using the low-level cache API.", "Nie. Niskopoziomowe API cache przechowuje tylko złożone statystyki."),
        question("When does the slow calculation run again?", "Kiedy wolne obliczenia wykonują się ponownie?", "On a MISS, for example after the statistics entry expires or the demo is reset.", "Przy MISS, na przykład po wygaśnięciu wpisu statystyk albo resecie demonstracji."),
    ],
    8: [
        question("Why can a list and a detail have different freshness?", "Dlaczego lista i szczegóły mogą mieć różną świeżość?", "They are stored under independent keys and lifetimes. One may expire while the other still contains an older valid response.", "Są przechowywane pod niezależnymi kluczami i z różnymi czasami ważności. Jeden wpis może wygasnąć, podczas gdy drugi nadal zawiera starszą, ważną odpowiedź."),
        question("Why are create, update and destroy not cached?", "Dlaczego create, update i destroy nie są cachowane?", "These operations change data. Reusing an old response would not perform the new requested change. This exercise caches reads and executes writes normally.", "Te operacje zmieniają dane. Ponowne użycie starej odpowiedzi nie wykonałoby nowej żądanej zmiany. Ćwiczenie cachuje odczyty, a zapisy wykonuje normalnie."),
        question("What does list return?", "Co zwraca list?", "A collection of clients; the demo restricts it to its dedicated client.", "Kolekcję klientów; demonstracja ogranicza ją do własnego klienta."),
        question("What does retrieve return?", "Co zwraca retrieve?", "The details of one client identified by its ID.", "Szczegóły jednego klienta wskazanego przez ID."),
        question("What are the homework lifetimes?", "Jakie czasy ważności wymaga zadanie?", "600 seconds for the list and 60 seconds for details. Quick demo uses shorter times, shown beside the inputs.", "600 sekund dla listy i 60 sekund dla szczegółów. Szybki pokaz używa krótszych czasów podanych przy polach."),
    ],
    9: [
        question("Why does PATCH invalidate detail but leave the cached list?", "Dlaczego PATCH unieważnia szczegóły, ale pozostawia listę w cache?", "perform_update saves the client and deletes only its detail key. The list has a separate cache_page entry that this method does not invalidate. That is why its old city can remain visible.", "perform_update zapisuje klienta i usuwa tylko jego klucz szczegółów. Lista ma osobny wpis cache_page, którego ta metoda nie unieważnia. Dlatego może nadal pokazywać stare miasto."),
        question("Why should the key be deleted after a successful save?", "Dlaczego klucz należy usuwać po udanym zapisie?", "The cache must be invalidated for a change that actually succeeded. Saving first also ensures the next uncached read can fetch the updated database value.", "Cache należy unieważnić dla zmiany, która rzeczywiście się powiodła. Zapis jako pierwszy pozwala też następnemu odczytowi bez cache pobrać zaktualizowaną wartość z bazy."),
        question("Which method deletes this client's detail key?", "Która metoda usuwa klucz szczegółów tego klienta?", "perform_update calls self.detail_cache.delete with the client's detail key.", "perform_update wywołuje self.detail_cache.delete z kluczem szczegółów klienta."),
        question("Must the next detail read wait for the old TTL?", "Czy następny odczyt szczegółów musi czekać na stary TTL?", "No. Deleting the key makes the next detail read a MISS immediately.", "Nie. Usunięcie klucza od razu powoduje MISS przy następnym odczycie szczegółów."),
        question("Does invalidation delete the client itself?", "Czy unieważnienie usuwa samego klienta?", "No. It deletes a cached copy; the updated database row remains.", "Nie. Usuwa kopię w cache; zaktualizowany rekord pozostaje w bazie."),
    ],
    10: [
        question("How is Redis different from process-local memory?", "Czym Redis różni się od pamięci pojedynczego procesu?", "Redis is a separate service. Multiple Django processes can access the same Redis database and keys. LocMem entries are private to one process.", "Redis jest osobną usługą. Wiele procesów Django może korzystać z tej samej bazy Redis i tych samych kluczy. Wpisy LocMem są prywatne dla jednego procesu."),
        question("Does stopping the Django server stop Redis too?", "Czy zatrzymanie serwera Django zatrzymuje też Redis?", "No. This controller manages the three Django processes. Redis continues independently, so unexpired Redis entries can survive a Django restart.", "Nie. Panel steruje trzema procesami Django. Redis działa niezależnie, więc niewygasłe wpisy Redis mogą przetrwać restart Django."),
        question("What does PONG confirm?", "Co potwierdza PONG?", "The real Redis service answered the connection probe.", "Rzeczywista usługa Redis odpowiedziała na test połączenia."),
        question("What does TTL mean?", "Co oznacza TTL?", "Time to live: how long an entry remains valid before expiration.", "Time to live: czas, przez który wpis pozostaje ważny przed wygaśnięciem."),
        question("What does this demo show if Redis is unavailable?", "Co pokazuje demonstracja, gdy Redis jest niedostępny?", "A connection error. It does not silently switch to a different cache backend.", "Błąd połączenia. Nie przełącza się po cichu na inny backend cache."),
    ],
}
