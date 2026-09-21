# Article Search Site — dokumentacja wersji 1

## 1. Cel projektu

Rozszerzenie tworzy zaawansowaną wyszukiwarkę artykułów pod adresem:

```text
/articles/search/
```

Kryteria są zapisane jako parametry `GET`, dlatego wynik ma dynamiczny adres, który można skopiować, zapisać i ponownie otworzyć, np.:

```text
/articles/search/?from=2026-01-01&category=2&author=tom&tag=django&keyword=orm
```

Wyniki są wyświetlane bezpośrednio pod tym adresem. Nie ma przekierowania do `/done/`, ponieważ utrudniałoby ono nawigację, udostępnianie zapytania oraz zachowanie parametrów.

## 2. Gdzie znajduje się kod

Najważniejsze miejsca są oznaczone komentarzem `SEARCH-SITE`.

| Plik | Odpowiedzialność |
|---|---|
| `myproject/blog/models.py` | `Author`, jawna tabela `PostTag`, ochrona kategorii i autor zastępczy |
| `myproject/blog/views.py` | filtry, punktacja zgodności, paginacja, JSON dla podpowiedzi |
| `myproject/blog/urls.py` | adresy wyszukiwarki, szczegółów, pomocy i podpowiedzi |
| `myproject/blog/templates/article_search.html` | formularz i lista wyników |
| `myproject/blog/templates/article_detail.html` | pełny artykuł z podświetleniami |
| `myproject/blog/templates/search_help.html` | pomoc przełączana EN/PL |
| `myproject/blog/static/blog/search.js` | Tom Select, podpowiedzi i Mark.js |
| `myproject/blog/static/blog/styles.css` | wygląd i wersja mobilna |
| `myproject/blog/management/commands/seed_blog.py` | 2000 postów, 90 autorów i 40 tagów |
| `myproject/blog/tests.py` | automatyczne sprawdzenie najważniejszych reguł |

## 3. Modele i relacje

### `Author` — ciekawy

Każdy `Post` ma dokładnie jednego autora:

```python
author = models.ForeignKey(Author, on_delete=models.SET(get_deleted_author))
```

- `ForeignKey` realizuje relację „wiele postów — jeden autor”.
- Nie tworzymy tabeli pośredniej autor–post, ponieważ wersja 1 nie obsługuje współautorów.
- `models.SET(...)` wywołuje funkcję dopiero podczas usuwania autora.
- `get_deleted_author()` pobiera albo tworzy wspólny rekord `Author deleted` i zwraca jego klucz główny.
- Dzięki temu posty nie znikają po usunięciu ich autora.

`PROTECT` nie nadawałby się do tego wymagania: całkowicie blokowałby usunięcie używanego autora.

### `Category` — ciekawy

```python
category = models.ForeignKey(Category, on_delete=models.PROTECT)
```

`PROTECT` jest tu celowy. Kategorii używanej przez istniejący post nie można usunąć. Program zgłosi `ProtectedError`, zamiast pozostawić post bez wymaganej kategorii.

### `PostTag` — trudny i niewykorzystywany wcześniej w zadaniach

```python
class PostTag(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
```

Jest to jawna tabela pośrednia relacji wiele-do-wielu. Django zwykle tworzy taką tabelę automatycznie, ale jawny model pozwala ją zobaczyć, testować i później rozszerzyć, np. o datę dodania tagu.

Ograniczenie `UniqueConstraint(fields=["post", "tag"])` nie pozwala przypisać tego samego tagu dwa razy do jednego postu. Usunięcie tagu kasuje tylko rekordy pośrednie; sam post pozostaje.

Migracja `0003_search_site.py` najpierw kopiuje dotychczasowe automatyczne powiązania tagów do `PostTag`, a dopiero potem zastępuje stare pole nową relacją. Chroni to istniejące dane.

## 4. Wyszukiwanie

### Parametry wielokrotne — ciekawy

Pola `author`, `category`, `tag` i `keyword` mogą wystąpić w adresie kilka razy. Odczytuje je:

```python
request.GET.getlist("author")
```

Zwykłe `request.GET.get("author")` zwróciłoby tylko jedną wartość. Funkcja `_clean_values()` usuwa puste wpisy i powtórzenia, zachowując kolejność.

### Autorzy i kategorie

- kilku autorów oznacza autor A **lub** autor B;
- fragment `tom` może znaleźć `Tom`, `Thomas` i nazwisko zawierające `tom`;
- kilka kategorii oznacza kategorię A **lub** kategorię B;
- niewypełniony filtr nie ogranicza wyników;
- początek i koniec zakresu dat są wliczone.

Obiekt `Q` pozwala budować zapytania z operatorem „lub”:

