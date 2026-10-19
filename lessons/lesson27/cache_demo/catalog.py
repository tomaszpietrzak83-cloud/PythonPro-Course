"""Task descriptions and source locations; presentation text is bilingual."""

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = {
    "l27_pro": {
        "port": 8000,
        "backend": "LocMemCache",
        "app": "myapp",
        "tasks": [1, 2, 3, 4, 5, 7, 8, 9],
    },
    "l27_pro_2": {
        "port": 8001,
        "backend": "FileBasedCache",
        "app": "myapp2",
        "tasks": [6],
    },
    "l27_pro_3": {
        "port": 8002,
        "backend": "Redis",
        "app": "myapp3",
        "tasks": [10],
    },
}
TITLES = {
    1: ("Local memory cache", "Cache w pamięci procesu"),
    2: ("Django Debug Toolbar", "Django Debug Toolbar"),
    3: ("Cache a complete API response", "Cache całej odpowiedzi API"),
    4: ("Write, read and expire a key", "Zapis, odczyt i wygaśnięcie klucza"),
    5: ("Clear cached data", "Czyszczenie danych cache"),
    6: ("File-based cache", "Cache plikowy"),
    7: (
        "Cache only expensive calculations",
        "Cache tylko kosztownych obliczeń",
    ),
    8: (
        "Separate list and detail lifetimes",
        "Oddzielny czas listy i szczegółów",
    ),
    9: (
        "Invalidate a detail after updating",
        "Unieważnienie szczegółów po edycji",
    ),
    10: ("Redis cache", "Cache Redis"),
}
REQUIREMENTS = {
    1: "Configure django.core.cache.backends.locmem.LocMemCache in settings.py. Start the server and check that the application starts without errors.",
    2: "Install and configure django-debug-toolbar as described in the lesson. Check that the toolbar appears in your application and you can open its Cache panel.",
    3: "Choose a simple GET API view, such as an object list. Use @cache_page to cache it for 60 seconds. Use Django Debug Toolbar to verify a cache miss on the first request and cache hits on subsequent requests within 60 seconds.",
    4: 'Open python manage.py shell. Import cache from django.core.cache. Run cache.set("my_key", "hello world", 30), then cache.get("my_key"). Wait 30 seconds and read it again. What happened?',
    5: "Find a manage.py command in the Django documentation that clears the whole cache and use it in a terminal. Mentor note: standard Django provides cache.clear(); there is no universal built-in manage.py cache-clear command.",
    6: "Switch settings.py to FileBasedCache and create its directory. Use the view from task 3. Check that new cache files appear after the first request. What do these files contain?",
    7: "Create a view with two data sources: a quick database query and a simulated expensive calculation using time.sleep(3). Use the low-level cache API to cache only the expensive result, rather than the entire response.",
    8: "Create a ModelViewSet. Use @method_decorator(cache_page(...)): cache list for 10 minutes and retrieve for 1 minute. Do not cache create, update or destroy. The current homework uses a manual detail key to support task 9.",
    9: "Extend task 8. After a successful update or partial_update, invalidate the retrieve cache of that particular object. Use post_save or perform_update. Understand Django view cache keys, or use your own keys.",
    10: "Install Redis, for example using Docker, and install django-redis. Configure CACHES to use Redis. Use Django Debug Toolbar to check communication with Redis. This configuration resembles a production setup.",
}
EXPLANATIONS = {
    1: (
        "Django writes and reads a probe using this process's memory cache. A different process has a different LocMem store.",
        "Django zapisuje i odczytuje wartość w pamięci tego procesu. Inny proces ma własny magazyn LocMem.",
    ),
    2: (
        "The HTML page allows Debug Toolbar to appear. Open Cache in the toolbar; use the original API link for homework inspection. The demo log is separate from the toolbar's request diagnostics.",
        "Strona HTML umożliwia wyświetlenie Debug Toolbar. Otwórz panel Cache; oryginalny endpoint służy do kontroli zadania. Historia demonstracji jest oddzielna od diagnostyki żądań toolbaru.",
    ),
    3: (
        "The adapter calls your original DRF view behind cache_page. MISS executes the view; HIT returns its previously rendered response. The adapter measures whether the view actually ran.",
        "Adapter wywołuje Twój widok DRF przez cache_page. MISS wykonuje widok; HIT zwraca wcześniej wyrenderowaną odpowiedź. Adapter sprawdza, czy widok faktycznie się wykonał.",
    ),
    4: (
        "cache.set stores a value with a lifetime. cache.get returns None when it is absent or expired. Reading a value does not extend its lifetime.",
        "cache.set zapisuje wartość z czasem ważności. cache.get zwraca None po wygaśnięciu lub gdy brak wartości. Odczyt nie przedłuża ważności.",
    ),
    5: (
        "This exercise calls cache.clear() on a dedicated memory sandbox, then reads two keys. The sandbox is separate from every other task and from the homework cache.",
        "Ćwiczenie wywołuje cache.clear() w osobnym magazynie pamięci, a potem odczytuje dwa klucze. Magazyn jest oddzielny od pozostałych zadań i cache pracy domowej.",
    ),
    6: (
        "Your product view runs behind FileBasedCache. The file list shows real .djcache files in the presentation directory. Expiration makes entries unusable; it does not guarantee immediate file removal. Files store serialized data, not readable JSON.",
        "Twój widok produktów korzysta z FileBasedCache. Lista pokazuje rzeczywiste pliki .djcache w katalogu prezentacji. Wygaśnięcie blokuje użycie wpisu, ale nie gwarantuje natychmiastowego usunięcia pliku. Pliki przechowują serializowane dane, a nie czytelny JSON.",
    ),
    7: (
        "Your get_complex_product_stats function sleeps for 3 seconds only on MISS. The adapter supplies a demo cache and timeout. The simple database query executes on every request, including HIT.",
        "Twoja funkcja get_complex_product_stats czeka 3 sekundy tylko przy MISS. Adapter przekazuje cache i czas demonstracji. Proste zapytanie do bazy wykonuje się zawsze, również przy HIT.",
    ),
    8: (
        "Your ClientViewSet serves list and detail. The demo subclass changes the cache namespace and timeouts. List uses cache_page; detail uses a manual object key. PATCH remains uncached.",
        "Twój ClientViewSet obsługuje listę i szczegóły. Podklasa demonstracyjna zmienia przestrzeń kluczy i czasy. Lista używa cache_page, szczegóły własnego klucza. PATCH nie jest cachowany.",
    ),
    9: (
        "PATCH updates a dedicated demo client through your perform_update method. cache.delete removes its detail key. The next detail read is a MISS with the new city. A cached list may still show the old city until it expires.",
        "PATCH edytuje specjalnego klienta demonstracyjnego przez Twoją metodę perform_update. cache.delete usuwa klucz szczegółów. Następny odczyt to MISS z nowym miastem. Lista może pokazywać stare miasto aż do wygaśnięcia.",
    ),
    10: (
        "The real Redis connection is probed before the demo. Your DRF product view uses cache_page with the Redis demo alias. No fallback cache is substituted if Redis is unavailable.",
        "Demonstracja sprawdza rzeczywiste połączenie z Redis. Twój widok produktów DRF używa cache_page z aliasem demonstracyjnym Redis. Niedostępny Redis nie jest zastępowany innym cache.",
    ),
}


