# Lesson 35 - Zadania

## TASK 01 - Health Check Script (proste)

Napisz skrypt Python, który sprawdza dostępność 3 dowolnych stron internetowych.

Użyj:

```python
requests
```

Skrypt powinien wyświetlić:

- czy strona odpowiada statusem `200 OK`,
- czas odpowiedzi.

## TASK 02 - Backup Script (proste)

Stwórz skrypt, który tworzy kopię zapasową katalogu.

Skrypt powinien:

- kopiować katalog do folderu `backups/`,
- dodawać datę i czas do nazwy, na przykład `backup_20240615_143022`,
- wyświetlać informację o sukcesie.

Użyj:

```python
shutil
datetime
```

## TASK 03 - AWS Region Lister (proste)

Użyj `boto3`, aby wylistować wszystkie regiony AWS dla usługi EC2.

Wyświetl:

- nazwę regionu,
- endpoint.

<p style="color:red"><strong>Komentarz mentora:</strong> To zadanie wymaga skonfigurowanych uprawnień AWS. Nie zapisuj kluczy dostępowych w kodzie.</p>

## TASK 04 - S3 Bucket Creator (proste)

Napisz funkcję:

```python
create_s3_bucket(bucket_name, region)
```

Funkcja ma:

- tworzyć nowy bucket S3,
- obsługiwać błąd, gdy bucket już istnieje.

## TASK 05 - File Upload to S3 (proste)

Stwórz skrypt, który uploaduje wszystkie pliki `.jpg` z danego katalogu do bucketa S3.

Użyj:

```python
Path
```

z modułu `pathlib` do iteracji po plikach.

## TASK 06 - EC2 Instance Lister (proste)

Napisz funkcję, która listuje wszystkie instancje EC2.

Wyświetl:

- ID,
- typ instancji,
- stan, na przykład `running` albo `stopped`,
- publiczny IP, jeśli istnieje.

## TASK 07 - Log Parser (proste)

Napisz funkcję, która parsuje plik z logami i zlicza, ile razy wystąpił każdy poziom logu:

- `ERROR`,
- `WARNING`,
- `INFO`.

Zwróć wynik jako słownik.

Przykładowy log:

```text
[2024-06-15 10:30] ERROR: Connection failed
[2024-06-15 10:31] INFO: Retrying...
[2024-06-15 10:32] ERROR: Max retries exceeded
```

## TASK 08 - Environment Variables Reader (proste)

Stwórz skrypt, który odczytuje zmienne środowiskowe AWS:

- `AWS_ACCESS_KEY_ID`,
- `AWS_SECRET_ACCESS_KEY`,
- `AWS_DEFAULT_REGION`.

Jeśli którejś brakuje, wyświetl ostrzeżenie.

Użyj:

```python
os.environ
```

## TASK 09 - Auto-Stop EC2 Scheduler (średnie)

Napisz skrypt, który:

- listuje wszystkie działające instancje EC2,
- sprawdza tag `AutoStop` z wartością `true` albo `false`,
- zatrzymuje instancje z `AutoStop=true`,
- loguje wszystkie akcje.

To symulacja schedulera, który oszczędza koszty przez zatrzymywanie instancji developerskich wieczorem.

<p style="color:red"><strong>Komentarz mentora:</strong> Najpierw zrób wersję w trybie `dry_run`, która tylko wypisuje planowane akcje. Dopiero potem pozwól skryptowi zatrzymywać prawdziwe instancje.</p>

## TASK 10 - S3 Backup with Rotation (średnie)

Rozszerz zadanie 2.

Zamiast kopiować backup lokalnie:

- uploaduj backup na S3,
- zaimplementuj rotację,
- usuń backupy starsze niż 7 dni,
- sprawdź `LastModified` w S3.

## TASK 11 - Multi-Region S3 Sync (średnie)

Stwórz funkcję, która kopiuje wszystkie obiekty z jednego bucketa S3 do drugiego bucketa w innym regionie.

Użyj:

```python
copy_object
```

z `boto3`.

To symulacja backupu disaster recovery.

## TASK 12 - Resource Cost Calculator (średnie)

Napisz klasę:

```python
AWSCostCalculator
```

Klasa ma:

- pobierać listę instancji EC2,
- na podstawie typu instancji i czasu działania szacować koszty,
- używać uproszczonego cennika, na przykład `t3.micro = $0.01/h`,
- zwracać raport kosztów.

