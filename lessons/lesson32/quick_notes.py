"""Independent presentation narrative, rather than concatenated line annotations."""
import ast

from line_notes import pair


# Each marker begins a new coherent block within the named function.
# Notes are deliberately short enough to say aloud during a presentation.
PLANS = {
    'create_product': [
        (None, 'Wejście i sesja / Input and session', 'Odczytujemy JSON i sprawdzamy nazwę oraz cenę. Każde żądanie dostaje własną sesję i transakcję.', 'Read JSON and validate name and price. Each request gets its own session and transaction.'),
        ('product = Product(', 'Zapis i ID / Insert and ID', 'Tworzymy produkt. add rejestruje go w sesji; flush wysyła INSERT i pobiera ID. Wyjście z begin zatwierdza zapis.', 'Construct a product. add tracks it; flush sends INSERT and retrieves its ID. Exiting begin commits the write.'),
        ('return web.json_response', 'Odpowiedź 201 / Response 201', 'Zwracamy słownik produktu jako JSON ze statusem 201: nowy zasób został utworzony.', 'Return the product dictionary as JSON with status 201: a new resource was created.'),
    ],
    'list_products': [
        (None, 'Zapytanie SELECT / SELECT query', 'Otwieramy sesję i budujemy SELECT. order_by ustala kolejność; offset i limit, jeśli występują, wybierają stronę. Sam opis zapytania nie odczytuje bazy.', 'Open a session and build SELECT. order_by defines order; offset and limit, when present, select a page. Building the query does not read the database.'),
        ('result = await session.execute', 'Baza → lista JSON / Database → JSON list', 'execute wykonuje zapytanie. scalars().all() zbiera obiekty Product. to_dict zmienia każdy z nich na słownik, a handler zwraca listę JSON.', 'execute runs the query. scalars().all() collects Product objects. to_dict converts each into a dictionary, and the handler returns a JSON list.'),
    ],
    'get_product': [
        (None, 'ID i odczyt / ID and retrieval', 'Z URL pobieramy dodatnie ID. Otwieramy sesję i szukamy produktu: get po kluczu głównym albo SELECT z JOIN w zadaniu 20.', 'Read a positive ID from the URL. Open a session and find the product: get by primary key, or SELECT with JOIN in task 20.'),
        ('if product is None:', 'Wynik albo 404 / Result or 404', 'Brak rekordu daje 404. Istniejący produkt zamieniamy na słownik i zwracamy jako JSON.', 'A missing row gives 404. Convert an existing product into a dictionary and return JSON.'),
    ],
    'update_product': [
        (None, 'PATCH: dane wejściowe / PATCH input', 'Pobieramy ID oraz JSON. partial=True pozwala zmienić samą nazwę lub samą cenę, bez przesyłania całego produktu.', 'Read the ID and JSON. partial=True allows changing only name or price without submitting the entire product.'),
        ('async with request.app[SESSION]', 'Produkt w transakcji / Product in a transaction', 'Własna sesja obejmuje odczyt i zapis. Pobieramy produkt; jeśli go nie ma, przerywamy żądanie odpowiedzią 404.', 'A dedicated session covers reading and writing. Retrieve the product; if absent, stop with 404.'),
        ('if "name" in data:', 'Zmiana pól i zapis / Change fields and save', 'Zmieniamy tylko obecne klucze JSON. Dzięki temu price=0 też działa. flush wysyła UPDATE, a poprawne wyjście z begin zatwierdza zmianę.', 'Change only keys present in JSON, so price=0 works too. flush sends UPDATE; successful exit from begin commits the change.'),
        ('return web.json_response', 'Zaktualizowany produkt / Updated product', 'Oddajemy nowe dane jako JSON. Kolejny GET w pokazie potwierdzi, że cena 999 została zapisana w bazie.', 'Return updated data as JSON. The next GET in the demo confirms that price 999 was saved in the database.'),
    ],
    'delete_product': [
        (None, 'Znajdź i usuń / Find and delete', 'W transakcji pobieramy produkt. Brak daje 404; await session.delete oznacza istniejący rekord do usunięcia. Wyjście z begin zatwierdza operację.', 'Retrieve the product in a transaction. Absence gives 404; await session.delete marks an existing row for deletion. Exiting begin commits it.'),
        ('return web.Response', '204 bez treści / Empty 204', 'Zwracamy 204 bez body. Późniejszy GET tego samego ID daje 404 — produktu już nie ma.', 'Return 204 with no body. A subsequent GET of the same ID gives 404: the product is gone.'),
    ],
    'transfer': [
        (None, 'Walidacja przelewu / Validate transfer', 'JSON musi podać dwa różne konta i dodatnią kwotę całkowitą. Błędne dane odrzucamy przed zmianą sald.', 'JSON must provide two different accounts and a positive integer amount. Reject invalid input before changing balances.'),
        ('async with request.app[SESSION]', 'Transakcja i blokady / Transaction and locks', 'Jedna transakcja obejmuje oba konta. SELECT FOR UPDATE blokuje wiersze na czas przelewu. Inny przelew na tych kontach poczeka.', 'One transaction covers both accounts. SELECT FOR UPDATE locks their rows during the transfer. Another transfer involving them waits.'),
        ('if len(by_id)', 'Konta i dostępne środki / Accounts and funds', 'Sprawdzamy istnienie obu kont oraz saldo źródła. Brak konta daje 404; zbyt duża kwota daje 409.', 'Check that both accounts exist and the source has enough funds. Missing accounts give 404; insufficient funds give 409.'),
        ('source.balance -=', 'Odjęcie i celowa awaria / Debit and deliberate failure', 'Odejmujemy kwotę i wykonujemy flush. Dla kwoty 13 celowo zgłaszamy błąd: rollback wycofa już wysłany UPDATE.', 'Debit the source and flush. Amount 13 deliberately raises an error: rollback reverses the UPDATE already sent.'),
        ('target.balance +=', 'Dodanie i commit / Credit and commit', 'Dodajemy kwotę odbiorcy i wpis historii. Poprawne wyjście zatwierdza wszystko razem. Suma sald pozostaje stała.', 'Credit the recipient and add a history record. Successful exit commits everything together. Total balance stays constant.'),
    ],
    'balances': [(None, 'Sprawdzenie sald / Inspect balances', 'Odczytujemy konta i zwracamy słownik ID → saldo. Ten odczyt potwierdza, że po rollbacku salda się nie zmieniły.', 'Read accounts and return an ID → balance dictionary. This verifies that rollback left balances unchanged.')],
    'chat': [
        (None, 'Prompt i walidacja / Prompt and validation', 'Odczytujemy JSON i wymagamy niepustego tekstu prompt. Niepoprawne dane dostają 400.', 'Read JSON and require nonempty prompt text. Invalid input receives 400.'),
        ('with span(', 'Czekanie bez blokowania / Wait without blocking', 'await asyncio.sleep(3) symuluje oczekiwanie na AI i oddaje sterowanie pętli. Inne żądania mogą działać. Po czekaniu zwracamy odpowiedź JSON.', 'await asyncio.sleep(3) simulates waiting for AI and yields to the loop. Other requests can run. Return a JSON response after the wait.'),
    ],
    'status': [(None, 'Szybka odpowiedź statusu / Fast status response', 'Handler od razu zwraca status OK. W pokazie odpowiada, gdy handler czatu nadal czeka.', 'The handler immediately returns status OK. In the demo it responds while the chat handler is still waiting.')],
    'create_app': [(None, 'Budowa aplikacji / Build the application', 'Tworzymy aplikację i zapisujemy fabrykę sesji. setup_routes z routes.py rejestruje adresy. Zwracamy gotową aplikację; serwer wystartuje później.', 'Create the application and store the session factory. setup_routes from routes.py registers URLs. Return the configured application; the server starts later.')],
}


