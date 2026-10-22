"""Authoring source. Run explicitly to regenerate examples and reviewed material."""
import ast
import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
TASKS = []


def add(title, intro, observation, result, pitfall, question, answer, code, notes,
        adaptation="Dane są przygotowane do pokazu; komunikaty kodu są po angielsku.|Inputs are prepared for presentation; program messages are in English."):
    TASKS.append(dict(title=title, intro=intro, watch=observation,
                      takeaway=result, caveat=pitfall, question=question,
                      answer=answer, source=dedent(code).strip() + "\n",
                      notes=notes, adaptation=adaptation))


add("Pierwsza korutyna|First coroutine",
    "Korutyna to funkcja opisana przez async def. Jej wywołanie tworzy obiekt z pracą do wykonania. Dopiero pętla zdarzeń wykonuje tę pracę.|An async def function creates a coroutine object when called. An event loop executes that work.",
    "Przewidź: czy tekst pojawi się przed asyncio.run()? Uruchom i znajdź komunikat oraz czas całego programu.|Predict whether the greeting appears before asyncio.run(). Find the message and total duration.",
    "Wywołanie main() przekazuje obiekt korutyny do asyncio.run(). Komunikat pochodzi z wnętrza uruchomionej korutyny.|main() supplies a coroutine object to asyncio.run(). The greeting comes from its executed body.",
    "Nie wywołuj asyncio.run() wewnątrz już działającej pętli zdarzeń tego samego wątku.|Do not call asyncio.run() inside an already running event loop in the same thread.",
    "Co zwraca main() zanim ruszy pętla zdarzeń?|What does main() return before the event loop starts?",
    "Obiekt korutyny, a nie wynik jej wykonania. Jego kod jeszcze się nie wykonał.|A coroutine object, not its execution result. Its body has not run yet.",
    '''
    import asyncio
    from lab_support import event, launch

    async def main():
        event("log", "greeting", "Ready to learn asyncio!")

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"main": "To wejście do programu asynchronicznego. async def definiuje funkcję, a event zapisuje komunikat widoczny w pokazie. Nie ma tu oczekiwania ani wielu zadań.|This is the async entry point. async def defines the function; event records the displayed greeting. There is no waiting or concurrency here."})

add("Licznik i oddawanie sterowania|Counter and yielding control",
    "await oznacza: poczekaj na wynik obiektu awaitable. Gdy czekanie faktycznie zawiesza korutynę, event loop może obsłużyć inne gotowe zadania.|await waits for an awaitable result. When waiting suspends a coroutine, the loop can run other ready tasks.",
    "Liczby 1, 2, 3 powinny pojawić się w odstępach około sekundy.|Numbers 1, 2, 3 should appear about one second apart.",
    "Każda iteracja najpierw czeka sekundę, potem publikuje liczbę. Razem około 3 sekund.|Each iteration waits one second then publishes its number: about three seconds total.",
    "await nie musi zawsze zawieszać wykonania: gotowy wynik może być dostępny natychmiast. sleep(1) tutaj rzeczywiście zawiesza korutynę.|await need not always suspend execution: a result may already be ready. sleep(1) does suspend here.",
    "Dlaczego range(1, n + 1) zawiera n?|Why does range(1, n + 1) include n?",
    "Prawa granica range jest wyłączona. Dla n=3 range(1,4) daje 1,2,3.|The upper bound is excluded. For n=3, range(1,4) yields 1,2,3.",
    '''
    import asyncio
    from lab_support import event, launch

    async def counter(n):
        for number in range(1, n + 1):
            await asyncio.sleep(1)
            event("log", "counter", str(number))

    async def main():
        await counter(3)

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"counter": "n jest parametrem oznaczającym ostatnią liczbę. for bierze kolejne wartości z range. await sleep(1) zatrzymuje tylko tę korutynę; str(number) zmienia liczbę w tekst logu.|n is the final number. for takes values from range; await sleep(1) suspends this coroutine. str(number) converts the number to log text.", "main": "await counter(3) czeka na zakończenie wszystkich trzech iteracji. Nie uruchamiamy osobnego Task; wykonanie tej korutyny jest częścią oczekiwania main.|await counter(3) waits for all three iterations. No separate Task is created; this coroutine runs as part of main's await."})

for number in (3, 4):
    concurrent = number == 4
    statement = 'await asyncio.gather(operation("A", 2), operation("B", 1))' if concurrent else 'await operation("A", 2)\n    await operation("B", 1)'
    add("Dwa zadania współbieżnie|Two concurrent operations" if concurrent else "Dwa zadania po kolei|Two sequential operations",
        "gather planuje kilka korutyn i czeka na wszystkie. Okresy oczekiwania mogą się nakładać.|gather schedules several coroutines and waits for all of them. Their waits can overlap." if concurrent else "Dwa await zapisane kolejno oznaczają, że drugie wywołanie zacznie się po zakończeniu pierwszego.|Two sequential awaits mean the second call starts after the first finishes.",
        "Porównaj tory A i B oraz czas z zadaniem 03. Oczekuj około 2 s zamiast 3 s.|Compare A and B and the duration with task 03. Expect about 2 s instead of 3 s." if concurrent else "Sprawdź, czy B rozpoczyna się dopiero po końcu A. Oczekuj około 3 s.|Check that B starts after A ends. Expect about 3 s.",
        "A czeka 2 s, B 1 s. Łączny czas zbliża się do najdłuższego oczekiwania, z narzutem wykonania.|A waits 2 s and B 1 s. Total time approaches the longest wait plus overhead." if concurrent else "Czasy 2 s i 1 s sumują się. Samo async def nie spowodowało współbieżności.|The 2 s and 1 s waits add up. async def alone did not introduce concurrency.",
        "To symulacja oczekiwania na I/O. Paski obejmują czekanie; nie mierzą pracy procesora.|This simulates I/O waiting. Bars include waiting and do not measure CPU work.",
        "Co się stanie po zamianie gather na dwa kolejne await?|What happens if gather is replaced by two sequential awaits?",
        "B wystartuje po A; czas wzrośnie z około 2 s do około 3 s.|B starts after A; time rises from about 2 s to about 3 s.",
        '''
import asyncio
from lab_support import event, launch, span

async def operation(name, delay):
    with span(name, "operation"):
        await asyncio.sleep(delay)
        event("log", name, "Completed")

async def main():
    STATEMENT

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
'''.replace("STATEMENT", statement),
        {"operation": "name to podpis toru, delay to czas oczekiwania w sekundach. with span rejestruje początek i koniec nawet przy błędzie. sleep zawiesza korutynę; event publikuje zakończenie.|name labels the lane; delay is seconds to wait. with span records start and end even on errors. sleep suspends the coroutine; event publishes completion.",
         "main": "Dwa wywołania operation tworzą obiekty korutyn. gather planuje je współbieżnie, a await czeka na obie. Wyniki gather byłyby w kolejności A, B, nawet jeśli B skończy pierwsze.|The operation calls create coroutine objects. gather schedules both; await waits for both. Results would be in A, B input order even if B finishes first." if concurrent else "Pierwszy await czeka 2 s na A. Dopiero po jego zakończeniu Python dochodzi do wywołania B i kolejnego await na 1 s. Prześledź tę kolejność na osi czasu.|The first await waits 2 s for A. Only then does Python call B and await it for 1 s. Trace that order on the timeline."})