def task_project(number):
    return next(
        name for name, project in PROJECTS.items() if number in project["tasks"]
    )


def polish_requirements():
    """Read the original homework instead of maintaining a second Polish copy."""
    text = (ROOT / "tasks.md").read_text(encoding="utf-8")
    return {
        int(section[:2]): re.sub(
            r"<[^>]+>", "", section.split("\n", 1)[1].strip()
        )
        for section in text.split("## TASK ")[1:]
    }


def source_files(number):
    """Use a fixed allowlist: the browser cannot request arbitrary local files."""
    project = task_project(number)
    app = PROJECTS[project]["app"]
    paths = [ROOT / project / app / "views.py"]
    if number in (1, 2, 6, 10):
        paths.insert(0, ROOT / project / project / "settings.py")
    if number in (4, 5):
        paths = [ROOT / f"task{number:02}.py"]
    if number in (8, 9):
        paths.append(ROOT / project / app / "serializers.py")
    # Settings contain a development secret key; show only the cache configuration.
    result = []
    for path in paths:
        content = path.read_text(encoding="utf-8")
        if path.name == "settings.py":
            wanted = (
                {"CACHES"}
                if number != 2
                else {
                    "DEBUG_TOOLBAR_INSTALLED",
                    "INSTALLED_APPS",
                    "MIDDLEWARE",
                    "INTERNAL_IPS",
                }
            )
            snippets = []
            for node in ast.parse(content).body:
                if isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id in wanted
                    for target in node.targets
                ):
                    snippets.append(ast.get_source_segment(content, node))
                elif (
                    number == 2
                    and isinstance(node, ast.If)
                    and "DEBUG_TOOLBAR_INSTALLED" in ast.unparse(node.test)
                ):
                    snippets.append(ast.get_source_segment(content, node))
            content = "\n\n".join(snippets)
        result.append({"path": str(path.relative_to(ROOT)), "code": content})
    return result
