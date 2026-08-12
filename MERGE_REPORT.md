# Raport scalenia repozytoriow lekcyjnych

Data wykonania: 2026-08-12
Repo docelowe: `C:\Users\Tomek\Documents\Developer\PythonPro-Course`
Branch docelowy: `main`

## Cel

Celem bylo uporzadkowanie nauki Pythona w jednym repozytorium `PythonPro-Course`, bez przepisywania starej historii Gita i bez dodawania lokalnych virtualenvow.

Zakres obejmowal tylko repozytoria lekcyjne `Lesson*` / `lesson-*` oraz obecne repo `PythonPro-Course`.

## Zasady bezpieczenstwa

Przed zmianami utworzono lokalne punkty powrotu:

```bash
git branch backup/pre-consolidation-20260812
git tag pre-consolidation-20260812
```

Nie wykonano:

```bash
git rebase -i
git filter-branch
git filter-repo
git reset --hard
git push --force
```

Stara historia commitow nie zostala przepisana. Import repozytoriow wykonano przez `git subtree add` bez `--squash`, zeby zachowac osobne commity z poprzednich repo.

## Przygotowanie lesson12

Przed scaleniem byly lokalne zmiany w `lesson12`. Zostaly podzielone na trzy tematyczne commity:

```bash
python -m py_compile lesson12/01.py lesson12/02.py lesson12/03.py lesson12/06.py lesson12/07.py lesson12/08.py lesson12/09.py

git add lesson12/01.py lesson12/02.py lesson12/07.py
git commit -m "feat(lesson12): extend object model exercises"

git add lesson12/03.py lesson12/08.py
git commit -m "refactor(lesson12): simplify calculator exercises"

git add lesson12/06.py lesson12/09.py
git commit -m "feat(lesson12): add custom validation exceptions"
```

## Porzadkowanie struktury

Istniejace lekcje w `PythonPro-Course` przeniesiono do katalogu `lessons/`. Dodano tez `.gitignore` ignorujacy m.in. `.venv/`, `venv/`, `__pycache__/`, cache testow i lokalne pliki edytorow.

Uzyte komendy w uproszczonej postaci:

```bash
mkdir lessons
git mv lesson01 lessons/lesson01
git mv lesson02 lessons/lesson02
git mv lesson03 lessons/lesson03
git mv lesson04 lessons/lesson04
git mv lesson05 lessons/lesson05
git mv lesson06 lessons/lesson06
git mv lesson07 lessons/lesson07
git mv lesson08 lessons/lesson08
git mv lesson09 lessons/lesson09
git mv lesson10 lessons/lesson10
git mv lesson11 lessons/lesson11
git mv lesson12 lessons/lesson12
git mv lesson13 lessons/lesson13
git mv lesson14 lessons/lesson14
git mv lesson16 lessons/lesson16
git mv Lesson21 lessons/lesson21
git add .gitignore
git commit -m "chore: organize course lessons directory"
```

## Import repozytoriow przez subtree

Zaimportowano nastepujace repozytoria lokalne:

| Repo zrodlowe | Branch | Katalog docelowy | Zachowanie historii |
| --- | --- | --- | --- |
| `Lesson 15 project app` | `master` | `lessons/lesson15_project_sql_app` | tak |
| `Lesson 17 app` | `master` | `lessons/lesson17_app` | tak |
| `Lesson 18` | `master` | `lessons/lesson18_app` | tak |
| `Lesson 19` | `master` | `lessons/lesson19` | tak |
| `Lesson 20` | `master` | `lessons/lesson20` | tak |
| `Lesson22` | `master` | `lessons/lesson22` | tak |
| `Lesson 23` | `master` | `lessons/lesson23` | tak |

Komendy:

```bash
git subtree add --prefix=lessons/lesson15_project_sql_app "C:\Users\Tomek\Documents\Developer\Lesson 15 project app" master --message "chore: import lesson 15 project repository"
git subtree add --prefix=lessons/lesson17_app "C:\Users\Tomek\Documents\Developer\Lesson 17 app" master --message "chore: import lesson 17 app repository"
git subtree add --prefix=lessons/lesson18_app "C:\Users\Tomek\Documents\Developer\Lesson 18" master --message "chore: import lesson 18 repository"
git subtree add --prefix=lessons/lesson19 "C:\Users\Tomek\Documents\Developer\Lesson 19" master --message "chore: import lesson 19 repository"
git subtree add --prefix=lessons/lesson20 "C:\Users\Tomek\Documents\Developer\Lesson 20" master --message "chore: import lesson 20 repository"
git subtree add --prefix=lessons/lesson22 "C:\Users\Tomek\Documents\Developer\Lesson22" master --message "chore: import lesson 22 repository"
git subtree add --prefix=lessons/lesson23 "C:\Users\Tomek\Documents\Developer\Lesson 23" master --message "chore: import lesson 23 repository"
```

## Lesson 24

`Lesson 24` nie mial katalogu `.git`, wiec nie bylo historii do zachowania. Pliki zostaly dodane jako nowy katalog:

```text
lessons/lesson24/
```

Pominieto `.venv` oraz usunieto wygenerowany `__pycache__` z kopii.

Commit:

```bash
git add lessons/lesson24
git commit -m "feat(lesson24): add Django lesson materials"
```

## Dlaczego nie zmieniano starych commitow

Zmiana opisow starych commitow albo dzielenie duzych commitow wymaga przepisywania historii. Poniewaz repozytoria sa juz na GitHubie, taka operacja moglaby wymagac `git push --force` i moglaby popsuc synchronizacje lokalnej oraz zdalnej historii.

Bezpieczniejsza alternatywa: zostawic historie tak jak jest, a od teraz pisac lepsze, mniejsze commity. Do nauki mozna przygotowac osobny dokument z propozycjami lepszych nazw dla starych commitow, bez zmieniania repo.

## Wynik

Wszystkie lekcje sa teraz w jednym repo `PythonPro-Course`, pod katalogiem `lessons/`. Historie osobnych repozytoriow zaimportowanych przez subtree pozostaly widoczne jako osobne commity.

## Dodatkowe czyszczenie po weryfikacji

Po imporcie sprawdzono, czy Git sledzi lokalne srodowiska albo cache Pythona:

```bash
git ls-files | Select-String -Pattern '(^|/)(\.venv|venv|__pycache__)(/|$)'
```

Nie znaleziono sledzonych virtualenvow, ale w historii repo `Lesson 15 project app` byly sledzone pliki `__pycache__/*.pyc`. Usunieto je z aktualnego drzewa zwyklym commitem, bez przepisywania starej historii:

```bash
git rm -- <tracked __pycache__ files>
git commit -m "chore: remove tracked Python cache files"
```