add("Wartość zwrócona przez korutynę|Returning a value",
    "return przekazuje wartość do miejsca, które czeka przez await. await to wyrażenie: jego wynik można przypisać zmiennej.|return supplies a value to the awaiting caller. await is an expression whose result can be assigned.",
    "Przed uruchomieniem oblicz 5³. Po 2 sekundach odczytaj wynik.|Calculate 5³ before running. Read the result after two seconds.",
    "power zwraca 125, a main odbiera tę liczbę do result. Oczekiwanie nie wykonuje potęgowania szybciej.|power returns 125; main receives it in result. Waiting does not speed up exponentiation.",
    "sleep jest sztucznym opóźnieniem zgodnym z zadaniem. Operator ** wykonuje zwykłe obliczenie CPU.|sleep is the artificial delay required by the task. ** performs ordinary CPU computation.",
    "Czym różni się print od return?|How does print differ from return?",
    "print pokazuje tekst; return daje wynik wywołującemu. W aplikacji metric pokazuje odebraną wartość.|print displays text; return passes a value to the caller. metric displays that received value here.",
    '''
    import asyncio
    from lab_support import launch, metric, span

    async def power(number, exponent):
        with span("power", "calculate"):
            await asyncio.sleep(2)
            return number ** exponent

    async def main():
        result = await power(5, 3)
        metric("5 ** 3", result)

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"power": "number=5 i exponent=3 są argumentami. ** oznacza potęgowanie, nie mnożenie. return kończy funkcję i oddaje 125; wyjście z with nadal rejestruje koniec toru.|number=5 and exponent=3 are arguments. ** is exponentiation. return ends the function with 125; leaving with still records the lane end.", "main": "Prawa strona przypisania musi się zakończyć przed nadaniem wartości result. await odbiera liczbę, nie obiekt korutyny. metric pokazuje ją na karcie wyników.|The right-hand expression completes before result is assigned. await receives a number, not a coroutine object. metric displays it on a result card."})

WEATHER = '''
async def fetch_weather(city):
    with span(city, "weather"):
        await asyncio.sleep(1.5)
        return {"city": city, "temperature": 25, "condition": "sunny"}
'''
for number in (6, 7):
    many = number == 7
    main = '''
async def main():
    cities = ["Warsaw", "Krakow", "Gdansk"]
    results = await asyncio.gather(*(fetch_weather(city) for city in cities))
    for weather in results:
        event("log", weather["city"], str(weather))
    metric("Cities", len(results))
''' if many else '''
async def main():
    weather = await fetch_weather("Warsaw")
    event("log", "weather", str(weather))
    metric("Temperature", weather["temperature"], "°C")
'''
    add("Pogoda dla wielu miast|Weather for several cities" if many else "Słownik danych pogodowych|Weather dictionary",
        "Lista comprehension buduje korutyny dla miast, a * rozpakowuje je na argumenty gather.|A comprehension creates city coroutines and * unpacks them into gather arguments." if many else "Słownik przechowuje pary klucz–wartość. Korutyna może zwrócić cały słownik, tak jak zwykła funkcja.|A dictionary stores key–value pairs. A coroutine can return a dictionary just like an ordinary function.",
        "Trzy tory powinny nakładać się przez około 1,5 s. Znajdź dane wszystkich miast w dzienniku.|Three lanes should overlap for about 1.5 s. Find every city's data in the log." if many else "Po około 1,5 s odczytaj miasto, temperaturę i stan pogody.|After about 1.5 s, read the city, temperature and condition.",
        "gather zwraca listę słowników w kolejności wejściowej. Wszystkie fikcyjne odczyty mają tę samą temperaturę.|gather returns dictionaries in input order. All fictional readings have the same temperature.",
        "Pogoda jest fikcyjna: nie wysyłamy zapytań do serwisu pogodowego.|Weather is fictional: no weather service is contacted.",
        "Co oznacza weather['temperature']?|What does weather['temperature'] mean?",
        "Odczyt wartości spod klucza temperature. Brak klucza spowodowałby KeyError.|Retrieve the value under the temperature key. A missing key would raise KeyError.",
        'import asyncio\nfrom lab_support import event, launch, metric, span\n' + WEATHER + main + '\nif __name__ == "__main__":\n    launch(lambda options: asyncio.run(main()))\n',
        {"fetch_weather": "city trafia do wartości klucza city. Po await sleep powstaje nowy słownik; return oddaje go wywołującemu. Nawiasy {} tworzą słownik, a dwukropek wiąże klucz z wartością.|city becomes the city key's value. After sleep a new dictionary is created and returned. Braces create a dictionary; colons associate keys with values.",
         "main": "cities to lista trzech napisów. Generator tworzy po jednej korutynie na miasto; * podaje je jako oddzielne argumenty. gather zbiera listę wyników, a for wydobywa każdy słownik weather i pokazuje jego dane.|cities contains three strings. The generator creates one coroutine per city; * passes them as separate arguments. gather collects results; for displays each weather dictionary." if many else "fetch_weather otrzymuje napis Warsaw. await oddaje gotowy słownik do weather. weather['temperature'] odczytuje 25, a metric dopisuje jednostkę °C.|fetch_weather receives Warsaw. await supplies its dictionary to weather. weather['temperature'] retrieves 25; metric adds the °C unit."})

add("Pięć symulowanych pingów|Five simulated pings",
    "Losowe opóźnienia sprawiają, że kolejność zakończenia bywa inna od kolejności wejściowej.|Random delays can make completion order differ from input order.",
    "Znajdź najkrótszy i najdłuższy tor. Porównaj kolejność odpowiedzi w logu z listą wyników.|Find the shortest and longest lane. Compare completion logs with the result list.",
    "gather zachowuje kolejność hostów. Log odpowiedzi pokazuje faktyczną kolejność zakończenia.|gather retains host order. Response logs show actual completion order.",
    "To symulacja bez pakietów ICMP. Stałe ziarno losowania daje powtarzalne dane, nie gwarantuje identycznych czasów wykonania.|This simulates ping without ICMP packets. A fixed seed repeats inputs, not exact execution timings.",
    "Czy pierwszy element results zawsze odpowie pierwszy?|Does the first results element always finish first?",
    "Nie. Pozycja wynika z kolejności argumentów gather.|No. Its position follows gather argument order.",
    '''
    import asyncio
    import random
    from lab_support import event, launch, metric, span

    async def ping(host, delay):
        with span(host, "ping"):
            await asyncio.sleep(delay)
            result = f"Host {host} responds"
            event("log", host, result)
            return result

    async def main():
        rng = random.Random(31)
        hosts = [f"server-{number}" for number in range(1, 6)]
        results = await asyncio.gather(
            *(ping(host, rng.uniform(0.1, 1.0)) for host in hosts)
        )
        event("log", "results", str(results))
        metric("Responses", len(results))

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"ping": "host jest nazwą serwera, delay wylosowanym opóźnieniem. f-string podstawia host do tekstu. return oddaje odpowiedź, a event wcześniej zapisuje chwilę jej otrzymania.|host is a server name; delay is a sampled wait. The f-string inserts host into text. return supplies the response; event first records its arrival.", "main": "Random(31) tworzy osobny generator. uniform(0.1,1.0) wybiera czas dla każdego hosta przed wykonaniem ping. range(1,6) daje pięć numerów. gather oddaje pięć odpowiedzi w kolejności hosts.|Random(31) creates a private generator. uniform samples each host's wait before ping executes. range(1,6) gives five numbers. gather returns five responses in hosts order."})

