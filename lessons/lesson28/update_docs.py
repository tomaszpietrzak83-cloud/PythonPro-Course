"""Generate the four Polish study guides from the roadmap and live source code."""

import argparse
import ast
import html
import re
from pathlib import Path

from docs_pl_data import INTERESTING, STAGES


ROOT = Path(__file__).resolve().parent
APP = ROOT / "l28_pro" / "GameShelf"
BANNER = (
    "> Plik generowany przez `update_docs.py`. Status pochodzi z `roadmap_done.md`, "
    "a fragmenty kodu i numery linii z aktualnych plików. "
    "Opisy PL: `docs_pl_data.py`.\n\n"
)


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def completed_versions():
    sections = re.finditer(
        r"^## Version ([\d.]+) - [^\n]+\n(.*?)(?=^## |\Z)",
        read("roadmap_done.md"), re.MULTILINE | re.DOTALL,
    )
    return {match[1] for match in sections if "Status: done." in match[2]}


def source_block(location):
    path, separator, symbol = location.partition("::")
    source = read(path)
    if not separator:
        return path, 1, source
    node = ast.parse(source)
    for part in symbol.split("."):
        node = next(child for child in node.body if getattr(child, "name", None) == part)
    start = min([node.lineno] + [item.lineno for item in getattr(node, "decorator_list", [])])
    return path, start, "\n".join(source.splitlines()[start - 1:node.end_lineno])


def location_link(location):
    path, _, symbol = location.partition("::")
    line = 1
    if symbol and (ROOT / path).is_file():
        _, line, _ = source_block(location)
    label = path + (f" — {symbol}" if symbol else "")
    return f"[{label}]({path}#L{line})"


def stage_map():
    return {stage[0]: stage for stage in STAGES}


def defined_test_count():
    return sum(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
        for path in APP.glob("test*.py")
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
    )


def red(text):
    return f'<p style="color:red"><strong>Stan realizacji:</strong> {html.escape(text)}</p>\n'


def task_pl(done):
    text = "# Lekcja 28 — projekt końcowy GameShelf\n\n" + BANNER
    text += """## Cel i projekt bazowy

Zbuduj funkcjonalną aplikację Django **GameShelf** — osobistą bibliotekę gier PC.
Gość przegląda publiczny katalog, szczegóły oraz filtry; zalogowany użytkownik
zapisuje posiadane gry (`owned`) lub listę życzeń (`wishlist`). Rozwijaj projekt
małymi, działającymi wersjami.

Wykorzystaj istniejący projekt `l28_pro` i aplikację `GameShelf`. Nie twórz nowego
projektu, chyba że obecnego rzeczywiście nie da się naprawić.

## Wymagania podstawowe i aktualny stan

| Wymaganie | Stan | Gdzie szukać |
|---|---|---|
"""
    requirements = [
        ("Rejestracja, logowanie i wylogowanie przez Django", "0.2.0"),
        ("Publiczny katalog i szczegóły gry", "0.0.5"),
        ("Wyszukiwanie tytułu, gatunki i tagi", "0.1.4"),
        ("Posiadane gry i wishlisty", "0.2.3"),
        ("Prywatna biblioteka użytkownika", "0.2.4"),
        ("Status, ocena i prywatna notatka", "0.3.0"),
        ("Usuwanie własnego wpisu", "0.3.1"),
        ("Konfiguracja panelu admina", "0.4.0"),
        ("Faker: 100 gier FAKE i polecenie seed_db", "0.1.4.1"),
        ("Seeder użytkowników i bibliotek", "0.5.0"),
        ("Upload i wyświetlanie ImageField", "0.5.0.1"),
        ("Domyślna okładka i brakujące pliki", "0.6.0"),
        ("Testy najważniejszych funkcji", "0.7.0"),
        ("API REST", "0.9.0"),
        ("OpenAPI, Swagger UI i ReDoc", "0.9.0.1"),
        ("Operacje biblioteki w API i demonstracja Swaggera", "0.9.0.2"),
        ("Końcowe dopracowanie interfejsu", "0.10.0"),
    ]
    for title, version in requirements:
        state = "Wykonane" if version in done else "Zaplanowane"
        text += f"| {title} | {state} ({version}) | {location_link(stage_map()[version][4])} |\n"
    text += """
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
"""
    return text


def roadmap_pl(done):
    text = "# GameShelf — plan rozwoju po polsku\n\n" + BANNER
    text += "Każda wersja ma być użyteczna i sprawdzona przed rozpoczęciem następnej.\n\n"
    for version, title, goal, tasks, location in STAGES:
        text += f"## Wersja {version} — {title}\n\n"
        text += f"**Stan: {'wykonane' if version in done else 'zaplanowane'}.** Cel: {goal}\n\n"
        text += "\n".join(f"{index}. {task}." for index, task in enumerate(tasks.split("|"), 1))
        text += f"\n\n{'Implementacja' if version in done else 'Miejsce do rozbudowy'}: {location_link(location)}.\n\n"
    text += """## Reguła po każdej wersji

1. Czy serwer się uruchamia?
2. Czy funkcję można sprawdzić w przeglądarce?
3. Czy migracje modeli zostały zastosowane i zapisane?
4. Czy dodano lub zaktualizowano co najmniej jeden sensowny test?
5. Czy kod pozostaje zrozumiały i mały?

Bez działającego serwera i głównego przepływu nie rozpoczynaj następnej wersji.
Po zmianach uruchom `python lessons/lesson28/update_docs.py` z katalogu kursu.
"""
    return text