## TASK 13 - Complete Deployment Pipeline (challenge)

Zbuduj kompletny skrypt deployment pipeline.

Skrypt ma:

- klonować albo aktualizować repozytorium Git,
- uruchamiać testy przez `pytest`,
- jeśli testy przechodzą, budować Docker image,
- pushować image do ECR,
- deployować aplikację na EC2 przez SSH,
- wykonać health check,
- jeśli health check nie przejdzie, wykonać rollback.

## TASK 14 - S3 Static Website Deployer (challenge)

Stwórz narzędzie CLI.

Użyj:

```python
argparse
```

Narzędzie ma:

- tworzyć bucket S3 z konfiguracją static website,
- uploadować wszystkie pliki HTML/CSS/JS,
- ustawiać poprawny `Content-Type`,
- konfigurować bucket policy dla publicznego dostępu,
- wyświetlać URL strony.

<p style="color:red"><strong>Komentarz mentora:</strong> Publiczny hosting na S3 wymaga świadomej konfiguracji dostępu. Nowe buckety mają mocne zabezpieczenia przed publicznym dostępem, więc nie obchodź ich przypadkowo.</p>

## TASK 15 - Infrastructure Monitor (challenge)

Zbuduj system monitoringu, który co 5 minut:

- sprawdza stan wszystkich instancji EC2,
- sprawdza wykorzystanie dysków EBS,
- testuje dostępność aplikacji przez HTTP health checks,
- zapisuje metryki do pliku CSV,
- wysyła alert, jeśli wykryje problem.

Użyj:

```python
schedule
```

albo:

```python
asyncio
```

## TASK 16 - Auto-Scaling Simulator (challenge)

Zasymuluj auto-scaling.

Wymagania:

- funkcja `simulate_load()` zwraca losowe obciążenie CPU od 20% do 90%,
- jeśli obciążenie jest większe niż 70% przez 3 pomiary, program "uruchamia" nową instancję przez `print`,
- jeśli obciążenie jest mniejsze niż 30% przez 3 pomiary, program "zatrzymuje" instancję,
- zapisuje historię akcji,
- działa przez 20 iteracji.

To uproszczona wersja mechanizmu AWS Auto Scaling Groups.

## TASK 17 - S3 Event Processor (challenge)

Stwórz system, który:

- monitoruje bucket S3 przez listowanie nowych obiektów,
- po wykryciu nowego obrazu `.jpg` albo `.png` pobiera go,
- tworzy thumbnail,
- uploaduje thumbnail do folderu `thumbnails/` w tym samym buckecie.

Użyj:

```python
Pillow
```

To symulacja S3 Event + Lambda function.

## TASK 18 - Multi-Environment Config Manager (challenge)

Zbuduj system zarządzania konfiguracją dla wielu środowisk.

Klasa `ConfigManager` ma:

- przechowywać konfiguracje w JSON,
- wspierać środowiska `dev`, `staging`, `production`,
- przechowywać dla każdego środowiska `region`, `instance_type`, `db_size`,
- mieć metodę `deploy(environment)`, która wyświetla, jakie zasoby należy utworzyć,
- mieć metodę `compare(env1, env2)`, która pokazuje różnice między środowiskami.

## TASK 19 - Disaster Recovery Orchestrator (challenge)

Zaprojektuj system disaster recovery.

Wymagania:

- funkcja `create_snapshot()` symuluje snapshot EC2 i RDS oraz zapisuje metadane do JSON,
- funkcja `store_backup_s3()` symuluje upload backupu do S3 w innym regionie,
- funkcja `restore_from_backup(snapshot_id)` symuluje odtworzenie z backupu,
- funkcja `test_recovery()` testuje cały proces,
- pełna historia operacji jest zapisywana do logów.

## TASK 20 - Cloud Cost Optimizer (challenge)

Stwórz narzędzie do optymalizacji kosztów.

Użyj danych symulowanych jako słowników.

Narzędzie ma:

- analizować listę instancji EC2 i ich czas działania,
- wykrywać instancje działające 24/7 z niskim użyciem,
- sugerować migrację do Reserved Instances i wyliczać oszczędności,
- wykrywać zatrzymane instancje z podpiętymi wolumenami,
- generować raport rekomendacji w formacie Markdown.