add("Prawdziwe statusy HTTP|Real HTTP status codes",
    "ClientSession zarządza połączeniami HTTP. async with pilnuje zamknięcia sesji i odpowiedzi również po błędzie.|ClientSession manages HTTP connections. async with closes sessions and responses even on errors.",
    "Uruchom trzy lokalne zapytania. Odczytaj rzeczywiste statusy 200, 404 i 503.|Run three local requests and read real 200, 404 and 503 status codes.",
    "Status HTTP to odpowiedź serwera, nie wyjątek połączenia. Bez raise_for_status kod 404 nadal jest odczytywany jako liczba.|An HTTP status is a server response, not a connection error. Without raise_for_status, 404 is read as a number.",
    "Rzeczywiste HTTP działa na loopback, bez Internetu. Port jest dobierany przez system. Sztuczne 0,2 s opóźnienia serwera ułatwia obserwację.|Real HTTP uses loopback without Internet. The OS chooses a port. An artificial 0.2 s server delay aids observation.",
    "Dlaczego jedna sesja dla trzech żądań?|Why share one session across three requests?",
    "Sesja zarządza pulą połączeń. Tworzenie nowej dla każdego URL marnuje zasoby.|A session manages a connection pool. Recreating it per URL wastes resources.",
    '''
    import asyncio
    import aiohttp
    from aiohttp import web
    from lab_support import event, launch, metric, span

    async def respond(request):
        await asyncio.sleep(0.2)
        return web.Response(status=int(request.match_info["status"]))

    async def fetch_status(session, url):
        with span(url.rsplit("/", 1)[-1], "HTTP"):
            try:
                async with session.get(url) as response:
                    event("log", "HTTP", f"{url} -> {response.status}")
                    return response.status
            except (aiohttp.ClientError, asyncio.TimeoutError) as error:
                event("log", "HTTP", str(error))
                return None

    async def main():
        application = web.Application()
        application.router.add_get("/{status}", respond)
        runner = web.AppRunner(application)
        await runner.setup()
        try:
            server = await asyncio.get_running_loop().create_server(
                runner.server, "127.0.0.1", 0
            )
            async with server:
                port = server.sockets[0].getsockname()[1]
                urls = [f"http://127.0.0.1:{port}/{s}" for s in (200, 404, 503)]
                timeout = aiohttp.ClientTimeout(total=3)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    statuses = await asyncio.gather(
                        *(fetch_status(session, url) for url in urls)
                    )
                metric("HTTP statuses", str(statuses))
        finally:
            await runner.cleanup()

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"respond": "To lokalny serwer testowy. Router przekazuje część URL w match_info['status']; int zamienia napis na liczbę statusu. web.Response buduje prawdziwą odpowiedź HTTP.|This is a local test server. The router puts the URL segment in match_info['status']; int converts it to a status number. web.Response creates a real HTTP response.", "fetch_status": "session.get rozpoczyna GET. async with czeka na odpowiedź i gwarantuje jej zwolnienie. response.status jest liczbą, np. 404. except przechwytuje problemy sieciowe i timeout; wtedy return None oznacza brak odpowiedzi.|session.get starts a GET. async with awaits the response and releases it. response.status is a number such as 404. except catches network failures and timeout; None means no response.", "main": "Najpierw tworzymy kontrolowany serwer, potem klienta. create_server z portem 0 prosi system o wolny port; getsockname odbiera jego numer. ClientTimeout ogranicza każde żądanie. gather zbiera statusy. finally sprząta serwer, nawet jeśli zapytanie zawiedzie.|First build a controlled server, then a client. create_server with port 0 requests a free port; getsockname retrieves it. ClientTimeout bounds each request. gather collects statuses; finally cleans up the server even on failure."},
    "Lista URL wskazuje kontrolowany lokalny serwer zamiast publicznych witryn. To nadal prawdziwe aiohttp i HTTP. Obsługujemy statusy 200/404/503 oraz błędy i timeout.|URLs point to a controlled local server rather than public sites. This still uses real aiohttp and HTTP, with 200/404/503 responses, errors and timeouts.")

add("Trzy odliczania|Three countdowns",
    "Każde wywołanie korutyny ma własne zmienne lokalne. Trzy liczniki nie nadpisują sobie remaining.|Each coroutine call has its own local variables. The three counters do not overwrite remaining.",
    "Oczekuj końców po około 3, 5 i 7 s. Sprawdź wspólny czas około 7 s.|Expect finishes around 3, 5 and 7 s and total time near 7 s.",
    "Jedna pętla zdarzeń przełącza gotowe korutyny. Nie powstały trzy wątki.|One event loop switches ready coroutines. Three threads were not created.",
    "Kolejność logów o tym samym nominalnym czasie nie jest istotną gwarancją programu.|The order of logs at the same nominal time is not an essential program guarantee.",
    "Co oznacza trzeci argument -1 w range?|What does range's third argument -1 do?",
    "Zmniejsza wartość o jeden w każdej iteracji. range(start,0,-1) kończy na 1.|It decreases the value by one per iteration. range(start,0,-1) ends at 1.",
    '''
    import asyncio
    from lab_support import event, launch, span

    async def countdown(name, start):
        with span(name, "countdown"):
            for remaining in range(start, 0, -1):
                event("log", name, f"{remaining} seconds left")
                await asyncio.sleep(1)
            event("log", name, "Finished")

    async def main():
        await asyncio.gather(
            countdown("A", 5), countdown("B", 3), countdown("C", 7)
        )

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"countdown": "start wyznacza pierwszą wartość. range(start,0,-1) odlicza do 1, bez zera. Najpierw logujemy remaining, potem czekamy sekundę. Finished pojawia się dopiero po ostatnim oczekiwaniu.|start sets the first value. range(start,0,-1) counts down to 1. We log remaining before waiting a second. Finished appears after the last wait.", "main": "gather dostaje trzy oddzielne obiekty korutyn z różnymi argumentami. await kończy się, gdy wszystkie trzy zakończą odliczanie; C wyznacza najdłuższy czas.|gather receives three separate coroutine objects with different arguments. await completes when all three countdowns finish; C determines the longest duration."})