def quick_steps(record):
    """Return short, authored blocks with ranges resolved against current source."""
    source=record['steps']['source']
    lines=source.splitlines()
    tree=ast.parse(source)
    steps=[]

    def add(name,start,end,body):
        steps.append(dict(id=f'quick-{len(steps)+1}',name=name,start=start,end=end,
                          details=[],body=body))

    entry=next(n for n in tree.body if isinstance(n,ast.If))
    add('Start programu / Program entry',entry.lineno,entry.end_lineno,
        pair('Warunek __main__ uruchamia pokaz tylko przy wykonaniu pliku. launch mierzy czas, a asyncio.run(main()) uruchamia główną korutynę.', 'The __main__ guard starts the demo only when executing the file. launch measures time; asyncio.run(main()) runs the main coroutine.'))
    imports=[]
    for node in tree.body:
        if not isinstance(node,(ast.Import,ast.ImportFrom)):
            break
        imports.append(node)
    if imports:
        add('Narzędzia / Tools',imports[0].lineno,imports[-1].end_lineno,
            pair('Importy dostarczają asyncio, serwer HTTP i narzędzia bazy potrzebne w tym pliku. Pomocniki przygotowują pokaz i zapisują zdarzenia; właściwa logika jest w handlerach poniżej.', 'Imports provide asyncio, HTTP server and database tools needed in this file. Helpers prepare the demo and record events; the actual logic is in the handlers below.'))
    models=[n for n in tree.body if isinstance(n,ast.ClassDef)]
    if models:
        text={
            16: pair('Base rejestruje modele. Account przechowuje ID i saldo w groszach; Transfer zapisuje historię. Zmiany obu modeli należą do jednej transakcji przelewu.', 'Base registers models. Account stores ID and balance in cents; Transfer records history. Changes to both belong to the same transfer transaction.'),
            20: pair('Product ma user_id wskazujące na User.id. Ten klucz obcy łączy produkt z twórcą i pozwala wykonać JOIN.', 'Product.user_id points to User.id. This foreign key links a product to its creator and enables JOIN.'),
        }.get(record['number'],pair('Base rejestruje tabelę Product: id to klucz główny, name to tekst do 100 znaków, price to cena w groszach. to_dict przygotowuje zwykły słownik do JSON.', 'Base registers the Product table: id is the primary key, name is text up to 100 characters, and price uses cents. to_dict prepares a plain dictionary for JSON.'))
        add('Model danych / Data model',models[0].lineno,models[-1].end_lineno,text)

    functions=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    main=next(n for n in functions if n.name=='main')
    split=next((n.lineno for n in ast.walk(main) if isinstance(n,ast.Await) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='demo'),None)
    setup=pair('main przygotowuje aplikację oraz trasy. Dla zadań z bazą database(Base) tworzy tabele i fabrykę sesji w osobnym schemacie. Rejestracja trasy nie wywołuje jeszcze handlera.', 'main prepares the application and routes. For database exercises, database(Base) creates tables and a session factory in a separate schema. Registering a route does not call the handler yet.')
    if record['number']==7:
        setup=pair('database(Base) tworzy rzeczywistą tabelę w PostgreSQL. Pokaz wypisuje nazwy kolumn i jednostkę ceny. Przy wyjściu usuwa tymczasowy schemat.', 'database(Base) creates a real PostgreSQL table. The demo reports column names and the price unit. Exiting removes its temporary schema.')
    if record['number']==18:
        setup=pair('Uruchamiamy serwer i klienta. create_task wysyła czat, po 0,1 s pytamy o status, a na końcu czekamy na czat. Status powinien odpowiedzieć pierwszy.', 'Start a server and client. create_task sends chat; after 0.1 s request status, then await chat. Status should respond first.')
    add('Przygotowanie pokazu / Prepare the demo',main.lineno,split-1 if split else main.end_lineno,setup)
    if split:
        add('Żądania i oczekiwany wynik / Requests and expected result',split,main.end_lineno,
            pair('demo wysyła pokazane żądania HTTP po kolei i sprawdza statusy. '+record['takeaway']['pl'], 'demo sends the shown HTTP requests sequentially and checks their statuses. '+record['takeaway']['en']))

    for node in functions:
        if node.name=='main':
            continue
        plan=PLANS[node.name]
        if node.name=='list_products' and record['number']==17:
            plan=[(None,'Parametry strony / Page parameters', 'page i limit zamieniamy na dodatnie liczby. offset = (page - 1) * limit określa, ile rekordów pominąć. ORDER BY zapewnia stałą kolejność.', 'Convert page and limit to positive integers. offset = (page - 1) * limit determines how many rows to skip. ORDER BY provides stable ordering.'), *plan[1:]]
        if node.name=='get_product' and record['number']==20:
            plan=[(None,'SELECT z JOIN / SELECT with JOIN', 'Pobieramy ID z URL. select(Product, User).join(User) buduje zapytanie o produkt i twórcę; execute wysyła je do bazy.', 'Read the URL ID. select(Product, User).join(User) builds a query for product and creator; execute sends it to the database.'),('row = result.one_or_none()', 'Para obiektów → JSON / Object pair → JSON', 'Brak wiersza daje 404. Wiersz rozpakowujemy na product i user; JSON zawiera dane produktu i user.username jako creator.', 'An absent row gives 404. Unpack the row into product and user; JSON includes product data and user.username as creator.')]
        starts=[node.lineno]
        for marker,*_ in plan[1:]:
            matches=[i for i in range(starts[-1]+1,node.end_lineno+1) if lines[i-1].strip().startswith(marker)]
            if not matches:
                raise ValueError(f'Missing quick-note marker: {node.name}: {marker}')
            starts.append(matches[0])
        for index,(_,title,pl,en) in enumerate(plan):
            end=starts[index+1]-1 if index+1<len(starts) else node.end_lineno
            add(title,starts[index],end,pair(pl,en))
    if len(steps)>20:
        raise ValueError(f'Quick presentation exceeds 20 slides: task {record["number"]}')
    return steps