```python
query |= Q(author__first_name__icontains=term)
```

Operator `|=` dopisuje kolejną możliwość do istniejącego warunku, a `icontains` porównuje tekst bez rozróżniania wielkości liter.

### Procent zgodności — trudny

Słowa kluczowe i tagi nie są filtrami obowiązkowymi. Każde kryterium daje jeden możliwy punkt:

```python
matched, total = _matching_score(post, keywords, tag_terms)
post.match_percent = round(matched / total * 100)
```

Przykład dla `python`, `orm`, `django`:

- 3 z 3 → 100%;
- 2 z 3 → 67%;
- 1 z 3 → 33%;
- 0 z 3 → post jest ukrywany.

Gdy nie podano słów ani tagów, procent nie jest wyświetlany. Wyniki z punktacją są sortowane najpierw według procentu, potem według daty publikacji.

Obliczenia są wykonywane w Pythonie. Przy 2000 postów jest to czytelne i wystarczająco szybkie rozwiązanie edukacyjne. W bardzo dużym serwisie należałoby użyć wyszukiwarki pełnotekstowej.

### Paginacja

```python
page_obj = Paginator(results, 5).get_page(request.GET.get("page"))
```

- `Paginator(results, 5)` dzieli listę po pięć elementów.
- `get_page()` łagodnie obsługuje brakujący lub nieprawidłowy numer strony.
- `_query_without_page()` zachowuje filtry w linkach następnej i poprzedniej strony, ale usuwa stary numer `page`.

## 5. JavaScript i biblioteki — trudny

### Tom Select

Tom Select zmienia zwykłe pola `<select multiple>` w kontrolki z tokenami. Autorzy i tagi pobierają podpowiedzi z małych widoków JSON po wpisaniu trzech znaków.

```javascript
fetch(`${element.dataset.url}?q=${encodeURIComponent(query)}`)
```

- `dataset.url` pochodzi z atrybutu `data-url` w HTML;
- `encodeURIComponent()` bezpiecznie zapisuje wpisany tekst w adresie;
- `fetch()` wykonuje żądanie `GET` bez przeładowania całej strony;
- odpowiedź JSON trafia do listy podpowiedzi.

Opcja `create` pozwala nacisnąć Enter i zachować fragment, nawet jeśli użytkownik nie wybierze konkretnej osoby lub tagu.

### Mark.js

Mark.js podświetla słowa kluczowe w tytule i treści bez zmieniania danych w bazie. Autorzy oraz tagi dostają osobne klasy CSS. Przycisk **Clear highlights**:

1. wywołuje `unmark()` dla tekstu;
2. usuwa klasy autora i tagów;
3. nie zmienia adresu ani wyników wyszukiwania.

Biblioteki są pobierane z CDN, więc interaktywne tokeny i podświetlanie wymagają internetu. Formularz nadal jest zwykłym formularzem HTML `GET`, dlatego podstawowe wyszukiwanie działa również bez JavaScriptu.

## 6. Seeder

Polecenie:

```powershell
.\.venv\Scripts\python.exe lessons\lesson22\myproject\manage.py seed_blog
```

usuwa stare dane bloga i tworzy:

- 10 kategorii;
- 90 losowych autorów;
- 40 tagów;
- 2000 postów;
- od 1 do 5 tagów dla każdego postu.

Najpierw każdy z 90 autorów dostaje co najmniej jeden post. Pozostałe posty otrzymują autorów losowo. Rekord `Author deleted` powstaje dopiero wtedy, gdy jest potrzebny, więc nie jest wliczany do 90 autorów testowych.

`bulk_create()` zapisuje wiele obiektów w znacznie mniejszej liczbie zapytań SQL niż wywoływanie `create()` w każdej iteracji.

## 7. Testy i uruchomienie

```powershell
cd lessons\lesson22\myproject
..\..\..\.venv\Scripts\python.exe manage.py migrate
..\..\..\.venv\Scripts\python.exe manage.py test blog
```

Testy obejmują między innymi punktację 67%, alternatywę autorów i kategorii, walidację dat, limit pięciu wyników, podpowiedzi od trzech znaków oraz reguły usuwania autora, kategorii i tagu.

## 8. Pomysły na wersję 2

- PostgreSQL i wyszukiwanie pełnotekstowe z rankingiem ważności pól;
- poprawianie literówek i wyszukiwanie podobnych wyrazów;
- zapisywanie nazwanych zestawów filtrów na koncie użytkownika;
- eksport wyników do CSV lub PDF;
- statystyki najpopularniejszych wyszukiwań;
- filtr minimalnego procentu zgodności;
- jawny `PostTag` rozszerzony o autora i datę przypisania tagu;
- testy JavaScriptu w przeglądarce.
