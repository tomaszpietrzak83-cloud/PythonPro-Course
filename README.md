# PythonPro-Course

Repozytorium z cwiczeniami z kursu Python Pro. To jest robocze repo do nauki Pythona, Django, SQL, pracy z plikami, testowania i uzywania Gita.

## Struktura

```text
PythonPro-Course/
  lessons/              # lekcje i projekty lekcyjne
  README.md             # opis repozytorium
  MERGE_REPORT.md       # dokumentacja scalenia repozytoriow
  LEARNING_JOURNAL.md   # dziennik nauki z historii commitow
  .gitignore            # ignorowane pliki lokalne, cache i venv
```

Aktualne katalogi lekcji:

```text
lessons/lesson01
lessons/lesson02
lessons/lesson03
lessons/lesson04
lessons/lesson05
lessons/lesson06
lessons/lesson07
lessons/lesson08
lessons/lesson09
lessons/lesson10
lessons/lesson11
lessons/lesson12
lessons/lesson13
lessons/lesson14
lessons/lesson15_project_sql_app
lessons/lesson16
lessons/lesson17_app
lessons/lesson18_app
lessons/lesson19
lessons/lesson20
lessons/lesson21
lessons/lesson22
lessons/lesson23
lessons/lesson24
```

## Praca z virtualenv

Virtualenv jest lokalny i nie powinien trafic do repozytorium.

Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
```

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Instalowanie pakietow najlepiej robic przez:

```bash
python -m pip install nazwa_pakietu
```

## Zasady commitow

Preferowane sa male commity z opisem celu zmiany, np.:

```text
feat(lesson12): add custom validation exceptions
refactor(lesson12): simplify calculator exercises
chore: organize course lessons directory
```

Nie przepisujemy starej historii repozytorium bez waznego powodu. Dla repo publicznego zmiana starych commitow zwykle wymaga `force push`, wiec jest ryzykowna.

## Dokumentacja

- `MERGE_REPORT.md` opisuje, jak osobne repozytoria lekcyjne zostaly scalone do tego repo.
- `LEARNING_JOURNAL.md` podsumowuje postep nauki na podstawie historii commitow.