add("Dziesięć wyników i suma|Ten results and their sum",
    "gather zbiera wartości return. Dopiero gotową listę liczb można przekazać do sum.|gather collects return values. The finished list of numbers can then be passed to sum.",
    "Porównaj 10 liczb z kartą sumy. Tory mają losowe długości od 2 do 5 s.|Compare the ten numbers with the sum card. Lanes last from 2 to 5 s.",
    "Czas zbliża się do najdłuższego czekania. Wynik sumy nie zależy od kolejności zakończenia.|Time approaches the longest wait. The sum does not depend on completion order.",
    "To symulowane długie obliczenia: sleep nie obciąża CPU. Dane losowane są z ustalonym ziarnem.|These are simulated long calculations: sleep does not load the CPU. Inputs use a fixed random seed.",
    "Dlaczego sum wywołujemy dopiero po await gather?|Why call sum only after await gather?",
    "Wcześniej mielibyśmy korutyny, a nie zwrócone przez nie liczby.|Before that we would have coroutines rather than returned numbers.",
    '''
    import asyncio
    import random
    from lab_support import event, launch, metric, span

    async def calculate(name, delay, value):
        with span(name, "calculate"):
            await asyncio.sleep(delay)
            event("log", name, str(value))
            return value

    async def main():
        rng = random.Random(31)
        jobs = [calculate(f"job-{i}", rng.uniform(2, 5), rng.randint(1, 100))
                for i in range(10)]
        results = await asyncio.gather(*jobs)
        event("log", "results", str(results))
        metric("Sum", sum(results))
        metric("Count", len(results))

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"calculate": "value jest przygotowaną liczbą 1–100. Po czekaniu return oddaje ją jako wynik tej korutyny. name pozwala przypisać wynik do toru.|value is a prepared number from 1 to 100. After waiting, return supplies it as this coroutine's result. name identifies its lane.", "main": "randint obejmuje obie granice 1 i 100. Lista jobs zawiera 10 korutyn, nie 10 wyników. *jobs rozpakowuje listę. await gather zastępuje oczekiwanie gotową listą liczb w results; sum je dodaje, len liczy.|randint includes both bounds. jobs contains ten coroutines, not results. *jobs unpacks the list. await gather produces the numbers in results; sum adds them and len counts them."})

add("Pierwszy wynik i sprzątanie|First result and cleanup",
    "Task jest uchwytem do zaplanowanej korutyny. wait może zwrócić dwie grupy: zakończone done i jeszcze działające pending.|A Task is a handle to a scheduled coroutine. wait returns finished done and unfinished pending sets.",
    "Znajdź zwycięzcę i komunikaty anulowania. Cały program nie powinien czekać na najwolniejszy tor.|Find the winner and cancellation messages. The program should not wait for the slowest lane.",
    "FIRST_COMPLETED wraca po pierwszym zakończeniu. Pozostałe zadania prosimy o anulowanie i czekamy na ich sprzątanie.|FIRST_COMPLETED returns on first completion. Remaining tasks are cancelled and awaited for cleanup.",
    "done jest zbiorem: przy bliskich zakończeniach może zawierać więcej niż jedno zadanie. cancel to prośba, a nie natychmiastowe zabicie.|done is a set and can contain multiple near-simultaneous completions. cancel requests cancellation rather than killing immediately.",
    "Po co gather po cancel?|Why gather after cancel?",
    "Aby zadania mogły obsłużyć CancelledError i zakończyć sprzątanie przed wyjściem.|So tasks can handle CancelledError and finish cleanup before exit.",
    '''
    import asyncio
    import random
    from lab_support import event, launch, metric, span

    async def contender(name, delay):
        with span(name, "race"):
            try:
                await asyncio.sleep(delay)
                return delay
            except asyncio.CancelledError:
                event("log", name, "Cancelled; cleanup complete")
                raise

    async def main():
        rng = random.Random(31)
        tasks = [asyncio.create_task(contender(f"job-{i}", rng.uniform(1, 10)))
                 for i in range(5)]
        done, pending = await asyncio.wait(
            tasks, return_when=asyncio.FIRST_COMPLETED
        )
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
        metric("First completed delay", min(task.result() for task in done), "s")
        metric("Cancelled tasks", len(pending))

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"contender": "try otacza miejsce możliwego anulowania. Gdy sleep otrzyma CancelledError, except zapisuje sprzątanie, a samo raise ponownie zgłasza ten sam wyjątek. Dzięki temu Task zachowuje stan anulowany.|try surrounds the cancellation point. If sleep receives CancelledError, except records cleanup and bare raise propagates the same exception, preserving cancelled status.", "main": "create_task planuje każdą korutynę. wait wymaga tu Task, nie surowych korutyn. Przypisanie done,pending rozpakowuje parę zbiorów. cancel zgłasza żądanie. gather(return_exceptions=True) odbiera zakończenia bez przerywania sprzątania przez wyjątki anulowania. result odczytuje wynik już ukończonego Task.|create_task schedules each coroutine. wait requires Tasks here. done,pending unpacks two sets. cancel requests cancellation. gather(return_exceptions=True) collects cleanup outcomes without cancellation exceptions interrupting it. result reads an already completed Task."})

