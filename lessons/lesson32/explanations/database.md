# Co robi pomocnik bazy danych?

Rozwiązania zadań są w osobnych plikach. Wspólny `examples/api_support.py`
przygotowuje rzeczywistą bazę PostgreSQL dla pokazu. Poniższa kolejność pozwala
prześledzić przejście od konfiguracji do sesji używanej przez handler.

1. `SESSION = web.AppKey('session_factory', async_sessionmaker)` tworzy klucz
   stanu aplikacji. Wartością pod tym kluczem będzie fabryka sesji. Klucz nie
   otwiera połączenia i nie przechowuje jednej sesji dla wszystkich żądań.
2. `@asynccontextmanager` zmienia funkcję z `yield` w asynchroniczny menedżer
   kontekstu, obsługiwany przez `async with database(Base) as factory`.
3. `database(base)` dostaje klasę bazową modeli konkretnego zadania.
   Jej `metadata` zawiera tabele zarejestrowane przez klasy Product, User lub Account.
4. `Path(__file__).resolve().parents[1] / '.env'` wskazuje `.env` lekcji 32,
   niezależnie od katalogu, z którego uruchomiono program.
5. `dotenv_values(...)` odczytuje lokalny plik do słownika. Nie wypisuje hasła.
6. `values.get('DATABASE_URL')` pobiera adres połączenia. Warunek poniżej odrzuca
   brak konfiguracji i bazę inną niż `lesson32`.
7. `uuid.uuid4().hex` daje losowy identyfikator. Prefiks `demo_` tworzy nazwę
   schematu przeznaczonego tylko dla jednego uruchomienia. Nazwa nie pochodzi od klienta HTTP.
8. `create_async_engine(url)` tworzy silnik administracyjny. Silnik zarządza
   połączeniami; sam nie jest pojedynczą sesją ORM.
9. `engine = None` przygotowuje zmienną do sprzątania również wtedy, gdy
   inicjalizacja przerwie się przed utworzeniem drugiego silnika.
10. `try` obejmuje inicjalizację i działanie pokazu; `finally` wykona się także
    przy wyjątku podczas normalnego rozwijania stosu.
11. `async with admin.begin() as connection` pobiera połączenie i otwiera transakcję.
12. `text(...)` opakowuje jawny SQL. `await connection.execute(...)` wysyła
    `CREATE SCHEMA` do PostgreSQL i czeka na odpowiedź. Poprawne wyjście z bloku zatwierdza DDL.
13. Drugi `create_async_engine` ustawia `search_path` na schemat tego pokazu.
    Dzięki temu tabela `products` z jednego zadania nie miesza się z tabelą innego pokazu.
14. `async with engine.begin()` otwiera transakcję na tym drugim silniku.
15. `await connection.run_sync(base.metadata.create_all)` uruchamia mechanizm
    tworzenia tabel SQLAlchemy przez mostek do asynchronicznego połączenia.
    Przekazujemy funkcję `create_all`, bez `()`. `run_sync` dostarcza jej połączenie.
    To nie jest ogólny sposób na bezpieczne uruchamianie blokującego kodu, np. `time.sleep`.
16. `event(...)` jedynie informuje dziennik, że przygotowanie bazy się skończyło.
17. `async_sessionmaker(engine, expire_on_commit=False)` buduje fabrykę.
    Jej każde wywołanie utworzy nową AsyncSession. `expire_on_commit=False`
    pozostawia załadowane atrybuty dostępne po commit, bez automatycznej próby ponownego odczytu.
18. `yield` przekazuje fabrykę do `main`. Funkcja `database` zatrzymuje się
    w tym miejscu na czas wykonywania całego bloku `async with` w zadaniu.
19. `main` zapisuje fabrykę w `app[SESSION]`. Handler odczytuje ją przez
    `request.app[SESSION]()` i tworzy własną sesję.
20. Wyjście z bloku `database` wraca za `yield` do `finally`.
21. `await engine.dispose()` zamyka pulę połączeń silnika pokazu po zamknięciu
    jego sesji i serwera. Żadne żądanie pokazu nie powinno już wtedy korzystać z bazy.
22. Silnik administracyjny wykonuje `DROP SCHEMA IF EXISTS ... CASCADE`.
    Usuwa tylko losowy schemat tego uruchomienia wraz z tabelami i danymi demonstracji.
23. `await admin.dispose()` zamyka drugą pulę. Ostatni `event` potwierdza sprzątanie.

Proces zabity wymuszenie nie musi wykonać `finally`. To ograniczenie pokazu:
może pozostać schemat `demo_...` w dedykowanej bazie `lesson32`.

## Handler i transakcja

`session.add(product)` zmienia stan sesji w pamięci. Nie wymaga `await`.
`await session.flush()` wykonuje SQL i może dostarczyć wygenerowane ID.
Wyjście z `async with session.begin()` wykonuje commit, a wyjątek opuszczający
ten blok powoduje rollback. W zadaniu 16 błąd następuje po flush, aby pokazać,
że także SQL już wykonany w transakcji może zostać wycofany.

Nie współdzielimy jednej AsyncSession pomiędzy równoczesnymi żądaniami.
Wspólna fabryka i wspólny silnik są właściwymi zasobami aplikacji.

## Serwer i klient pokazu

`web.AppRunner(app)` zarządza serwerem, `await runner.setup()` inicjalizuje go,
a `web.TCPSite(..., '127.0.0.1', 0)` prosi system o wolny lokalny port.
`await site.start()` rozpoczyna nasłuch. `runner.addresses[0]` podaje przydzielony
adres. `yield` oddaje go klientowi, a `finally: await runner.cleanup()` zatrzymuje serwer.

`demo(app, cases)` otwiera serwer i ClientSession. Pętla wysyła kolejne przypadki
przez `request(...)`. Ten pomocnik zapisuje metodę, URL i wejście, odczytuje body,
porównuje status HTTP z oczekiwanym i zwraca zdekodowany JSON lub tekst.
Odpowiedzi `204` pozostają pustym tekstem; klient nie próbuje parsować ich jako JSON.

`object_json` sprawdza strukturę JSON, `product_fields` sprawdza nazwę i cenę,
a `positive_id` zamienia parametr tekstowy na dodatnią liczbę. Kod tych funkcji
jest dostępny w zakładce `api_support.py` w „Cały kod”.
