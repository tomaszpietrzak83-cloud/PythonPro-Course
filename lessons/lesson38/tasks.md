# Lesson 38 - Zadania

## TASK 01 - Pierwszy Workflow (proste)

Stwórz plik:

```text
.github/workflows/hello.yml
```

Workflow ma uruchamiać się przy każdym pushu i wyświetlać:

```text
Hello, CI/CD!
```

Oczekiwany rezultat:

- workflow uruchamia się automatycznie,
- w logach widać `Hello, CI/CD!`.

## TASK 02 - Workflow z Pythonem (proste)

Stwórz workflow, który:

- setupuje Python `3.11`,
- tworzy prosty plik Python z funkcją `hello()`,
- uruchamia ten plik.

## TASK 03 - Instalacja Dependencies (proste)

Dodaj do workflow krok instalujący zależności z:

```text
requirements.txt
```

Stwórz `requirements.txt` z pakietami:

- `requests`,
- `pytest`.

## TASK 04 - Pierwszy Test (proste)

Napisz prosty test w pliku:

```text
tests/test_math.py
```

Kod:

```python
def test_addition():
    assert 2 + 2 == 4
```

Dodaj krok w workflow uruchamiający ten test przez:

```bash
pytest
```

## TASK 05 - Cache Dependencies (proste)

Dodaj do workflow cache dla zależności `pip`, aby przyspieszyć instalację.

Wskazówka z materiału:

```yaml
uses: actions/cache@v3
```

<p style="color:red"><strong>Komentarz mentora:</strong> Sprawdź aktualną wersję `actions/cache`, bo wersje akcji GitHub zmieniają się z czasem.</p>

## TASK 06 - Matrix Strategy (proste)

Zmodyfikuj workflow tak, aby uruchamiał testy równocześnie na:

- Python `3.9`,
- Python `3.10`,
- Python `3.11`.

## TASK 07 - Linting (proste)

Dodaj krok uruchamiający:

```bash
flake8
```

dla plików w folderze:

```text
src/
```

Zainstaluj `flake8` w poprzednim kroku workflow.

## TASK 08 - Workflow Trigger (proste)

Stwórz workflow, który uruchamia się:

- na push do brancha `main`,
- na pull request do brancha `main`,
- ręcznie przez `workflow_dispatch`.

## TASK 09 - Multi-Job Workflow (średnie)

Stwórz workflow z trzema jobami:

- `lint` - uruchamia `flake8`,
- `test` - uruchamia `pytest`,
- `build` - buduje aplikację tylko wtedy, gdy `lint` i `test` przejdą.

`build` powinien zależeć od `lint` i `test` przez:

```yaml
needs:
  - lint
  - test
```

## TASK 10 - Artifacts (średnie)

Zmodyfikuj workflow tak, aby zapisywał wyniki testów jako artifact.

Wskazówka z materiału:

```yaml
uses: actions/upload-artifact@v3
```

Oczekiwany rezultat:

- po uruchomieniu workflow w zakładce `Artifacts` widać wyniki testów.

<p style="color:red"><strong>Komentarz mentora:</strong> Przy nowym workflow sprawdź aktualną wersję `actions/upload-artifact`.</p>

## TASK 11 - Environment Variables (średnie)

Stwórz workflow używający zmiennych środowiskowych:

- globalnych zmiennych przez `env:` na poziomie workflow,
- lokalnych zmiennych dla konkretnego joba.

Wyświetl je w kroku:

```yaml
run:
```

## TASK 12 - Conditional Steps (średnie)

Dodaj do workflow krok, który wykonuje się tylko:

- jeśli jesteś na branchu `main`,
- jeśli testy przeszły przez `if: success()`.

Ten krok powinien wyświetlać:

```text
Ready to deploy!
```

## TASK 13 - Full CI/CD Pipeline (challenge)

Stwórz kompletny pipeline CI/CD.

Każdy stage powinien być osobnym jobem z zależnościami.

Stage:

- `Lint` - `flake8`, `black`,
- `Test` - `pytest` z coverage,
- `Build` - Docker image,
- `Deploy` - symulacja przez `echo "Deploying..."`.

## TASK 14 - Docker Build w GitHub Actions (challenge)

Stwórz workflow, który:

- buduje Docker image z aplikacją Python,
- uruchamia testy w kontenerze,
- pushuje image do GitHub Container Registry `ghcr.io`.

Wskazówka z materiału:

```yaml
docker/login-action@v2
docker/build-push-action@v4
```

<p style="color:red"><strong>Komentarz mentora:</strong> W nowych workflow sprawdź aktualne wersje akcji Docker. W projektach produkcyjnych rozważ pinning do SHA.</p>

## TASK 15 - GitLab CI/CD (challenge)

Przepisz jeden workflow z GitHub Actions na GitLab CI/CD.

Stwórz plik:

```text
.gitlab-ci.yml
```

Powinien zawierać:

- 3 stage: `build`, `test`, `deploy`,
- cache dla dependencies,
- artifacts dla wyników testów.

## TASK 16 - Secrets Management (challenge)

Stwórz workflow, który:

- używa secretu, na przykład `API_KEY`,
- wyświetla maskowaną wartość secretu,
- symuluje deploy z użyciem secretu.

Dodaj secret w ustawieniach repozytorium.

## TASK 17 - Scheduled Workflow (challenge)

Stwórz workflow, który uruchamia się codziennie o `3:00 UTC`.

Workflow ma:

- wykonać security scan, na przykład `pip-audit`,
- jeśli znajdzie vulnerabilities, stworzyć GitHub Issue.

Wskazówka z materiału:

```yaml
peter-evans/create-issue-from-file@v4
```

## TASK 18 - Multi-Platform Testing (challenge)

Stwórz workflow testujący aplikację na:

- Ubuntu,
- macOS,
- Windows.

Wersje Pythona:

- `3.9`,
- `3.10`,
- `3.11`.

Użyj matrix z `exclude` dla specyficznych kombinacji.

Oczekiwany rezultat:

- 9 jobów, czyli 3 OS x 3 wersje Pythona.

## TASK 19 - Integration z AWS (challenge)

Stwórz workflow deployujący aplikację do AWS.

Workflow ma:

- konfigurować AWS credentials,
- budować Docker image,
- pushować image do ECR,
- aktualizować ECS service.

Możesz użyć `localstack` do symulacji AWS.

<p style="color:red"><strong>Komentarz mentora:</strong> Do prawdziwego AWS w GitHub Actions preferuj OIDC i `role-to-assume`, zamiast stałych kluczy w secrets.</p>

## TASK 20 - Custom GitHub Action (challenge)

Stwórz własną akcję GitHub.

Folder:

```text
.github/actions/my-action/
```

Plik:

```text
action.yml
```

Funkcja:

- uruchamia testy,
- generuje badge z coverage.

Użyj tej akcji w workflow.

Wskazówka:

- akcja może być composite,
- akcja może być Docker-based.