add("Serwer TCP echo|TCP echo server",
    "TCP przesyła strumień bajtów. Ustalamy prosty protokół: jedna wiadomość kończy się znakiem nowej linii.|TCP carries a byte stream. Our protocol ends one message with a newline.",
    "Wbudowany klient wyśle Hello asyncio i odbierze tę samą wiadomość. Porównaj bajty na karcie wyniku.|The built-in client sends Hello asyncio and receives it back. Compare the result bytes.",
    "To prawdziwe połączenie TCP na loopback. Serwer odsyła otrzymane bajty i zamyka połączenie.|This is a real loopback TCP connection. The server echoes received bytes and closes the connection.",
    "Domyślny port 0 unika konfliktów; wariant 8888 realizuje port z polecenia. Jedna linia to celowy protokół demonstracyjny.|Port 0 avoids conflicts by default; the 8888 preset uses the specified port. One line is a deliberate demo protocol.",
    "Dlaczego samo writer.write nie wystarcza?|Why isn't writer.write alone enough?",
    "write przekazuje dane do bufora. await drain obsługuje kontrolę przepływu; zamknięcie wymaga close i wait_closed.|write buffers bytes. await drain handles flow control; closing uses close and wait_closed.",
    '''
    import asyncio
    from lab_support import config, event, launch, metric, span

    async def handle_client(reader, writer):
        with span("server", "echo"):
            try:
                data = await reader.readline()
                writer.write(data)
                await writer.drain()
                event("log", "server", repr(data))
            finally:
                writer.close()
                await writer.wait_closed()

    async def main():
        port = config().get("port", 0)
        server = await asyncio.start_server(handle_client, "127.0.0.1", port)
        async with server:
            actual_port = server.sockets[0].getsockname()[1]
            reader, writer = await asyncio.open_connection("127.0.0.1", actual_port)
            try:
                message = b"Hello asyncio!\\n"
                writer.write(message)
                await writer.drain()
                reply = await asyncio.wait_for(reader.readline(), timeout=3)
                metric("Echo matches input", reply == message)
                event("log", "client", repr(reply))
            finally:
                writer.close()
                await writer.wait_closed()

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"handle_client": "start_server wywołuje tę korutynę dla nowego klienta i daje reader oraz writer. readline czeka na bajty do znaku \\n. write odsyła je bez zmiany. finally zamyka writer także po błędzie.|start_server calls this coroutine for each client with reader and writer. readline waits for bytes through a newline. write echoes them unchanged. finally closes the writer even on errors.", "main": "config.get wybiera port, domyślnie 0. async with server utrzymuje nasłuchiwanie w bloku. open_connection tworzy klienta. b przed napisem oznacza bytes. wait_for chroni odczyt przed wiecznym czekaniem; == sprawdza zgodność odpowiedzi.|config.get selects the port, default 0. async with server keeps it listening within the block. open_connection creates a client. b denotes bytes. wait_for bounds the read; == checks response equality."},
    "Pokaz ma automatycznego klienta i kończy serwer po wymianie wiadomości. Domyślnie system wybiera wolny port; dostępny jest wariant localhost:8888.|The demo includes a client and stops its server after the exchange. The OS selects a free port by default; localhost:8888 is also available.")

add("Producent, kolejka, konsumenci|Producer, queue and consumers",
    "Queue rozdziela produkowanie danych od ich przetwarzania. get czeka na element, a task_done potwierdza jego obsłużenie.|Queue separates production from processing. get waits for an item; task_done acknowledges its processing.",
    "Obserwuj 20 liczb i nazwy konsumentów. Program trwa co najmniej 10 s, bo producent dodaje co 0,5 s.|Watch twenty numbers and consumer names. The producer adds every 0.5 s, taking at least ten seconds.",
    "Każda liczba jest odebrana raz. queue.join czeka na potwierdzenia task_done, nie tylko na pusty magazyn.|Each number is received once. queue.join waits for task_done acknowledgements, not merely an empty queue.",
    "Kto odbierze konkretną liczbę zależy od planowania. None jest sygnałem końca, nie liczbą do przetworzenia.|Which consumer receives a particular number depends on scheduling. None marks shutdown rather than work.",
    "Dlaczego potrzebujemy dwóch None?|Why do we need two None markers?",
    "Są dwaj konsumenci. Każdy musi dostać własny sygnał zakończenia.|There are two consumers and each needs its own shutdown signal.",
    '''
    import asyncio
    from lab_support import event, launch, metric, span

    async def producer(queue):
        for number in range(1, 21):
            await asyncio.sleep(0.5)
            await queue.put(number)
            event("put", "producer", str(number))
        for _ in range(2):
            await queue.put(None)

    async def consumer(name, queue, processed):
        while True:
            number = await queue.get()
            try:
                if number is None:
                    return
                event("get", name, str(number))
                with span(name, f"item-{number}"):
                    await asyncio.sleep(0.7)
                    processed.append(number)
                    event("log", name, f"Processed {number}")
            finally:
                queue.task_done()

    async def main():
        queue = asyncio.Queue(maxsize=4)
        processed = []
        consumers = [asyncio.create_task(consumer(name, queue, processed))
                     for name in ("consumer-A", "consumer-B")]
        await producer(queue)
        await queue.join()
        await asyncio.gather(*consumers)
        metric("Processed items", len(processed))
        metric("Exactly 1..20", sorted(processed) == list(range(1, 21)))

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"producer": "queue.put dodaje liczbę; przy pełnej kolejce czeka na miejsce. range(1,21) daje 20 liczb. Dwie wartości None wysyłamy po danych. _ to nazwa zmiennej, której wartości tu nie używamy.|queue.put adds a number and waits if full. range(1,21) yields twenty numbers. Two None markers follow the data. _ names an unused loop variable.", "consumer": "while True powtarza pobieranie. get usuwa jeden element z kolejki. is None rozpoznaje sygnał końca. finally gwarantuje jedno task_done dla każdego pobrania, także przy return. append dodaje przetworzoną liczbę do listy.|while True repeats retrieval. get removes one item. is None recognizes shutdown. finally guarantees one task_done per retrieval even on return. append records processed numbers.", "main": "maxsize=4 ogranicza liczbę oczekujących elementów. Dwa Task zaczynają obsługiwać dane, gdy main oddaje sterowanie. Po produkcji join czeka na wszystkie potwierdzenia, gather na zakończenie konsumentów. sorted pozwala porównać zawartość niezależnie od kolejności.|maxsize=4 bounds waiting items. Two Tasks process data when main yields. After production, join waits for acknowledgements and gather for consumer exit. sorted compares contents regardless of order."},
    "Dodano jawne zakończenie przez dwa None, kontrolę przetworzonych liczb i 0,7 s symulowanego przetwarzania. Produkcja zachowuje 20 liczb oraz odstęp 0,5 s.|Two None markers stop consumers; processing is checked and includes a simulated 0.7 s delay. Production retains twenty items at 0.5 s intervals.")

