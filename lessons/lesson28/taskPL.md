# Lekcja 28 — projekt końcowy GameShelf

> Plik generowany przez `update_docs.py`. Status pochodzi z `roadmap_done.md`, a fragmenty kodu i numery linii z aktualnych plików. Opisy PL: `docs_pl_data.py`.

## Cel i projekt bazowy

Zbuduj funkcjonalną aplikację Django **GameShelf** — osobistą bibliotekę gier PC.
Gość przegląda publiczny katalog, szczegóły oraz filtry; zalogowany użytkownik
zapisuje posiadane gry (`owned`) lub listę życzeń (`wishlist`). Rozwijaj projekt
małymi, działającymi wersjami.

Wykorzystaj istniejący projekt `l28_pro` i aplikację `GameShelf`. Nie twórz nowego
projektu, chyba że obecnego rzeczywiście nie da się naprawić.

## Wymagania podstawowe i aktualny stan

| Wymaganie | Stan | Gdzie szukać |
|---|---|---|
| Rejestracja, logowanie i wylogowanie przez Django | Wykonane (0.2.0) | [l28_pro/GameShelf/views.py — register](l28_pro/GameShelf/views.py#L21) |
| Publiczny katalog i szczegóły gry | Wykonane (0.0.5) | [l28_pro/GameShelf/views.py — game_detail](l28_pro/GameShelf/views.py#L74) |
| Wyszukiwanie tytułu, gatunki i tagi | Wykonane (0.1.4) | [l28_pro/GameShelf/views.py — game_suggestions](l28_pro/GameShelf/views.py#L59) |
| Posiadane gry i wishlisty | Wykonane (0.2.3) | [l28_pro/GameShelf/views.py — add_to_wishlist](l28_pro/GameShelf/views.py#L106) |
| Prywatna biblioteka użytkownika | Wykonane (0.2.4) | [l28_pro/GameShelf/views.py — my_library](l28_pro/GameShelf/views.py#L124) |
| Status, ocena i prywatna notatka | Wykonane (0.3.0) | [l28_pro/GameShelf/forms.py — UserGameEditForm](l28_pro/GameShelf/forms.py#L42) |
| Usuwanie własnego wpisu | Wykonane (0.3.1) | [l28_pro/GameShelf/views.py — remove_library_entry](l28_pro/GameShelf/views.py#L167) |
| Konfiguracja panelu admina | Wykonane (0.4.0) | [l28_pro/GameShelf/admin.py — GameAdmin](l28_pro/GameShelf/admin.py#L50) |
| Faker: 100 gier FAKE i polecenie seed_db | Wykonane (0.1.4.1) | [l28_pro/GameShelf/management/commands/seed_db.py — Command.handle](l28_pro/GameShelf/management/commands/seed_db.py#L144) |
| Seeder użytkowników i bibliotek | Wykonane (0.5.0) | [l28_pro/GameShelf/management/commands/seed_db.py — Command.seed_libraries](l28_pro/GameShelf/management/commands/seed_db.py#L115) |
| Upload i wyświetlanie ImageField | Wykonane (0.5.0.1) | [l28_pro/GameShelf/test_covers.py — CoverUploadTests.test_admin_upload_stores_file_path_and_displays_cover](l28_pro/GameShelf/test_covers.py#L53) |
| Domyślna okładka i brakujące pliki | Wykonane (0.6.0) | [l28_pro/GameShelf/models.py — Game.cover_url](l28_pro/GameShelf/models.py#L58) |
| Testy najważniejszych funkcji | Wykonane (0.7.0) | [l28_pro/GameShelf/test_workflows.py — PlayerWorkflowTests](l28_pro/GameShelf/test_workflows.py#L8) |
| API REST | Wykonane (0.9.0) | [l28_pro/l28_pro/urls.py](l28_pro/l28_pro/urls.py#L1) |
| OpenAPI, Swagger UI i ReDoc | Zaplanowane (0.9.0.1) | [l28_pro/l28_pro/urls.py](l28_pro/l28_pro/urls.py#L1) |
| Operacje biblioteki w API i demonstracja Swaggera | Zaplanowane (0.9.0.2) | [l28_pro/l28_pro/urls.py](l28_pro/l28_pro/urls.py#L1) |
| Końcowe dopracowanie interfejsu | Zaplanowane (0.10.0) | [l28_pro/GameShelf/templates/base.html](l28_pro/GameShelf/templates/base.html#L1) |

## Sugerowane modele

- **Game:** `title`, `description`, `release_date`, `cover`, `studio`, `genres`,
  `tags`; dla późniejszego importu także `source_url` i `external_id`.
- **Studio:** `name`; opcjonalnie w przyszłości `description` i `logo`.
- **Genre** i **Tag:** `name`, `slug`.
- **UserGame:** `user`, `game`, `list_type`, `play_status`, `rating`, `note`;
  sugerowane dalsze metadane: `created_at`, `updated_at`.

Są to propozycje, a nie stwierdzenie, że wszystkie pola już istnieją.
`list_type` ma wartości `owned` i `wishlist`. Statusy to `not_started`, `playing`,
`completed`, `abandoned`. Jeden użytkownik nie może mieć dwóch wpisów tej samej gry.

## Funkcje publiczne

Gość może otworzyć stronę główną, katalog i szczegóły, wyszukać tytuł oraz
filtrować po gatunku i tagu. W tym projekcie wyszukiwarka dodatkowo podpowiada
do trzech tytułów od pierwszego znaku, korzystając z lokalnej bazy.

## Funkcje zalogowanego użytkownika

Może zapisać grę do posiadanych lub wishlisty, przenieść wishlistę do posiadanych,
przeglądać własną bibliotekę i jej filtry, zmienić status, ocenę i prywatną
notatkę oraz usunąć własny wpis. Obecna reguła: posiadana gra pozostaje `owned`
przy żądaniu dodania jej do wishlisty. Ocena wynosi 1–10 albo pozostaje pusta.

## Admin

Skonfiguruj `list_display`, `search_fields`, `list_filter`, sensowne sortowanie,
edycję inline i przydatne własne metody. Przykłady: licznik zapisów gry,
wyszukiwanie po tytule/studiu, filtry gatunku/tagu/daty oraz powiązane wpisy
użytkowników dostępne przy grze.

## Wymagane dane testowe

Faker i `python manage.py seed_db` domyślnie tworzą 100 fikcyjnych gier ze studiami.
Każda ma gatunek **FAKE** (`fake`) i tag **FAKE** (`fake`). Wykorzystaj istniejące
filtry katalogu. Trwałe identyfikatory seedowania i powtarzalny `--seed` zapobiegają
duplikatom; `--games 100` steruje liczbą. Etap 0.5.0 rozszerza to samo polecenie
o konta testowe i biblioteki. Ręczne dane i edycje mają zostać zachowane.

```powershell
python manage.py seed_db --games 100 --users 3 --entries-per-user 10
```

Opcjonalny późniejszy import RAWG nie zastępuje seedera:

```powershell
python manage.py import_games --genre action --limit 100
```

Najpierw ma działać lokalny katalog; klucz zewnętrznego API przechowuj poza kodem.

## Wymaganie dotyczące obrazów

`Game.cover` musi być Django `ImageField`. Etap 0.5.0.1 obejmuje media storage,
upload lokalnego obrazu przez admina oraz wyświetlanie w katalogu i szczegółach.
Baza przechowuje ścieżkę, sam plik znajduje się w media storage. Sam URL obrazu
nie zastępuje tego wymagania. Placeholder umożliwia pracę bez okładek; prawdziwe
obrazy z importu będą później zapisywane do tego samego storage.

## Frontend

Zacznij od szablonów Django i CSS. Po ukończeniu backendu możesz wykorzystać
[Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/javascript/),
[Flowbite](https://flowbite.com/docs/getting-started/introduction/) lub
[htmx](https://htmx.org/docs/). Priorytetem pozostają modele, widoki, formularze,
uwierzytelnianie i testy; końcowe dopracowanie interfejsu to osobny etap.

## Wymagane API i Swagger

W 0.9.0 dodaj DRF: listę/szczegóły gier, gatunki, tagi i bibliotekę bieżącego
użytkownika. W 0.9.0.1 skonfiguruj drf-spectacular, OpenAPI, Swagger UI i ReDoc.
Opisz parametry, przykłady, pola, błędy, uwierzytelnianie sesją i CSRF.

W 0.9.0.2 dodaj POST, szczegółowe GET, PATCH i DELETE dla własnych wpisów.
W Swaggerze pokaż: znalezienie FAKE, dodanie wishlisty, przejście do owned,
błąd oceny i usunięcie. API jest dodatkiem do stron HTML.

## Lista kontrolna oddania projektu

Sprawdź stronę główną, katalog, szczegóły, konta, obie listy, bibliotekę, admina,
seeder 100 FAKE, testy i ImageField. Import zewnętrzny jest opcjonalny. API ze
Swaggerem jest wymagane w finalnej wersji. Pełny aktualny plan: [roadmapPL.md](roadmapPL.md).
