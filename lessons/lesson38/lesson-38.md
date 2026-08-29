# Lekcja 38: CI/CD i GitHub Actions

`#lekcja` `#python` `#cicd` `#github-actions` `#devops` `#automation`

W tej lekcji poznajesz podstawy CI/CD, czyli automatyzacji integracji, testowania, budowania i wdrażania aplikacji.

Główne tematy:

- czym jest CI/CD,
- etapy pipeline,
- GitHub Actions,
- workflow, jobs, steps i runners,
- matrix strategy,
- secrets, artifacts i cache,
- deployment do AWS,
- alternatywne narzędzia CI/CD,
- wykorzystanie AI w CI/CD.

## 1. Czym jest CI/CD?

> [!definition]
>
> CI/CD, czyli Continuous Integration / Continuous Deployment, to zestaw praktyk DevOps automatyzujących integrację kodu, testowanie i wdrażanie aplikacji.

CI, czyli Continuous Integration, skupia się na częstym łączeniu zmian w kodzie i automatycznym sprawdzaniu ich testami.

CD może oznaczać:

- Continuous Delivery - kod jest zawsze gotowy do wdrożenia, ale produkcyjny deploy wymaga ręcznej akcji,
- Continuous Deployment - każda zmiana, która przejdzie pipeline, trafia automatycznie na produkcję.

Korzyści:

- szybsze wykrywanie błędów,
- automatyczne testy przy każdej zmianie,
- mniej konfliktów w kodzie,
- szybsze dostarczanie funkcjonalności,
- większa pewność jakości,
- automatyzacja powtarzalnych zadań.

## 2. Tradycyjny proces vs CI/CD

Tradycyjny proces:

```text
Developer pisze kod lokalnie
Ręcznie uruchamia testy
Commituje kod
Inny developer pobiera zmiany
Błędy są wykrywane późno
Ręczny deploy na serwer
```

Proces z CI/CD:

```text
Developer pisze kod lokalnie
Push do repozytorium
Pipeline automatycznie uruchamia testy
Pipeline sprawdza jakość kodu
Pipeline buduje aplikację
Pipeline może wdrożyć aplikację
Developer dostaje szybki feedback
```

## 3. Struktura projektu z CI/CD

Przykładowa struktura:

```text
my-python-project/
    .github/
        workflows/
            test.yml
            deploy.yml
            lint.yml
    src/
        app.py
    tests/
        test_app.py
    requirements.txt
    Dockerfile
    README.md
```

Workflow GitHub Actions trzymamy w:

```text
.github/workflows/
```

## 4. Etapy pipeline

Typowy pipeline ma kilka etapów:

```text
BUILD
TEST
DEPLOY
MONITOR
```

Etap `BUILD`:

- instalacja zależności,
- kompilacja, jeśli jest potrzebna,
- tworzenie artefaktów, na przykład Docker image.

Etap `TEST`:

- unit testy,
- integration testy,
- coverage report,
- linting,
- type checking.

Etap `DEPLOY`:

- deploy do staging,
- smoke tests,
- deploy do produkcji z manual approval albo automatycznie.

Etap `MONITOR`:

- health checks,
- metryki aplikacji,
- alerty.

## 5. Przykład testów lokalnych

Przykładowy test:

```python
def test_addition():
    assert 2 + 2 == 4
```

Przykładowy `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts =
    --verbose
    --cov=src
    --cov-report=html
    --cov-report=term
```

## 6. Pre-commit

Pre-commit hooki pozwalają uruchamiać formatowanie i linting przed commitem.

Przykład:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
        language_version: python3.11
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88]
```

<p style="color:red"><strong>Komentarz mentora:</strong> Wersje narzędzi w przykładzie są zachowane z materiału. W nowym projekcie sprawdź aktualne wersje `black`, `flake8` i innych hooków, a potem przypnij konkretną wersję.</p>

## 7. Best practices CI/CD

Najważniejsze zasady:

- utrzymuj testy szybkie,
- jeden branch powinien mieć jeden przewidywalny pipeline,
- używaj cache dla zależności,
- monitoruj czas wykonania pipeline,
- miej rollback strategy,
- nie wdrażaj bez testów,
- nie zapisuj sekretów w kodzie.

> [!warning]
>
> Częste błędy: zbyt wolne testy, brak testów integracyjnych, deploy bez rollbacku, brak monitoringu po deployu i hardcoded secrets.

## 8. GitHub Actions

> [!definition]
>
> GitHub Actions to platforma CI/CD wbudowana w GitHub. Używa plików YAML do definiowania automatyzacji uruchamianych przez eventy, na przykład `push` albo `pull_request`.

Podstawowe pojęcia:

- `Workflow` - cały proces automatyzacji,
- `Event` - zdarzenie uruchamiające workflow,
- `Job` - zestaw kroków na jednym runnerze,
- `Step` - pojedynczy krok,
- `Action` - reużywalna akcja,
- `Runner` - maszyna wykonująca workflow.

## 9. Pierwszy workflow testowy

Materiał pokazuje workflow uruchamiany przy push i pull request:

```yaml
name: Run Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov flake8
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Lint with flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

      - name: Run tests with pytest
        run: |
          pytest tests/ --cov=src --cov-report=xml --cov-report=term