add("Wspólny plik i Lock|Shared file and Lock",
    "Lock chroni sekcję, w której tylko jedna korutyna ma pracować naraz. aiofiles udostępnia await dla operacji plikowych delegowanych do puli wątków.|Lock protects a section used by one coroutine at a time. aiofiles provides awaitable file operations delegated to a thread pool.",
    "Odczytaj pięć pełnych wierszy z prawdziwego pliku. Tory oczekiwania mogą się nakładać, sekcje zapisu mają osobne podpisy.|Read five complete lines from a real file. Waiting can overlap; write sections are labelled separately.",
    "Lock obejmuje otwarcie, dopisanie i zamknięcie pliku. Wynik odczytujemy dopiero po zakończeniu wszystkich autorów.|Lock covers opening, appending and closing. The file is read after all writers finish.",
    "aiofiles używa wątków pomocniczych; nie każda operacja async wykonuje się wyłącznie w jednym wątku. Plik demonstracyjny jest tymczasowy.|aiofiles uses helper threads; not every async operation runs exclusively on one thread. The demo file is temporary.",
    "Dlaczego jeden wspólny Lock, a nie pięć różnych?|Why one shared Lock instead of five separate locks?",
    "Osobne blokady nie koordynowałyby dostępu do tego samego pliku.|Separate locks would not coordinate access to the same file.",
    '''
    import asyncio
    import tempfile
    from pathlib import Path
    import aiofiles
    from lab_support import event, launch, metric, span

    async def write_log(number, path, lock):
        with span(f"writer-{number}", "generate"):
            await asyncio.sleep(0.1)
        async with lock:
            with span(f"writer-{number}", "write"):
                async with aiofiles.open(path, "a", encoding="utf-8") as output:
                    await output.write(f"Log from coroutine {number}\\n")

    async def main():
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "logs.txt"
            lock = asyncio.Lock()
            await asyncio.gather(*(write_log(i, path, lock) for i in range(1, 6)))
            async with aiofiles.open(path, encoding="utf-8") as source:
                text = await source.read()
            event("log", "file", text)
            lines = text.splitlines()
            metric("Complete lines", len(lines))
            expected = {f"Log from coroutine {i}" for i in range(1, 6)}
            metric("All records intact", set(lines) == expected and len(lines) == 5)

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"write_log": "Każdy autor dostaje ten sam path i lock. async with lock czeka na wyłączny dostęp i zwalnia go automatycznie. Tryb a dopisuje zamiast kasować dane. await write przekazuje pełną linię do pliku; zamknięcie kończy zapis przed oddaniem blokady.|Each writer shares path and lock. async with lock acquires exclusive access and releases it automatically. Mode a appends. await write writes one full line; closing finishes before the lock is released.", "main": "TemporaryDirectory tworzy prywatny katalog i usuwa go po bloku. Operator / na Path buduje ścieżkę. Po gather otwieramy plik do odczytu. splitlines dzieli tekst na wiersze bez znaków końca linii; zbiór set sprawdza treść, len także liczbę wpisów.|TemporaryDirectory creates and later removes a private directory. Path / builds a path. After gather we read the file. splitlines returns lines without newline characters; set checks content and len also checks the record count."})

add("Rate limiter: pięć na sekundę|Rate limiter: five per second",
    "Limit szybkości dotyczy liczby startów w czasie. Semafor ogranicza liczbę operacji jednocześnie; to inny warunek.|A rate limit bounds starts over time. A semaphore bounds simultaneous operations, which is a different condition.",
    "Obserwuj 40 zezwoleń: 20 zadań prosi po dwa razy. Sprawdź grupy najwyżej pięciu startów na sekundę.|Watch forty grants: twenty tasks request twice each. Check groups of at most five starts per second.",
    "Kolejka przechowuje chwile udzielonych zezwoleń. Zanim przyznamy nowe, usuwamy te starsze niż sekundę.|A deque retains grant times. Before granting another, timestamps at least one second old are removed.",
    "To limit w kroczącym oknie 1 s jednego procesu. Nie gwarantuje sprawiedliwości między zadaniami ani limitu wspólnego dla wielu serwerów.|This limits a rolling one-second window in one process. It guarantees neither fairness nor a shared limit across servers.",
    "Dlaczego zegar pętli zamiast aktualnej daty?|Why use loop time rather than the current date?",
    "To zegar monotoniczny do odstępów; zmiana zegara systemowego nie cofa obliczanego czasu.|It is a monotonic interval clock; wall-clock adjustments do not reverse elapsed time.",
    '''
    import asyncio
    from collections import deque
    from lab_support import event, launch, metric, span

    class RateLimiter:
        def __init__(self, limit):
            if limit < 1:
                raise ValueError("Limit must be positive")
            self.limit = limit
            self.timestamps = deque()
            self.lock = asyncio.Lock()

        async def acquire(self):
            loop = asyncio.get_running_loop()
            async with self.lock:
                while True:
                    now = loop.time()
                    while self.timestamps and now - self.timestamps[0] >= 1:
                        self.timestamps.popleft()
                    if len(self.timestamps) < self.limit:
                        self.timestamps.append(now)
                        return now
                    await asyncio.sleep(max(0, 1 - (now - self.timestamps[0])))

    async def request(name, limiter, grants):
        for attempt in range(2):
            with span(name, f"wait-{attempt}"):
                granted = await limiter.acquire()
            grants.append(granted)
            event("log", name, f"Granted attempt {attempt + 1}")

    async def main():
        limiter = RateLimiter(5)
        grants = []
        await asyncio.gather(*(request(f"job-{i}", limiter, grants) for i in range(20)))
        times = sorted(grants)
        valid = all(times[i] - times[i - 5] >= 1 for i in range(5, len(times)))
        metric("Granted requests", len(times))
        metric("Rolling window respected", valid)

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"RateLimiter": "Klasa łączy stan i zachowanie. self oznacza konkretny obiekt limitera. __init__ zapisuje limit, pustą deque i wspólną blokadę. Metoda acquire przyzna zezwolenie albo zaczeka.|The class groups state and behavior. self is this limiter instance. __init__ stores the limit, an empty deque and a shared lock. acquire grants permission or waits.", "__init__": "limit musi być dodatni. self.limit pamięta n; timestamps zawiera wyłącznie chwile przyznanych zezwoleń. deque pozwala tanio usuwać najstarszy wpis z lewej strony.|limit must be positive. self.limit stores n; timestamps holds granted times only. deque efficiently removes the oldest entry from the left.", "acquire": "Lock chroni wspólne sprawdzenie i dopisanie czasu. Wewnętrzne while usuwa stare wpisy przez popleft. Jeśli jest miejsce, append zapisuje now, return kończy metodę i zwalnia blokadę. W przeciwnym razie sleep czeka do wygaśnięcia najstarszego wpisu; pętla sprawdza warunek ponownie. Trzymanie Lock podczas sleep celowo ustawia kolejkę oczekujących; event loop nadal może wykonywać inne zadania.|Lock protects checking and appending together. The inner while removes old entries with popleft. If capacity exists, append stores now and return releases the lock. Otherwise sleep waits until the oldest expires and the loop rechecks. Holding Lock during sleep deliberately queues waiters; the event loop can still run other tasks.", "request": "Każde z 20 zadań ma dwie próby. await acquire dostaje czas zezwolenia. Paski pokazują oczekiwanie na limit, a lista grants służy późniejszej kontroli.|Each of twenty tasks makes two attempts. await acquire receives a grant time. Bars show waiting for permission; grants supports verification.", "main": "Tworzymy jeden wspólny limiter, nie osobny dla każdego zadania. Kontrola porównuje i-te zezwolenie z tym pięć miejsc wcześniej: odstęp musi wynosić co najmniej sekundę.|Create one shared limiter, not one per task. Verification compares each grant with the one five positions earlier: they must be at least a second apart."},
    "20 zadań wykonuje po dwie iteracje, łącznie 40 acquire, aby pokaz był skończony. Limit wynosi 5 na kroczącą sekundę.|Twenty tasks perform two iterations each, totalling forty acquire calls, so the demo terminates. The limit is five per rolling second.")