def lesson_done(done):
    latest = max(done, key=lambda item: tuple(map(int, item.split("."))))
    text = "# Lekcja 28 — materiał z komentarzami o realizacji\n\n" + BANNER
    text += red(f"Ukończono GameShelf do {latest}. W kodzie zdefiniowano {defined_test_count()} testów; wynik ich wykonania opisuje roadmap_done.md.")
    text += "\n## Zrealizowane etapy i miejsca w kodzie\n\n"
    for version, title, _, _, location in STAGES:
        if version in done:
            path, line, _ = source_block(location)
            label = html.escape(f"{version} — {title}")
            target = html.escape(f"{path}#L{line}", quote=True)
            where = html.escape(f"{path}, okolice linii {line}")
            text += (
                f'<p style="color:red"><strong>Wykonane: {label}.</strong> '
                f'Gdzie: <a href="{target}">{where}</a>.</p>\n\n'
            )
    api_ready = "0.9.0" in done
    swagger_ready = "0.9.0.1" in done
    comments = {
        "1": "Dokumentacja projektu i cztery pliki PL są generowane przez update_docs.py. Nie oznacza to jeszcze ukończenia dokumentacji REST API.",
        "2": ("Etap OpenAPI i Swagger jest zapisany jako wykonany; sprawdź routing i ustawienia projektu."
              if swagger_ready else "OpenAPI i Swagger w aplikacji GameShelf są jeszcze zaplanowane (0.9.0.1). Nie należy mylić plików Markdown ani JSON-owych podpowiedzi z dokumentacją Swagger."),
        "3": ("Integracja dokumentacji API: etap 0.9.0.1 wykonany; konfiguracja w l28_pro/l28_pro/settings.py i urls.py."
              if swagger_ready else "Ten fragment jest materiałem do późniejszego etapu 0.9.0.1. Obecne INSTALLED_APPS i routing nie konfigurują jeszcze DRF, schematu OpenAPI, Swagger UI ani ReDoc."),
        "4": ("Opis parametrów i odpowiedzi API należy utrzymywać razem ze schematem; zobacz etap 0.9.0.1."
              if swagger_ready else "extend_schema, OpenApiParameter i OpenApiResponse nie są jeszcze użyte w GameShelf. Filtry HTML są już w forms.py i filtered_games w views.py; ich dokumentacja API powstanie później."),
        "5": ("API ma własne widoki i serializery — ich opisy należy aktualizować z kodem."
              if api_ready else "Docstringi są już w kodzie Python, np. Game.cover_url i filtered_games. Pokazany niżej APIView pozostaje przykładem lekcyjnym; nie jest obecnym widokiem GameShelf."),
        "6": ("Dekoratory dokumentacji należy porównać z rzeczywistymi kodami odpowiedzi i walidacją."
              if swagger_ready else "Przykłady @extend_schema są planem do 0.9.0.1–0.9.0.2. Aktualne aplikacyjne POST-y biblioteki są zwykłymi widokami Django w GameShelf/views.py i korzystają z sesji oraz CSRF."),
        "7": "Analiza sentymentu to przykład możliwości API, a nie ukończona funkcja ani obowiązkowy zakres GameShelf. Nie dodawano tu usługi AI.",
        "8": f"Aktualny stan: do {latest}. Szczegóły wersji są w roadmapPL.md i roadmap_done.md; wybrane rzeczywiste bloki kodu objaśnia most_interesting.md.",
    }
    text += "\n---\n\n" + read("lesson-28.md").split("\n", 1)[0] + "\n"
    in_code = False
    for line in read("lesson-28.md").splitlines()[1:]:
        if line.startswith("```"):
            in_code = not in_code
        text += line + "\n"
        match = re.match(r"## (\d+)\.", line)
        if not in_code and match and match[1] in comments:
            text += "\n" + red(comments[match[1]]) + "\n"
    return text


def interesting():
    text = "# Najciekawsze bloki kodu GameShelf\n\n" + BANNER
    text += "To rzeczywisty kod projektu, nie uproszczone kopie. Numery linii i treść są odświeżane przez generator.\n\n"
    for title, location, explanation in INTERESTING:
        path, line, code = source_block(location)
        text += f"## {title}\n\nŹródło: {location_link(location)}.\n\n```python\n{code}\n```\n\n{explanation}\n\n"
    return text


def generated_documents():
    english_versions = re.findall(r"^## Version ([\d.]+) -", read("roadmap.md"), re.MULTILINE)
    if english_versions != [stage[0] for stage in STAGES]:
        raise ValueError("Zaktualizuj opisy etapów w docs_pl_data.py zgodnie z roadmap.md.")
    done = completed_versions()
    if not done or not done.issubset(stage_map()):
        raise ValueError("Brak statusów lub nieznana wersja w roadmap_done.md.")
    return {
        "taskPL.md": task_pl(done), "roadmapPL.md": roadmap_pl(done),
        "lesson-28-DONE.md": lesson_done(done), "most_interesting.md": interesting(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check freshness without writing files.")
    options = parser.parse_args()
    stale = []
    for name, text in generated_documents().items():
        path = ROOT / name
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            stale.append(name)
            if not options.check:
                path.write_text(text, encoding="utf-8", newline="\n")
    if options.check and stale:
        print("Nieaktualne pliki: " + ", ".join(stale))
        print("Uruchom: python lessons/lesson28/update_docs.py")
        return 1
    print("Dokumentacja PL aktualna." if not stale else "Zaktualizowano: " + ", ".join(stale))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