```

<p style="color:red"><strong>Komentarz mentora:</strong> `actions/checkout@v3`, `actions/setup-python@v4` i `actions/cache@v3` są przykładami z materiału. Aktualne wersje akcji zmieniają się, więc dla nowych workflow sprawdź najnowsze release i rozważ pinning do pełnego SHA w projektach o wysokich wymaganiach bezpieczeństwa.</p>

## 10. Matrix strategy

Matrix pozwala uruchomić ten sam job na wielu konfiguracjach.

Przykład:

```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11"]
```

Możesz też testować różne systemy:

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    python-version: ["3.9", "3.10", "3.11"]
```

`fail-fast: false` sprawia, że pozostałe kombinacje kontynuują pracę, nawet jeśli jedna kombinacja padnie.

## 11. Cache

Cache przyspiesza pipeline, bo nie trzeba za każdym razem pobierać tych samych zależności.

Przykład z materiału:

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

<p style="color:red"><strong>Komentarz mentora:</strong> GitHub przebudowywał backend cache i starsze wersje akcji mogły wymagać aktualizacji. Dla nowego projektu sprawdź aktualną wersję `actions/cache`.</p>

## 12. Deployment do AWS

Materiał pokazuje deployment do AWS:

- checkout kodu,
- konfiguracja AWS credentials,
- login do ECR,
- build Docker image,
- testy w kontenerze,
- push image do ECR,
- aktualizacja ECS task definition,
- deploy do ECS,
- powiadomienie o sukcesie.

Fragment:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  AWS_REGION: eu-west-1
  ECR_REPOSITORY: my-python-app
  ECS_SERVICE: my-service
  ECS_CLUSTER: my-cluster
```

Przykładowa konfiguracja AWS z materiału używa sekretów:

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v2
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: ${{ env.AWS_REGION }}
```

<p style="color:red"><strong>Komentarz mentora:</strong> Dla GitHub Actions i AWS preferuj OIDC oraz `role-to-assume`, zamiast długotrwałych kluczy `AWS_ACCESS_KEY_ID` i `AWS_SECRET_ACCESS_KEY` zapisanych jako secrets.</p>

## 13. Secrets

Secrets w GitHub Actions służą do przechowywania poufnych danych:

- tokenów,
- haseł,
- kluczy API,
- connection stringów,
- webhooków.

Przykład:

```yaml
- name: Deploy to production
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    python deploy.py --db-url "$DATABASE_URL"
```

Różnica:

- `env` - dobre dla danych jawnych,
- `secrets` - dla danych poufnych.

> [!warning]
>
> Nie hardcoduj sekretów w YAML ani w kodzie.

## 14. Artifacts

Artifacts pozwalają przechowywać pliki wygenerowane przez workflow.

Przykłady:

- raporty testów,
- coverage,
- zbudowana dokumentacja,
- paczki release,
- raporty security scan.

Przykład:

```yaml
- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: junit/*.xml
```

<p style="color:red"><strong>Komentarz mentora:</strong> Tak jak przy innych actions, wersja `actions/upload-artifact@v3` pochodzi z materiału. W nowych workflow sprawdź aktualną wersję tej akcji.</p>

## 15. Zaawansowane features

GitHub Actions wspiera:

- `matrix`,
- `secrets`,
- `artifacts`,
- `needs`,
- `if`,
- `schedule`,
- `workflow_dispatch`.

Przykład zależności:

```yaml
publish:
  needs: [test-matrix, security-scan, build-docs]
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
```

Przykład schedule:

```yaml
on:
  schedule:
    - cron: "0 3 * * *"
```

## 16. Limity i koszty

Materiał wspomina limity darmowego planu GitHub Actions, między innymi minuty dla prywatnych repozytoriów i storage dla artifacts.