add("Łańcuch zależności|Dependency chain",
    "Nie da się pobrać postów bez ID użytkownika. Gdy mamy listę postów, komentarze do różnych postów mogą być pobierane współbieżnie.|Posts need a user ID. Once post IDs are known, their comments can be fetched concurrently.",
    "Znajdź dwa pojedyncze etapy po 1 s, a potem trzy nakładające się pobrania komentarzy.|Find two sequential one-second stages, then three overlapping comment fetches.",
    "Około 3 s: 1 s użytkownik + 1 s posty + około 1 s wspólnego czekania na komentarze.|About three seconds: one for user, one for posts and one overlapping wait for comments.",
    "Baza i API są symulowane. Nie nakładamy etapów, które potrzebują wyniku poprzedniego.|Database and API are simulated. Stages needing previous results cannot overlap here.",
    "Dlaczego nie gather dla całego łańcucha?|Why not gather the entire chain?",
    "Argument user_id nie istnieje przed pierwszym wynikiem, a post_ids przed drugim.|user_id is unavailable before the first result, and post_ids before the second.",
    '''
    import asyncio
    from lab_support import event, launch, metric, span

    async def fetch_user_id(username):
        with span("user", "lookup"):
            await asyncio.sleep(1)
            event("log", "user", f"{username} -> 42")
            return 42

    async def fetch_posts(user_id):
        with span("posts", "lookup"):
            await asyncio.sleep(1)
            return [user_id * 10 + i for i in range(3)]

    async def fetch_comments(post_id):
        with span(f"post-{post_id}", "comments"):
            await asyncio.sleep(1)
            return [f"Comment on post {post_id}"]

    async def main():
        user_id = await fetch_user_id("Anna")
        post_ids = await fetch_posts(user_id)
        comments = await asyncio.gather(*(fetch_comments(post) for post in post_ids))
        event("log", "comments", str(comments))
        metric("Posts", len(post_ids))

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"fetch_user_id": "username jest wejściowym napisem Anna. Po symulowanym wyszukaniu zwracamy ID 42, które main przypisze do user_id.|username is the input Anna. After a simulated lookup we return ID 42, which main assigns to user_id.", "fetch_posts": "user_id=42 pozwala przygotować ID 420,421,422. Comprehension buduje nową listę; return oddaje ją jako całość.|user_id=42 produces IDs 420,421,422. The comprehension creates a list and return supplies it as a whole.", "fetch_comments": "Każdy post_id daje osobne pobranie. Wynik to lista z jednym komentarzem, dlatego gather w main zwróci listę list.|Each post_id gets its own fetch. Its result is a one-comment list, so gather in main produces a list of lists.", "main": "Czytaj od góry: najpierw ID, potem posty dla tego ID. Dopiero teraz tworzymy korutyny komentarzy. * rozpakowuje trzy korutyny, a gather planuje je razem. Zagnieżdżona lista odzwierciedla trzy posty.|Read top to bottom: user ID, then posts for that ID. Only then are comment coroutines created. * unpacks three coroutines; gather schedules them together. The nested result reflects three posts."})

add("Anulowanie i sprzątanie|Cancellation and cleanup",
    "cancel prosi o dostarczenie CancelledError przy najbliższej okazji. Korutyna może wtedy zwolnić zasoby i przekazać anulowanie dalej.|cancel requests delivery of CancelledError at the next opportunity. The coroutine can clean up and propagate cancellation.",
    "Przez około 5 s zobaczysz Working. Potem komunikat sprzątania i potwierdzenie stanu Task.|See Working for about five seconds, then cleanup and confirmation of Task status.",
    "main nie kończy się od razu po cancel: await task czeka na obsługę anulowania.|main does not exit immediately after cancel: await task waits for cancellation handling.",
    "Liczba logów blisko granicy 5 s zależy od planowania. Nie ignorujemy CancelledError wewnątrz worker.|Logs near the five-second boundary depend on scheduling. worker does not swallow CancelledError.",
    "Po co raise wewnątrz except?|Why raise inside except?",
    "Przekazuje anulowanie dalej po sprzątaniu. Bez niego Task mógłby zakończyć się normalnie.|It propagates cancellation after cleanup. Without it the Task could finish normally.",
    '''
    import asyncio
    from lab_support import event, launch, metric, span

    async def worker():
        with span("worker", "lifetime"):
            try:
                while True:
                    event("log", "worker", "Working...")
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                event("log", "worker", "Cancelled; cleaning up...")
                raise

    async def main():
        task = asyncio.create_task(worker())
        await asyncio.sleep(5)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            event("log", "main", "Cancellation acknowledged")
        metric("Task cancelled", task.cancelled())

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"worker": "while True nie ma naturalnego końca. sleep oddaje sterowanie co sekundę i jest miejscem dostarczenia anulowania. except sprząta, a raise nie ukrywa faktu anulowania. with span zapisuje też koniec przerwanej pracy.|while True has no natural end. sleep yields every second and receives cancellation. except cleans up and raise preserves cancellation. with span records the interrupted work's end.", "main": "create_task zwraca uchwyt task. Podczas sleep(5) worker działa. cancel zgłasza prośbę, await task odbiera CancelledError. main obsługuje go jako oczekiwane zakończenie. cancelled sprawdza końcowy stan.|create_task returns the task handle. worker runs during sleep(5). cancel requests interruption; await task receives CancelledError. main handles it as an expected outcome. cancelled checks final status."})

