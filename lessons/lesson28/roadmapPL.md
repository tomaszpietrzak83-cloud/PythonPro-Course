# GameShelf — plan rozwoju po polsku

> Plik generowany przez `update_docs.py`. Status pochodzi z `roadmap_done.md`, a fragmenty kodu i numery linii z aktualnych plików. Opisy PL: `docs_pl_data.py`.

Każda wersja ma być użyteczna i sprawdzona przed rozpoczęciem następnej.

## Wersja 0.0.1 — Uruchomienie projektu

**Stan: wykonane.** Cel: Uruchomić istniejący projekt Django.

1. Użyć l28_pro i aplikacji GameShelf.
2. Dodać aplikację do INSTALLED_APPS.
3. Utworzyć i zastosować migracje.
4. Uruchomić serwer i django check.

Implementacja: [l28_pro/l28_pro/settings.py](l28_pro/l28_pro/settings.py#L1).

## Wersja 0.0.2 — Pierwsza strona

**Stan: wykonane.** Cel: Wyświetlić stronę główną.

1. Utworzyć routing aplikacji.
2. Dodać widok home i szablon.
3. Podłączyć routing projektu.
4. Dodać odnośnik do admina.

Implementacja: [l28_pro/GameShelf/views.py — home](l28_pro/GameShelf/views.py#L17).

## Wersja 0.0.3 — Pierwszy model

**Stan: wykonane.** Cel: Przechowywać gry w bazie.

1. Dodać Game: title, description, release_date.
2. Utworzyć i zastosować migrację.
3. Zarejestrować model w adminie.
4. Przygotować administratora i ręcznie dodać gry.

Implementacja: [l28_pro/GameShelf/models.py — Game](l28_pro/GameShelf/models.py#L39).

## Wersja 0.0.4 — Katalog gier

**Stan: wykonane.** Cel: Wyświetlić gry z bazy pod /games/.

1. Utworzyć widok listy i szablon.
2. Pokazać tytuły oraz skrócone opisy.
3. Połączyć katalog ze stroną główną odnośnikami.

Implementacja: [l28_pro/GameShelf/views.py — game_list](l28_pro/GameShelf/views.py#L52).

## Wersja 0.0.5 — Szczegóły gry

**Stan: wykonane.** Cel: Każda gra ma własny adres.

1. Dodać widok szczegółów i adres z ID lub slugiem.
2. Utworzyć szablon.
3. Podlinkować gry w katalogu.
4. Zwracać 404 przez get_object_or_404 dla nieistniejącej gry.

Implementacja: [l28_pro/GameShelf/views.py — game_detail](l28_pro/GameShelf/views.py#L74).

## Wersja 0.1.0 — Minimalna użyteczna aplikacja

**Stan: wykonane.** Cel: Zapewnić spójny i działający katalog.

1. Dodać wspólną nawigację i CSS.
2. Poprawić stronę główną, listę i szczegóły.
3. Dodać testy głównej strony, katalogu i szczegółów.

Implementacja: [l28_pro/GameShelf/templates/base.html](l28_pro/GameShelf/templates/base.html#L1).

## Wersja 0.1.1 — Studia

**Stan: wykonane.** Cel: Powiązać gry ze studiami.

1. Utworzyć Studio.
2. Dodać ForeignKey w Game.
3. Przygotować migrację i admina.
4. Wyświetlić nazwę studia w katalogu i szczegółach.

Implementacja: [l28_pro/GameShelf/models.py — Studio](l28_pro/GameShelf/models.py#L7).

## Wersja 0.1.2 — Gatunki

**Stan: wykonane.** Cel: Filtrować gry według gatunku.

1. Utworzyć Genre.
2. Dodać ManyToManyField do Game.
3. Zaktualizować admina.
4. Wyświetlać gatunki w szczegółach.
5. Dodać filtr katalogu; nazwy gatunków zgodne z RAWG.

Implementacja: [l28_pro/GameShelf/forms.py — CatalogFilterForm](l28_pro/GameShelf/forms.py#L6).

## Wersja 0.1.3 — Tagi

**Stan: wykonane.** Cel: Dodać elastyczne filtrowanie.

1. Utworzyć Tag i relację wiele-do-wielu.
2. Zaktualizować admina.
3. Wyświetlać tagi w szczegółach.
4. Filtrować katalog po tagu, także łącznie z gatunkiem.

Implementacja: [l28_pro/GameShelf/models.py — Tag](l28_pro/GameShelf/models.py#L28).

## Wersja 0.1.4 — Wyszukiwanie

**Stan: wykonane.** Cel: Ułatwić znalezienie gry po tytule.

1. Dodać formularz i wyszukiwanie tytułu.
2. Opcjonalnie wyszukiwać studio.
3. Zachować czytelne parametry URL.
4. Od pierwszego znaku sugerować maksymalnie 3 tytuły z lokalnej bazy.

Implementacja: [l28_pro/GameShelf/views.py — game_suggestions](l28_pro/GameShelf/views.py#L59).

## Wersja 0.1.4.1 — Seeder 100 fikcyjnych gier

**Stan: wykonane.** Cel: Przygotować lokalny katalog do ćwiczeń przed logowaniem.

1. Dodać polecenie seed_db wykorzystujące Faker.
2. Domyślnie utworzyć 100 fikcyjnych gier z opisami, datami i studiami.
3. Każdej grze przypisać gatunek FAKE i tag FAKE (slug fake).
4. Stosować trwały identyfikator seedowania i nie nadpisywać ręcznych danych.
5. Obsłużyć --games oraz powtarzalny --seed.
6. Testować liczbę gier, oznaczenia FAKE i ponowne uruchomienie.

Implementacja: [l28_pro/GameShelf/management/commands/seed_db.py — Command.handle](l28_pro/GameShelf/management/commands/seed_db.py#L144).

## Wersja 0.2.0 — Rejestracja i logowanie

**Stan: wykonane.** Cel: Umożliwić użytkownikowi utworzenie konta i korzystanie z sesji.

1. Dodać adresy logowania i wylogowania.
2. Utworzyć formularz i szablon logowania.
3. Dostosować nawigację do sesji.
4. Dodać widok i szablon rejestracji.
5. Sprawdzić rejestrację w przeglądarce.

Implementacja: [l28_pro/GameShelf/views.py — register](l28_pro/GameShelf/views.py#L21).

## Wersja 0.2.1 — Model UserGame

**Stan: wykonane.** Cel: Zapisać związek użytkownika z grą.

1. Połączyć UserGame z użytkownikiem i Game.
2. Dodać list_type: owned/wishlist.
3. Wymusić unikalność pary użytkownik–gra.
4. Zarejestrować model w adminie.
5. Przetestować ograniczenie unikalności.

Implementacja: [l28_pro/GameShelf/models.py — UserGame](l28_pro/GameShelf/models.py#L69).

## Wersja 0.2.2 — Dodawanie do posiadanych

**Stan: wykonane.** Cel: Zapisywać gry jako posiadane.

1. Dodać przycisk w szczegółach.
2. Zapisywać przez POST i wymagać logowania.
3. Przenosić istniejący wpis z wishlisty do owned.
4. Wyświetlić komunikat sukcesu.

Implementacja: [l28_pro/GameShelf/views.py — add_to_owned](l28_pro/GameShelf/views.py#L93).

## Wersja 0.2.3 — Wishlist

**Stan: wykonane.** Cel: Zapisywać gry na liście życzeń.

1. Dodać przycisk i widok POST.
2. Wymagać logowania.
3. Wybrać regułę dla posiadanej gry: obecnie pozostaje owned.
4. Pokazać komunikat i zapobiegać duplikatom.

Implementacja: [l28_pro/GameShelf/views.py — add_to_wishlist](l28_pro/GameShelf/views.py#L106).

## Wersja 0.2.4 — Moja biblioteka

**Stan: wykonane.** Cel: Wyświetlać wyłącznie wpisy zalogowanego użytkownika.

1. Dodać widok chroniony logowaniem.
2. Pokazać posiadane gry i wishlistę.
3. Dodać filtry all/owned/wishlist.
4. Dodać My Library do nawigacji.

Implementacja: [l28_pro/GameShelf/views.py — my_library](l28_pro/GameShelf/views.py#L124).

## Wersja 0.3.0 — Status, ocena i notatka

**Stan: wykonane.** Cel: Spersonalizować bibliotekę.

1. Dodać play_status, rating i note do UserGame.
2. Utworzyć formularz i stronę edycji wpisu.
3. Walidować ocenę (w projekcie 1–10 albo brak).
4. Udostępnić statusy not_started/playing/completed/abandoned.
5. Zachować prywatność notatek.

Implementacja: [l28_pro/GameShelf/forms.py — UserGameEditForm](l28_pro/GameShelf/forms.py#L42).

## Wersja 0.3.1 — Usuwanie z biblioteki

**Stan: wykonane.** Cel: Usuwać własne wpisy bez usuwania gry z katalogu.

1. Dodać przycisk lub odnośnik usuwania.
2. Usuwać wyłącznie przez POST.
3. Dodać potwierdzenie lub jednoznaczną etykietę.
4. Wyświetlać komunikat.
5. Przetestować ochronę cudzych wpisów.

Implementacja: [l28_pro/GameShelf/views.py — remove_library_entry](l28_pro/GameShelf/views.py#L167).

## Wersja 0.4.0 — Wygodniejszy panel admina

**Stan: wykonane.** Cel: Sprawnie zarządzać katalogiem i kolekcjami.

1. Dodać list_display, search_fields i list_filter.
2. Ustawić sensowne sortowanie.
3. Użyć edycji inline tam, gdzie pomaga.
4. Dodać własne metody, np. licznik użytkowników zapisujących grę.

Implementacja: [l28_pro/GameShelf/admin.py — GameAdmin](l28_pro/GameShelf/admin.py#L50).

## Wersja 0.5.0 — Rozszerzony seeder

**Stan: wykonane.** Cel: Generować powtarzalne dane testowe i biblioteki.

1. Rozszerzyć istniejące seed_db i zachować identyfikatory.
2. Nadal domyślnie generować 100 gier z gatunkiem i tagiem FAKE.
3. Wykorzystać Faker dla studiów, gatunków, tagów, gier, użytkowników i wpisów.
4. Dodać jawne opcje --users i --entries-per-user.
5. Zachować unikalność wpisów i bezpieczeństwo ponownych uruchomień.

Implementacja: [l28_pro/GameShelf/management/commands/seed_db.py — Command.seed_libraries](l28_pro/GameShelf/management/commands/seed_db.py#L115).

## Wersja 0.5.0.1 — Upload i wyświetlanie obrazów

**Stan: wykonane.** Cel: Zweryfikować ImageField przed importem prawdziwych okładek.

1. Dodać opcjonalne Game.cover i Pillow.
2. Przygotować migrację.
3. Skonfigurować MEDIA_ROOT, MEDIA_URL i lokalne serwowanie mediów.
4. Przesłać lokalny obraz przez admina.
5. Wyświetlić go w katalogu i szczegółach; sprawdzić brak okładki.
6. Przechowywać plik w media, a jego ścieżkę w bazie; bez zewnętrznego importu.

Implementacja: [l28_pro/GameShelf/test_covers.py — CoverUploadTests.test_admin_upload_stores_file_path_and_displays_cover](l28_pro/GameShelf/test_covers.py#L53).

## Wersja 0.6.0 — Okładki

**Stan: wykonane.** Cel: Ujednolicić wygląd katalogu i obsłużyć brak obrazu.

1. Wykorzystać istniejącą konfigurację mediów i ImageField.
2. Dodać domyślny placeholder.
3. Wyświetlać okładki w katalogu i szczegółach.
4. Nie przerywać działania strony przy braku pliku.

Implementacja: [l28_pro/GameShelf/models.py — Game.cover_url](l28_pro/GameShelf/models.py#L58).

## Wersja 0.7.0 — Testy najważniejszych funkcji

**Stan: wykonane.** Cel: Chronić główne zachowania aplikacji testami.

1. Testować tworzenie modeli.
2. Sprawdzić statusy HTTP katalogu i szczegółów.
3. Sprawdzić logowanie przy dodawaniu do owned i wishlist.
4. Sprawdzić brak duplikatów.
5. Sprawdzić ochronę cudzych wpisów przed edycją.
6. Przeprowadzić test całego przepływu z rzeczywistą sesją i CSRF.

Implementacja: [l28_pro/GameShelf/test_workflows.py — PlayerWorkflowTests](l28_pro/GameShelf/test_workflows.py#L8).

## Wersja 0.8.0 — Opcjonalny import zewnętrzny

**Stan: wykonane.** Cel: Importować rzeczywiste dane gier, np. z RAWG.

1. Wybrać źródło i przechowywać klucz API poza kodem.
2. Dodać polecenie import_games.
3. Zacząć od jednego gatunku i małego limitu.
4. Zapisywać zewnętrzne ID, aby uniknąć duplikatów.
5. Pobierać okładki do media i przypisywać je do Game.cover; URL źródła może być metadanymi.
6. Czytelnie obsłużyć błędy API.

Implementacja: [l28_pro/GameShelf/management/commands/import_games.py — Command.handle](l28_pro/GameShelf/management/commands/import_games.py#L72).

## Wersja 0.9.0 — Podstawowe API

**Stan: wykonane.** Cel: Udostępnić API REST przed dodaniem Swaggera.

1. Skonfigurować Django REST Framework.
2. Dodać serializery gier, gatunków, tagów i wpisów biblioteki.
3. Dodać publiczne GET /api/v1/games/, /api/v1/games/{id}/, /api/v1/genres/ i /api/v1/tags/.
4. Obsłużyć q, genre i tag tak jak w katalogu.
5. Dodać chronione GET /api/v1/library/ tylko dla bieżącego użytkownika.
6. Testować filtry, 404, logowanie i prywatność notatek.

Implementacja: [l28_pro/l28_pro/urls.py](l28_pro/l28_pro/urls.py#L1).

## Wersja 0.9.0.1 — OpenAPI i Swagger UI

**Stan: wykonane.** Cel: Udokumentować działające API.

1. Skonfigurować drf-spectacular jako generator schematu.
2. Dodać /api/schema/, /api/schema/swagger-ui/ i /api/schema/redoc/.
3. Dodać opisy, tagi i przykłady przez @extend_schema.
4. Opisać q, genre i tag, w tym FAKE.
5. Opisać pola, uwierzytelnianie sesją, CSRF i rzeczywiste kody odpowiedzi.
6. Walidować schemat i testować adresy dokumentacji.
7. W Swagger Try it out wywołać listę, filtr FAKE, szczegóły i brakującą grę.

Implementacja: [l28_pro/l28_pro/urls.py](l28_pro/l28_pro/urls.py#L1).

## Wersja 0.9.0.2 — Dodatkowe endpointy i demonstracja Swaggera

**Stan: zaplanowane.** Cel: Pokazać walidację i różne metody HTTP na bibliotece.

1. Dodać POST /api/v1/library/ (201, duplikat 400).
2. Dodać GET /api/v1/library/{id}/.
3. Dodać PATCH do list_type, statusu, oceny i notatki.
4. Dodać DELETE własnego wpisu.
5. Ograniczać każdy odczyt i zapis do request.user; cudze ID zwracają 404.
6. Rozszerzyć OpenAPI o walidację i kody 200/201/204/400/404 oraz błędy logowania i CSRF.
7. Przetestować poprawne i błędne operacje.
8. W Swaggerze znaleźć FAKE, dodać wishlistę, przenieść do owned, pokazać błąd oceny i usunąć wpis.

Miejsce do rozbudowy: [l28_pro/l28_pro/urls.py](l28_pro/l28_pro/urls.py#L1).

## Wersja 0.10.0 — Dopracowanie interfejsu

**Stan: zaplanowane.** Cel: Ułatwić codzienne korzystanie z gotowego backendu.

1. Przejrzeć home, katalog, szczegóły, logowanie/rejestrację i bibliotekę.
2. Wybrać Bootstrap, Flowbite lub htmx.
3. Poprawić nawigację, formularze, karty i odstępy.
4. Dodać puste stany oraz komunikaty.
5. Sprawdzić wąski ekran.

Miejsce do rozbudowy: [l28_pro/GameShelf/templates/base.html](l28_pro/GameShelf/templates/base.html#L1).

## Wersja 1.0.0 — Przegląd końcowy

**Stan: zaplanowane.** Cel: Oddać kompletny projekt zaliczeniowy.

1. Uruchomić wszystkie testy i django check.
2. Przeklikać główny przepływ.
3. Usunąć martwy kod i zapisać migracje.
4. Sprawdzić brak sekretów w Git.
5. Uaktualnić README i opisać aplikację.
6. Potwierdzić seeder 100 FAKE, upload ImageField oraz API i Swagger z etapów 0.9.0.1/0.9.0.2.

Miejsce do rozbudowy: [l28_pro/README.md](l28_pro/README.md#L1).

## Reguła po każdej wersji

1. Czy serwer się uruchamia?
2. Czy funkcję można sprawdzić w przeglądarce?
3. Czy migracje modeli zostały zastosowane i zapisane?
4. Czy dodano lub zaktualizowano co najmniej jeden sensowny test?
5. Czy kod pozostaje zrozumiały i mały?

Bez działającego serwera i głównego przepływu nie rozpoczynaj następnej wersji.
Po zmianach uruchom `python lessons/lesson28/update_docs.py` z katalogu kursu.