<p style="color:red"><strong>Komentarz mentora:</strong> Limity i ceny GitHub Actions są zależne od planu i mogą się zmieniać. Przed planowaniem długich pipeline sprawdź aktualną stronę billing/usage w GitHub.</p>

## 17. Alternatywne narzędzia CI/CD

Poza GitHub Actions istnieją:

- GitLab CI/CD,
- CircleCI,
- Jenkins,
- Travis CI,
- Azure DevOps,
- AWS CodePipeline,
- Google Cloud Build.

Wybór zależy od:

- miejsca hostowania kodu,
- wymagań self-hosted,
- budżetu,
- dostawcy chmury,
- wymagań enterprise,
- integracji z Dockerem i Kubernetes.

## 18. GitLab CI/CD

GitLab CI/CD używa pliku:

```text
.gitlab-ci.yml
```

Przykładowe etapy:

```yaml
stages:
  - build
  - test
  - deploy
```

Zalety:

- wbudowane w GitLab,
- self-hosted runners,
- wbudowany Docker registry,
- environments,
- dobra integracja z Kubernetes.

## 19. CircleCI

CircleCI używa pliku:

```text
.circleci/config.yml
```

W materiale pojawiają się:

- `orbs`,
- executors,
- cache,
- test results,
- artifacts,
- deployment do AWS.

Zalety:

- szybkie buildy,
- reusable orbs,
- dobra integracja z Dockerem,
- resource classes,
- insights.

## 20. Jenkins

Jenkins używa zwykle pliku:

```text
Jenkinsfile
```

Pipeline jest definiowany w Groovy DSL.

Zalety:

- open-source,
- self-hosted,
- pełna kontrola,
- tysiące pluginów,
- częsty wybór w enterprise.

Wady:

- wymaga utrzymania serwera,
- konfiguracja bywa złożona,
- starsza architektura,
- trzeba dbać o pluginy i bezpieczeństwo.

## 21. Jak wybrać narzędzie CI/CD?

Prosta zasada z materiału:

- kod na GitHub - GitHub Actions,
- kod na GitLab - GitLab CI/CD,
- potrzeba self-hosted - Jenkins albo GitLab,
- aplikacja mocno związana z AWS - CodePipeline,
- aplikacja mocno związana z Azure - Azure DevOps,
- performance-critical pipelines - CircleCI.

> [!note]
>
> Zacznij prosto. Dla większości małych projektów Python na GitHub wystarczy GitHub Actions.

## 22. AI w CI/CD

AI może pomagać w:

- generowaniu testów,
- analizie logów CI/CD,
- sugerowaniu optymalizacji pipeline,
- podsumowywaniu błędów,
- tworzeniu checklist.

Przykład funkcji z materiału:

```python
def calculate_discount(price, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

AI może wygenerować testy:

```python
import pytest


def test_calculate_discount():
    assert calculate_discount(100, 10) == 90
    assert calculate_discount(100, 0) == 100
    assert calculate_discount(100, 100) == 0

    with pytest.raises(ValueError):
        calculate_discount(100, -5)

    with pytest.raises(ValueError):
        calculate_discount(100, 150)
```

Materiał pokazuje też analizę logów przez starszy styl OpenAI:

```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
)
```

<p style="color:red"><strong>Komentarz mentora:</strong> `openai.ChatCompletion.create` to starszy styl SDK. Przy nowych projektach sprawdź aktualny klient OpenAI. Nie wysyłaj do AI logów zawierających sekrety, tokeny, dane osobowe albo prywatne adresy.</p>

## 23. Podsumowanie

W tej lekcji najważniejsze są:

- CI/CD jako automatyzacja testowania i wdrażania,
- różnica między Continuous Delivery i Continuous Deployment,
- GitHub Actions jako narzędzie CI/CD,
- workflow, events, jobs, steps i runners,
- testy, linting i coverage,
- matrix strategy,
- cache i artifacts,
- secrets,
- deployment do AWS,
- alternatywne narzędzia CI/CD,
- AI jako wsparcie przy testach i analizie błędów.

Materiał kończy się połączeniem z wcześniejszymi tematami: Git, testing, Docker, AWS i web frameworks.

<p style="color:red"><strong>Komentarz mentora:</strong> PDF odwołuje się do Dockera jako „Lekcja 46” i AWS jako „Lekcje 43-44”. W tym katalogu wygląda to na niespójną numerację względem aktualnych plików lekcji.</p>
