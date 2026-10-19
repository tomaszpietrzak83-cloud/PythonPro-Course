"""Small bilingual explanations before the transaction demonstration."""

PAGES = [
    {
        "pl": [
            "Dlaczego to zadanie jest trudne?",
            "Wyobraź sobie, że Django tworzy zamówienie, a worker ma je przetworzyć. Najpierw musimy zatwierdzić zapis w bazie, a dopiero potem zlecić pracę Celery. W naszym ćwiczeniu zamówienie zastępuje ProcessingRecord z tekstem.",
            "Django i worker działają w osobnych procesach i korzystają z osobnych połączeń z bazą. Worker może nie widzieć rekordu, którego transakcja jeszcze nie została zatwierdzona.",
            "objects.create() tworzy rekord wewnątrz transakcji. To nie jest jeszcze jej ostateczne zatwierdzenie.",
        ],
        "en": [
            "Why is this exercise difficult?",
            "Imagine Django creating an order and a worker processing it. First we must commit the database write, then submit work to Celery. In this exercise, a ProcessingRecord containing text stands in for the order.",
            "Django and the worker run in separate processes with separate database connections. The worker may not see a row whose transaction has not committed yet.",
            "objects.create() creates a row inside the transaction. This is not yet its final commit.",
        ],
    },
    {
        "pl": [
            "atomic(): zapis jako jedna transakcja",
            "with transaction.atomic(): obejmuje operacje, które mają zostać zatwierdzone razem albo wycofane razem. W tym bloku tworzymy ProcessingRecord.objects.create(text=...).",
            "Poprawne wyjście z najbardziej zewnętrznego bloku atomic zatwierdza transakcję — COMMIT. Wyjątek wychodzący z bloku powoduje jej wycofanie — ROLLBACK.",
            "Jeśli atomic jest zagnieżdżone, koniec wewnętrznego bloku nie oznacza jeszcze COMMIT całej transakcji.",
        ],
        "en": [
            "atomic(): one transaction",
            "with transaction.atomic(): groups operations that should commit together or roll back together. Inside this block we call ProcessingRecord.objects.create(text=...).",
            "Successfully leaving the outermost atomic block commits the transaction — COMMIT. An exception escaping the block causes a rollback — ROLLBACK.",
            "With nested atomic blocks, leaving an inner block does not yet commit the whole transaction.",
        ],
    },
    {
        "pl": [
            "Pułapka: .delay() przed COMMIT",
            "Gdybyśmy wywołali process_record.delay(record.pk) bezpośrednio po objects.create(), nadal wewnątrz atomic(), wiadomość mogłaby dotrzeć do workera przed zatwierdzeniem rekordu.",
            "Worker próbowałby pobrać rekord po ID. Jego połączenie może go jeszcze nie widzieć, więc odczyt mógłby się nie udać. Dodatkowo późniejszy rollback usunąłby rekord, ale nie cofnął wysłanej wiadomości.",
            "To problem kolejności zdarzeń. Czasami kod zadziała, a czasami zawiedzie — zależnie od tego, który proces będzie szybszy.",
        ],
        "en": [
            "The trap: .delay() before COMMIT",
            "If we called process_record.delay(record.pk) directly after objects.create(), still inside atomic(), the message could reach the worker before the row commits.",
            "The worker would try to load the row by ID. Its connection may not see it yet, so the read could fail. A later rollback would also discard the row without undoing the published message.",
            "This is an event-ordering problem. Code may sometimes work and sometimes fail, depending on which process is faster.",
        ],
    },
    {
        "pl": [
            "on_commit(): zapamiętaj, wykonaj później",
            "transaction.on_commit(lambda: process_record.delay(record.pk)) rejestruje callback, czyli funkcję do późniejszego wykonania. Django uruchomi ją dopiero po poprawnym zatwierdzeniu transakcji.",
            "lambda tworzy małą funkcję. Podczas jej rejestracji .delay() jeszcze się nie wykonuje. Dopiero wywołanie callbacku publikuje wiadomość Celery.",
            "Callback zarejestrowany wewnątrz transakcji czeka na COMMIT. Poza transakcją on_commit wykona go od razu.",
        ],
        "en": [
            "on_commit(): remember now, execute later",
            "transaction.on_commit(lambda: process_record.delay(record.pk)) registers a callback: a function to execute later. Django runs it only after the transaction commits successfully.",
            "lambda creates a small function. Registering it does not execute .delay() yet. Calling the callback publishes the Celery message.",
            "A callback registered inside a transaction waits for COMMIT. Outside a transaction, on_commit runs it immediately.",
        ],
    },
    {
        "pl": [
            "Cały przebieg udanego wykonania",
            "1. Django tworzy rekord. 2. Rejestruje callback przez on_commit(). 3. Zatwierdza transakcję. 4. Callback publikuje zadanie. 5. Worker pobiera zatwierdzony rekord.",
            "Nasz worker zamienia text na wielkie litery, ustawia processed_at i zapisuje oba pola. Dla tekstu hello transaction zobaczysz wynik HELLO TRANSACTION oraz czas przetworzenia.",
            "Zapis wyniku przez workera jest osobną operacją w bazie, wykonywaną po transakcji tworzącej rekord.",
        ],
        "en": [
            "The complete successful flow",
            "1. Django creates a row. 2. It registers an on_commit() callback. 3. It commits the transaction. 4. The callback publishes a task. 5. The worker loads the committed row.",
            "Our worker uppercases text, sets processed_at and saves both fields. For hello transaction, the result is HELLO TRANSACTION together with the processing time.",
            "The worker's result write is a separate database operation after the record-creation transaction.",
        ],
    },
    {
        "pl": [
            "Dlaczego w aplikacji jest apply_async()?",
            "Callback w rzeczywistym kodzie wywołuje tasks.process_record.apply_async(args=[record.pk], task_id=task_id). Zleca tę samą pracę, którą można zlecić przez .delay(), ale pozwala podać dodatkowe opcje.",
            "record.pk jest ID rekordu w bazie. task_id jest osobnym identyfikatorem zadania Celery, przygotowanym wcześniej przez uuid.uuid4(). Widok zwraca go przeglądarce do obserwowania stanu i wyniku.",
            "ID rekordu odpowiada na pytanie: co przetwarzamy? task_id odpowiada: które wykonanie obserwujemy?",
        ],
        "en": [
            "Why does the app use apply_async()?",
            "The actual callback calls tasks.process_record.apply_async(args=[record.pk], task_id=task_id). It submits the same work as .delay(), while allowing extra options.",
            "record.pk is the database row ID. task_id is a separate Celery task identifier, allocated earlier with uuid.uuid4(). The view returns it to the browser for observing state and results.",
            "The row ID answers: what are we processing? task_id answers: which execution are we observing?",
        ],
    },
    {
        "pl": [
            "Rollback: ani rekordu, ani zlecenia",
            "W demonstracji rollback celowo zgłaszamy wyjątek wewnątrz atomic(). Django wycofuje nowy rekord i odrzuca callback on_commit(). Nic nie zostaje wysłane do workera.",
            "Porównaj oba warianty w przykładach: zwykłe zlecenie zapisuje i przetwarza tekst. Przykład rollback zwraca ROLLED_BACK, bez task_id, ponieważ zadanie Celery nie powstało.",
            "Przy rollback nie oczekujemy stanu FAILURE zadania. Nie ma zadania, którego wynik można sprawdzić.",
        ],
        "en": [
            "Rollback: neither a row nor a submission",
            "The rollback demonstration deliberately raises inside atomic(). Django rolls back the new row and discards the on_commit() callback. Nothing is sent to the worker.",
            "Compare both examples: normal submission saves and processes text. The rollback example returns ROLLED_BACK without a task_id because no Celery task was submitted.",
            "Rollback does not produce a task FAILURE. There is no task whose result could be queried.",
        ],
    },
    {
        "pl": [
            "Co gwarantuje to rozwiązanie?",
            "on_commit() pilnuje kolejności: najpierw COMMIT, potem publikacja zadania. Chroni przed zleceniem pracy nad niezatwierdzonym rekordem i pomija callback przy rollback.",
            "Nie łączy bazy i brokera w jedną transakcję. Jeśli zapis zostanie zatwierdzony, a publikacja wiadomości się nie powiedzie, rekord pozostanie w bazie bez zleconej pracy. Błąd callbacku nie wycofa wcześniejszego COMMIT.",
            "Zapamiętaj: zatwierdź rekord, potem zleć pracę. Teraz przejdź do przykładów, porównaj COMMIT i ROLLBACK, a następnie obejrzyj rzeczywisty kod krok po kroku.",
        ],
        "en": [
            "What does this solution guarantee?",
            "on_commit() enforces ordering: COMMIT first, then task publication. It protects against submitting work on an uncommitted row and discards the callback on rollback.",
            "It does not combine the database and broker into one transaction. If the write commits but publication fails, the row remains without submitted work. A callback error does not undo the earlier COMMIT.",
            "Remember: commit the row, then submit work. Continue to the examples, compare COMMIT and ROLLBACK, then inspect the actual code step by step.",
        ],
    },
]