add("Asynchroniczny generator liczb pierwszych|Async prime generator",
    "yield produkuje pojedynczą wartość i zachowuje stan generatora. async for prosi o następne wartości, czekając na nie asynchronicznie.|yield produces one value and preserves generator state. async for requests successive values asynchronously.",
    "Sprawdź liczby 2,3,5…97, liczbę wyników 25 i największą liczbę 97.|Check 2,3,5…97, the count 25 and the largest prime 97.",
    "Generator daje wartości stopniowo, bez przygotowania całej listy z góry. Odbiorca dopisuje je do results.|The generator yields incrementally without preparing the whole list. The consumer appends to results.",
    "sleep(0.1) ilustruje produkowanie z opóźnieniem. Sprawdzanie pierwszości nadal jest synchronicznym obliczeniem CPU; tu zakres jest mały.|sleep(0.1) illustrates delayed production. Primality checking remains synchronous CPU work; the range is small here.",
    "Czym yield różni się od return?|How does yield differ from return?",
    "yield przekazuje jeden element i pozwala wznowić generator; return kończy jego działanie.|yield supplies one item and permits resumption; return ends the generator.",
    '''
    import asyncio
    from lab_support import event, launch, metric

    def is_prime(number):
        if number < 2:
            return False
        return all(number % divisor != 0
                   for divisor in range(2, int(number ** 0.5) + 1))

    async def primes(limit):
        for number in range(2, limit + 1):
            if is_prime(number):
                await asyncio.sleep(0.1)
                yield number

    async def main():
        results = []
        async for number in primes(100):
            results.append(number)
            event("log", "prime", str(number))
        metric("Prime count", len(results))
        metric("Largest prime", max(results))

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"is_prime": "Liczby <2 nie są pierwsze. % to reszta z dzielenia; !=0 oznacza brak dzielnika. Wystarczy badać dzielniki do pierwiastka: number**0.5. all wymaga True dla każdego testu. Dla 2 lista testów jest pusta, a all zwraca True.|Numbers below 2 are not prime. % gives a remainder; !=0 means no divisor. Testing through the square root is sufficient. all requires every test to be True. For 2 there are no tests and all returns True.", "primes": "async def z yield tworzy asynchroniczny generator. Po znalezieniu liczby pierwszej czekamy 0,1 s i yield oddaje jeden element odbiorcy. Następne żądanie kontynuuje za yield.|async def containing yield defines an async generator. On finding a prime we wait 0.1 s and yield one item. The next request resumes after yield.", "main": "async for obsługuje protokół asynchronicznego iteratora: prosi o kolejny element, czeka i powtarza. Nie używamy await primes(100), bo to generator, nie korutyna zwracająca listę. len liczy zebrane liczby, max wybiera największą.|async for handles the async iteration protocol: request, await, repeat. We do not await primes(100), which is a generator, not a list-returning coroutine. len counts results and max picks the largest."},
    "Generator ma jawny limit 100 i kończy się sam. Liczby są pierwsze nie większe niż 100, a nie równe 100.|The generator has an explicit limit of 100 and stops itself. It yields primes no greater than 100, not a prime equal to 100.")

add("Timeout: wynik albo przekroczenie czasu|Timeout: result or deadline",
    "wait_for ogranicza czas oczekiwania. Gdy czas minie, anuluje oczekiwaną operację i zgłasza TimeoutError.|wait_for bounds waiting. On expiry it cancels the operation and raises TimeoutError.",
    "Uruchom oba warianty: 1 s daje wynik przed limitem 3 s; 5 s prowadzi do timeout. Dostępne jest też losowanie 1–5 s.|Try both presets: 1 s returns within the 3 s limit; 5 s times out. Random 1–5 s is also available.",
    "Przekroczenie limitu to obsłużona sytuacja pokazu. Odczytaj kartę Timeout oraz komunikat sprzątania.|A deadline expiry is an expected demo outcome. Read the Timeout card and cleanup message.",
    "wait_for czeka także na zakończenie anulowania, więc łączny czas może przekroczyć timeout. asyncio.TimeoutError jest aliasem wbudowanego TimeoutError we współczesnym Pythonie.|wait_for also waits for cancellation cleanup, so total time can exceed the timeout. asyncio.TimeoutError aliases built-in TimeoutError in modern Python.",
    "Czy timeout gwarantuje zakończenie programu dokładnie po 3 s?|Does timeout guarantee exit at exactly 3 s?",
    "Nie: dochodzi narzut planowania i sprzątanie anulowanej korutyny.|No: scheduling overhead and cancellation cleanup also take time.",
    '''
    import asyncio
    import random
    from lab_support import config, event, launch, metric, span

    async def operation(delay):
        with span("operation", "deadline"):
            try:
                await asyncio.sleep(delay)
                return "Completed in time"
            finally:
                event("log", "operation", "Cleanup complete")

    async def main():
        delay = config().get("delay", 1)
        if delay == "random":
            delay = random.uniform(1, 5)
        metric("Requested delay", round(delay, 3), "s")
        try:
            result = await asyncio.wait_for(operation(delay), timeout=3)
            event("log", "result", result)
            metric("Timeout", False)
        except asyncio.TimeoutError:
            event("log", "result", "Time limit of 3 seconds exceeded")
            metric("Timeout", True)

    if __name__ == "__main__":
        launch(lambda options: asyncio.run(main()))
    ''', {"operation": "delay to czas potrzebny na operację. Jeśli sleep skończy, return oddaje komunikat. finally działa zarówno przy wyniku, jak i przy anulowaniu przez wait_for: tu symuluje sprzątanie.|delay is the operation duration. If sleep finishes, return supplies a message. finally runs on success or cancellation by wait_for and represents cleanup.", "main": "config.get wybiera wariant. Dla random losujemy czas przez uniform. wait_for planuje operation i czeka najwyżej 3 s przed rozpoczęciem anulowania. Sukces daje result; przekroczenie limitu przechodzi do except. metric pokazuje True albo False.|config.get selects a preset; uniform samples random delay. wait_for schedules operation and waits up to 3 s before starting cancellation. Success supplies result; expiry goes to except. metric displays True or False."},
    "Domyślny wariant 1 s oraz wariant 5 s pozwalają pewnie pokazać oba wyniki. Osobny wariant losuje czas 1–5 s zgodnie z poleceniem.|Deterministic 1 s and 5 s presets demonstrate both outcomes. A separate random preset samples 1–5 s as required.")


def generate():
    records = []
    for number, task in enumerate(TASKS, 1):
        source = task.pop("source")
        notes = task.pop("notes")
        nodes = {node.name: node for node in ast.walk(ast.parse(source))
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        steps = []
        for name, explanation in notes.items():
            node = nodes[name]
            steps.append(dict(id=name, start=node.lineno, end=node.end_lineno,
                              code="\n".join(source.splitlines()[node.lineno-1:node.end_lineno]),
                              body=explanation))
        path = ROOT / "examples" / f"task{number:02}.py"
        path.write_text(source, encoding="utf-8")
        records.append(dict(number=number, **task, steps=steps, source=source))
    (ROOT / "material.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    generate()
