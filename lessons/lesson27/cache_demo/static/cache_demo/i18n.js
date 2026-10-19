// Translation data is kept away from request and timer logic.
// Add matching keys in both dictionaries when extending the interface.
const en = {
  practiceQuestions: 'Questions & answers', questionHint: 'Try answering first, then click the question to reveal its explanation.',
  moreQuestions: 'Want more simple questions?', allQuestions: 'All questions shown',
  previousNote: 'Previous instruction selected. Cache, timers and saved changes stay as they are; Next step repeats the operation.',
  home: 'Home', serverLabel: 'Current Django server', footer: 'Real Django requests. Real cache. A guided explanation.',
  homeEyebrow: 'THREE BACKENDS · ONE LESSON', homeTitle: 'See what your cache actually does.',
  homeLead: 'Follow a request from your Python view to its cached response. Compare memory, files and Redis, one step at a time.',
  howTitle: 'How this presentation works',
  howText: 'The launcher hosts this control page on port 7999 and starts three independent Django processes on ports 8000, 8001 and 8002. Each uses its own settings and a presentation copy of its database. Use runserver / Stop server to control each process, and task links to visit its port. Redis is a separate storage service on port 6379.',
  isolation: 'Demo cache is separate from the homework cache. Reset starts a fresh task namespace. Quick settings use 7–10 seconds; Homework settings restore the original lifetimes. Editing updates only a dedicated demo client.',
  checking: 'Checking…', online: 'Server and cache available', offline: 'Unavailable — check server / storage',
  refreshStatus: 'Refresh status', chooseTask: 'Choose a task', task: 'TASK', demonstration: 'Interactive demonstration',
  scenario: 'Scenario', quick: 'Quick demo', homework: 'Homework settings', ttl: 'Cache time [s]', detailTtl: 'Detail time [s]',
  apply: 'Apply & restart', reset: 'Reset scenario', guided: 'GUIDED WALKTHROUGH', next: 'Next step', previous: 'Previous step',
  result: 'Result', duration: 'Server duration', queries: 'SQL queries', response: 'Latest response', files: 'Actual cache files',
  openApi: 'Open original API / Debug Toolbar', history: 'Request history', action: 'Action', original: 'Original homework',
  python: 'What did Python do?', explainQuestion: 'Try explaining this:', yourCode: 'Your Python code',
  adapterNote: 'The demo adapter changes storage and lifetime. The core homework logic stays in the files below. The presentation engine is in cache_demo/engine.py.',
  note: 'Applied: {ttl} s. Homework: {original} s. {detail} Changing the inputs requires Apply & restart.',
  detailNote: 'Detail: {ttl} s (homework: 60 s).',
  probe: 'Check backend', read: 'Fetch / read', write: 'Write sample', delete: 'Delete key', clear: 'Clear sandbox',
  list: 'Fetch list', detail: 'Fetch detail', update: 'Update demo client',
  wait: 'Wait until the entry expires, then read it again. The countdown does not extend on HIT.',
  first: 'Make the first request. Expect a MISS and actual Python execution.',
  second: 'Repeat the same request before expiration. Expect a HIT.',
  probeStep: 'Check the configured backend with a real write and read.',
  writeStep: 'Write sample data with the selected cache lifetime.', readStep: 'Read the previously stored value.',
  clearStep: 'Clear the dedicated sandbox and inspect the missing keys.',
  listStep: 'Fetch the list and start its independent countdown.', detailStep: 'Fetch detail and start its countdown.',
  hitDetail: 'Read detail again before expiration. Expect a HIT.',
  updateStep: 'PATCH the demo client. The homework code invalidates its detail key.',
  updatedDetail: 'Fetch detail after PATCH. Expect a MISS and the new city.',
  staleList: 'Fetch the list again. If its timer is still running, the old city remains cached.',
  complete: 'Walkthrough complete. Reset to repeat or use the individual actions.',
  busy: 'Running Python…', ready: 'A fresh scenario is ready.', expiry: 'Expired — confirm with a new request',
  notStarted: 'No cached entry yet', remaining: '{seconds} s remaining',
  pending: 'Entry still valid. Wait {seconds} s before the expiration step.',
  missExplain: 'MISS: Python executed the uncached view or calculation. The result now has a new lifetime.',
  hitExplain: 'HIT: Python read the cached result. Its original expiration time stays unchanged.',
  invalidatedExplain: 'PATCH saved the new city and deleted only this client’s detail key. The list was not invalidated.',
  clearExplain: 'cache.clear() removed every key from this task’s dedicated sandbox.',
  resetExplain: 'Reset switches to a fresh task namespace; old page-cache entries expire naturally. Other homework endpoints are unaffected.',
  writeExplain: 'cache.set() stored the sample with the applied lifetime.',
  deleteExplain: 'cache.delete() removed this sample key.',
  connectedExplain: 'A real backend probe succeeded. No simulated backend was used.',
  readExplain: 'Python inspected the current values without extending their lifetime.',
  invalidInput: 'Enter whole seconds from 1 to 3600.', requestError: 'Request failed. Check the server and backend connection.',
  missingExplain: 'cache.get() returned None: the key is absent or expired. Reading does not recreate it.',
  unspecified: 'no required lifetime',
  redisDiagnostics: 'Redis diagnostics', redisMarker: "Real PING and remaining TTL of a companion key with the response's lifetime.",
  controllerLabel: 'Launcher control service', stopServer: 'Stop server', stopped: 'Server stopped',
  starting: 'Starting the Django server…', stopping: 'Stopping the Django server…', processFailed: 'Process action failed.',
  controllerNote: 'Home stays available when all three Django servers are stopped. Restarting a server clears its LocMem cache. Redis runs independently.',
  networkError: 'Cannot reach this server. Start the presentation launcher.',
};
const pl = {
  practiceQuestions: 'Pytania i odpowiedzi', questionHint: 'Najpierw spróbuj odpowiedzieć, potem kliknij pytanie, aby rozwinąć wyjaśnienie.',
  moreQuestions: 'Chcesz więcej prostych pytań?', allQuestions: 'Wszystkie pytania wyświetlone',
  previousNote: 'Wybrano poprzednią instrukcję. Cache, liczniki i zapisane zmiany pozostają w bieżącym stanie; Następny krok powtarza operację.',
  home: 'Strona główna', serverLabel: 'Bieżący serwer Django', footer: 'Rzeczywiste żądania Django. Rzeczywisty cache. Objaśnienia krok po kroku.',
  homeEyebrow: 'TRZY BACKENDY · JEDNA LEKCJA', homeTitle: 'Zobacz, co naprawdę robi Twój cache.',
  homeLead: 'Prześledź żądanie od widoku Python do odpowiedzi z cache. Porównaj pamięć, pliki i Redis, krok po kroku.',
  howTitle: 'Jak działa ta prezentacja',
  howText: 'Launcher udostępnia ten panel sterowania na porcie 7999 i uruchamia trzy niezależne procesy Django na portach 8000, 8001 i 8002. Każdy używa własnych ustawień i kopii bazy do prezentacji. Przyciski runserver / Zatrzymaj serwer sterują procesami, a linki zadań prowadzą na ich porty. Redis jest osobną usługą przechowywania na porcie 6379.',
  isolation: 'Cache demonstracji jest oddzielony od cache pracy domowej. Reset tworzy nową przestrzeń kluczy zadania. Szybki pokaz używa 7–10 sekund; ustawienia zadania przywracają oryginalne czasy. Edycja zmienia tylko specjalnego klienta demonstracyjnego.',
  checking: 'Sprawdzanie…', online: 'Serwer i cache dostępne', offline: 'Niedostępne — sprawdź serwer / magazyn',
  refreshStatus: 'Odśwież status', chooseTask: 'Wybierz zadanie', task: 'ZADANIE', demonstration: 'Interaktywna demonstracja',
  scenario: 'Scenariusz', quick: 'Szybki pokaz', homework: 'Ustawienia zadania', ttl: 'Czas cache [s]', detailTtl: 'Czas szczegółów [s]',
  apply: 'Zastosuj i zacznij od nowa', reset: 'Reset scenariusza', guided: 'PREZENTACJA KROK PO KROKU', next: 'Następny krok', previous: 'Poprzedni krok',
  result: 'Wynik', duration: 'Czas na serwerze', queries: 'Zapytania SQL', response: 'Ostatnia odpowiedź', files: 'Rzeczywiste pliki cache',
  openApi: 'Otwórz oryginalne API / Debug Toolbar', history: 'Historia żądań', action: 'Operacja', original: 'Oryginalne zadanie',
  python: 'Co zrobił Python?', explainQuestion: 'Spróbuj wyjaśnić:', yourCode: 'Twój kod Python',
  adapterNote: 'Adapter demonstracji zmienia magazyn i czas ważności. Główna logika zadania pozostaje w plikach poniżej. Silnik prezentacji jest w cache_demo/engine.py.',
  note: 'Zastosowano: {ttl} s. Zadanie: {original} s. {detail} Zmiana pól wymaga przycisku Zastosuj i zacznij od nowa.',
  detailNote: 'Szczegóły: {ttl} s (zadanie: 60 s).',
  probe: 'Sprawdź backend', read: 'Pobierz / odczytaj', write: 'Zapisz przykład', delete: 'Usuń klucz', clear: 'Wyczyść magazyn zadania',
  list: 'Pobierz listę', detail: 'Pobierz szczegóły', update: 'Edytuj klienta demonstracyjnego',
  wait: 'Poczekaj na wygaśnięcie, a potem odczytaj ponownie. Odczyt HIT nie przedłuża czasu.',
  first: 'Wykonaj pierwsze żądanie. Oczekuj MISS i wykonania kodu Python.',
  second: 'Powtórz żądanie przed wygaśnięciem. Oczekuj HIT.',
  probeStep: 'Sprawdź skonfigurowany backend rzeczywistym zapisem i odczytem.',
  writeStep: 'Zapisz przykładowe dane z wybranym czasem ważności.', readStep: 'Odczytaj wcześniej zapisaną wartość.',
  clearStep: 'Wyczyść osobny magazyn zadania i sprawdź brak kluczy.',
  listStep: 'Pobierz listę i uruchom jej oddzielne odliczanie.', detailStep: 'Pobierz szczegóły i uruchom ich licznik.',
  hitDetail: 'Odczytaj szczegóły ponownie przed wygaśnięciem. Oczekuj HIT.',
  updateStep: 'Wyślij PATCH klienta demonstracyjnego. Kod zadania unieważnia jego szczegóły.',
  updatedDetail: 'Pobierz szczegóły po PATCH. Oczekuj MISS i nowego miasta.',
  staleList: 'Pobierz listę ponownie. Jeśli jej czas nie upłynął, zobaczysz stare miasto z cache.',
  complete: 'Koniec prezentacji. Zresetuj scenariusz albo użyj pojedynczych operacji.',
  busy: 'Python pracuje…', ready: 'Nowy scenariusz jest gotowy.', expiry: 'Wygasło — potwierdź nowym żądaniem',
  notStarted: 'Brak wpisu w cache', remaining: 'Pozostało {seconds} s',
  pending: 'Wpis jest jeszcze ważny. Poczekaj {seconds} s przed krokiem wygaśnięcia.',
  missExplain: 'MISS: Python wykonał widok lub obliczenia bez gotowego wyniku w cache. Wynik otrzymał nowy czas ważności.',
  hitExplain: 'HIT: Python odczytał wynik z cache. Pierwotny termin wygaśnięcia pozostaje bez zmian.',
  invalidatedExplain: 'PATCH zapisał nowe miasto i usunął tylko klucz szczegółów tego klienta. Lista nie została unieważniona.',
  clearExplain: 'cache.clear() usunęło wszystkie klucze z osobnego magazynu tego zadania.',
  resetExplain: 'Reset przełącza na nową przestrzeń kluczy zadania; stare wpisy cache widoków wygasają naturalnie. Oryginalne endpointy pozostają niezależne.',
  writeExplain: 'cache.set() zapisało przykład z zastosowanym czasem ważności.',
  deleteExplain: 'cache.delete() usunęło klucz przykładu.',
  connectedExplain: 'Rzeczywisty test backendu zakończył się powodzeniem. Backend nie był symulowany.',
  readExplain: 'Python sprawdził bieżące wartości bez przedłużania ich ważności.',
  invalidInput: 'Podaj całkowitą liczbę sekund od 1 do 3600.', requestError: 'Żądanie nie powiodło się. Sprawdź serwer i połączenie z cache.',
  missingExplain: 'cache.get() zwróciło None: klucza nie ma lub wygasł. Odczyt nie tworzy go ponownie.',
  unspecified: 'brak wymaganego czasu',
  redisDiagnostics: 'Diagnostyka Redis', redisMarker: 'Rzeczywisty PING i pozostały czas klucza pomocniczego z takim samym czasem ważności jak odpowiedź.',
  controllerLabel: 'Usługa sterowania launchera', stopServer: 'Zatrzymaj serwer', stopped: 'Serwer zatrzymany',
  starting: 'Uruchamianie serwera Django…', stopping: 'Zatrzymywanie serwera Django…', processFailed: 'Operacja na procesie nie powiodła się.',
  controllerNote: 'Strona główna działa także po zatrzymaniu wszystkich trzech serwerów Django. Restart serwera czyści jego cache LocMem. Redis działa niezależnie.',
  networkError: 'Nie można połączyć się z serwerem. Uruchom skrypt prezentacji.',
};
let language = new URLSearchParams(location.search).get('lang') || localStorage.getItem('cache-demo-language') || 'en';
if (!['en', 'pl'].includes(language)) language = 'en';
export const getLanguage = () => language;
export const bilingual = value => value[language];
export function t(key, values = {}) {
  let result = (language === 'pl' ? pl : en)[key] || key;
  for (const [name, value] of Object.entries(values)) result = result.replaceAll(`{${name}}`, value);
  return result;
}
export function translatePage() {
  document.documentElement.lang = language;
  document.querySelectorAll('[data-i18n]').forEach(element => element.textContent = t(element.dataset.i18n));
  document.querySelector('#language-toggle').textContent = language === 'en' ? 'PL / ENG ✓' : 'PL ✓ / ENG';
  localStorage.setItem('cache-demo-language', language);
}
export function toggleLanguage() {
  language = language === 'en' ? 'pl' : 'en';
  // Keep explicit navigation language and reload preferences in agreement.
  const url = new URL(location.href);
  url.searchParams.set('lang', language);
  window.history.replaceState(null, '', url);
  translatePage();
  document.dispatchEvent(new Event('languagechange'));
}
