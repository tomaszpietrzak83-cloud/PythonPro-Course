# Lekcja 35: DevOps i AWS - Podstawy Wdrażania Aplikacji

`#lekcja` `#python` `#devops` `#aws` `#ec2` `#s3` `#deployment`

W tej lekcji poznasz podstawy DevOps i chmury obliczeniowej AWS.

Najważniejsze tematy:

- rola inżyniera DevOps,
- automatyzacja deploymentu,
- monitoring i health checki,
- backupy,
- podstawy AWS,
- EC2,
- S3,
- użycie `boto3`,
- wykorzystanie AI w DevOps.

## 1. Rola inżyniera DevOps

DevOps powstał jako odpowiedź na tradycyjny model pracy, w którym programiści tworzyli kod, a administratorzy systemów osobno zajmowali się wdrożeniem.

Ten podział często prowadził do opóźnień, konfliktów i ręcznych, trudnych do powtórzenia procesów.

> [!definition]
>
> DevOps to kultura i zestaw praktyk łączących development, czyli tworzenie oprogramowania, oraz operations, czyli zarządzanie infrastrukturą.

Inżynier DevOps:

- automatyzuje buildowanie, testowanie i wdrażanie,
- zarządza infrastrukturą przy użyciu kodu,
- monitoruje wydajność i dostępność aplikacji,
- skaluje aplikacje zależnie od obciążenia,
- dba o bezpieczeństwo infrastruktury i aplikacji.

## 2. Prosty deployment aplikacji Python

Materiał pokazuje przykładowy skrypt deploymentu aplikacji Django lub Flask:

```python
import subprocess
import sys


def deploy_app(app_name: str, branch: str = "main"):
    """
    Automatyczny deployment aplikacji Python na serwer.
    """
    print(f"Rozpoczynam deployment {app_name} z branch {branch}...")

    subprocess.run(["git", "fetch", "origin"], check=True)
    subprocess.run(["git", "checkout", branch], check=True)
    subprocess.run(["git", "pull", "origin", branch], check=True)

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        check=True,
    )

    subprocess.run(["python", "manage.py", "migrate"], check=True)
    subprocess.run(["python", "manage.py", "collectstatic", "--noinput"], check=True)
    subprocess.run(["sudo", "systemctl", "restart", f"{app_name}.service"], check=True)

    print(f"Deployment {app_name} zakończony pomyślnie!")
```

Taki skrypt automatyzuje powtarzalne kroki:

- pobranie kodu z Git,
- instalację zależności,
- migracje bazy danych,
- zebranie plików statycznych,
- restart aplikacji.

<p style="color:red"><strong>Komentarz mentora:</strong> To jest uproszczony przykład. W realnym projekcie przed restartem produkcji powinny być testy, backup, strategia rollbacku i środowisko staging.</p>

## 3. Health check

Health check sprawdza, czy aplikacja odpowiada poprawnie.

Przykład:

```python
import time
from typing import Dict, List

import requests


def check_service_health(services: List[Dict[str, str]]) -> None:
    print("Sprawdzam stan serwisów...\n")

    for service in services:
        name = service["name"]
        url = service["url"]

        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            elapsed = time.time() - start_time

            if response.status_code == 200:
                print(f"{name}: OK ({elapsed:.2f}s)")
            else:
                print(f"{name}: Status {response.status_code} ({elapsed:.2f}s)")

        except requests.exceptions.Timeout:
            print(f"{name}: TIMEOUT")
        except requests.exceptions.ConnectionError:
            print(f"{name}: CONNECTION ERROR")
```

Regularne health checki pozwalają szybko wykrywać problemy z dostępnością serwisów.

## 4. Backup z rotacją

Materiał pokazuje przykład backupu bazy PostgreSQL przez `pg_dump` i usuwania starych kopii.

Główne kroki:

- utworzenie katalogu backupów,
- wygenerowanie nazwy pliku z datą i godziną,
- wykonanie `pg_dump`,
- kompresja przez `gzip`,
- usunięcie backupów starszych niż ustalony limit.

```python
from datetime import datetime, timedelta
from pathlib import Path
import os
import subprocess


def backup_database(db_name: str, backup_dir: str, retention_days: int = 7):
    Path(backup_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.sql")

    with open(backup_file, "w") as file:
        subprocess.run(["pg_dump", "-U", "postgres", db_name], stdout=file, check=True)

    subprocess.run(["gzip", backup_file], check=True)

    cutoff_date = datetime.now() - timedelta(days=retention_days)
    for file in Path(backup_dir).glob(f"{db_name}_backup_*.sql.gz"):
        if file.stat().st_mtime < cutoff_date.timestamp():
            file.unlink()
```

<p style="color:red"><strong>Komentarz mentora:</strong> Backup jest użyteczny dopiero wtedy, gdy umiesz go odtworzyć. Do ćwiczenia dodaj później test restore, nawet jeśli materiał pokazuje tylko tworzenie kopii.</p>

## 5. Schemat pracy DevOps

Typowy cykl CI/CD:

```text
Developer pisze kod
Git push
Pipeline CI/CD
Automatyczne testy
Build aplikacji lub obrazu Docker
Deploy na staging
Testy manualne lub automatyczne
Akceptacja
Deploy na produkcję
Monitoring i logi
Rollback albo poprawka w razie problemów
```

Najlepsze praktyki:

- automatyzuj testy, deploymenty i backupy,
- traktuj infrastrukturę jako kod,
- monitoruj kluczowe metryki,
- używaj konteneryzacji dla spójności środowisk,
- miej plan rollbacku.

> [!warning]
>
> Częsty błąd: wdrażanie bezpośrednio na produkcję bez testowania na środowisku staging.

## 6. Wprowadzenie do AWS

AWS, czyli Amazon Web Services, to platforma chmurowa oferująca wiele usług infrastrukturalnych.

Zamiast kupować fizyczne serwery, wynajmujesz zasoby w chmurze i płacisz za użycie.

> [!definition]
>
> AWS działa w modelu pay-as-you-go: płacisz za faktycznie użyte zasoby.

Główne korzyści:

- skalowalność,
- globalna infrastruktura,
- niezawodność,
- mechanizmy bezpieczeństwa,
- kontrola kosztów.

Kluczowe usługi:

- `EC2` - serwery wirtualne,
- `S3` - przechowywanie plików,
- `RDS` - zarządzane bazy danych,
- `Lambda` - funkcje serverless,
- `CloudWatch` - monitoring,
- `IAM` - zarządzanie dostępem.

<p style="color:red"><strong>Komentarz mentora:</strong> Materiał wspomina Free Tier jako 12 miesięcy z przykładami limitów. AWS zmieniał zasady Free Tier zależnie od daty utworzenia konta, więc przed uruchamianiem zasobów zawsze sprawdzaj aktualny panel Billing i dokumentację AWS.</p>

## 7. boto3

`boto3` to oficjalna biblioteka AWS SDK dla Pythona.

Przykład podstawowej klasy:

```python
import boto3


class AWSManager:
    def __init__(self, region_name: str = "eu-central-1"):
        self.region = region_name
        self.session = boto3.Session(region_name=region_name)

    def get_ec2_client(self):
        return self.session.client("ec2")

    def get_s3_client(self):
        return self.session.client("s3")

    def get_rds_client(self):
        return self.session.client("rds")

    def list_all_regions(self):
        ec2 = self.get_ec2_client()
        response = ec2.describe_regions()

        for region in response["Regions"]:
            print(region["RegionName"], region["Endpoint"])
```

Konfiguracja zwykle korzysta z:

- `aws configure`,
- zmiennych środowiskowych,
- roli IAM,
- profili AWS CLI.

<p style="color:red"><strong>Komentarz mentora:</strong> Nie zapisuj kluczy AWS w kodzie ani w repozytorium. Do lokalnych ćwiczeń używaj profili AWS CLI lub zmiennych środowiskowych, a na serwerach ról IAM.</p>

## 8. Koszty i tagi AWS

Materiał pokazuje pobieranie kosztów przez Cost Explorer:

```python
import boto3


client = boto3.client("ce", region_name="us-east-1")
```

Koszty można grupować na przykład po usługach.

Materiał pokazuje też tagowanie zasobów:

```python
tags_to_add = {
    "Environment": "Production",
    "Project": "MyApp",
    "Owner": "DevOps Team",
    "CostCenter": "Engineering",
}
```

Tagi pomagają:

- organizować zasoby,
- szukać zasobów po projekcie lub środowisku,
- analizować koszty,
- automatyzować akcje, na przykład zatrzymywanie środowisk testowych.

## 9. Typowa architektura aplikacji w AWS

Materiał pokazuje architekturę:

```text
Users
Route 53
CloudFront
Load Balancer
EC2 instances
RDS PostgreSQL
S3 bucket
ElastiCache Redis
CloudWatch
```

Taka architektura daje:

- wysoką dostępność,
- skalowalność,
- osobne warstwy aplikacji,
- monitoring,
- przechowywanie plików poza serwerem aplikacji.

## 10. EC2

> [!definition]
>
> EC2 to usługa serwerów wirtualnych w AWS. Pozwala uruchamiać instancje z wybranym systemem operacyjnym, CPU, RAM i storage.

Najważniejsze pojęcia:

- typ instancji, na przykład `t3.micro`,
- system operacyjny,
- region,
- EBS volume,
- Security Group,
- klucz SSH `.pem`.

Rodzaje instancji:

- `T-series` - ogólnego przeznaczenia, tanie,
- `M-series` - zbalansowane CPU/RAM,
- `C-series` - pod obliczenia CPU,
- `R-series` - pod pamięć RAM,
- `P/G-series` - GPU dla ML/AI.

## 11. Tworzenie instancji EC2 przez boto3

Materiał pokazuje funkcję tworzącą instancję EC2:

```python
import boto3


def create_ec2_instance(
    instance_name: str,
    instance_type: str = "t3.micro",
    ami_id: str = "ami-0c55b159cbfafe1f0",
    key_name: str = "my-key-pair",
    security_group_ids: list[str] | None = None,
) -> dict:
    ec2 = boto3.resource("ec2")

    instance_params = {
        "ImageId": ami_id,
        "InstanceType": instance_type,
        "KeyName": key_name,
        "MinCount": 1,
        "MaxCount": 1,
        "TagSpecifications": [
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": instance_name},
                    {"Key": "ManagedBy", "Value": "Python-Boto3"},
                    {"Key": "Environment", "Value": "Development"},
                ],
            }
        ],
    }

    if security_group_ids:
        instance_params["SecurityGroupIds"] = security_group_ids

    instances = ec2.create_instances(**instance_params)
    instance = instances[0]
    instance.wait_until_running()
    instance.reload()

    return {
        "instance_id": instance.id,
        "instance_type": instance.instance_type,
        "state": instance.state["Name"],
        "public_ip": instance.public_ip_address,
    }
```

<p style="color:red"><strong>Komentarz mentora:</strong> ID AMI z materiału jest przykładowe. AMI zależy od regionu i czasu, więc przed uruchomieniem instancji trzeba znaleźć aktualne ID obrazu w wybranym regionie.</p>

## 12. Zarządzanie instancjami EC2

Materiał pokazuje klasę `EC2Manager`, która potrafi:

- listować instancje,
- uruchamiać instancje,
- zatrzymywać instancje,
- usuwać instancje.

Przykładowe operacje:

```python
manager = EC2Manager()

manager.list_instances()
# manager.start_instances(["i-1234567890abcdef0"])
# manager.stop_instances(["i-1234567890abcdef0"])
# manager.terminate_instances(["i-1234567890abcdef0"], confirm=True)
```

Cykl życia instancji:

```text
pending -> running -> stopping -> stopped
running -> terminated
stopped -> terminated
```

> [!warning]
>
> `terminated` oznacza usunięcie instancji. Ta operacja jest nieodwracalna.

<p style="color:red"><strong>Komentarz mentora:</strong> Skrypty boto3 mogą naprawdę tworzyć, zatrzymywać i usuwać zasoby AWS. Do ćwiczeń najpierw używaj danych testowych albo konta szkoleniowego z budżetem i alertami.</p>

## 13. Deployment Django na EC2 przez SSH

Materiał pokazuje deployment przez `paramiko`.

Główne kroki:

- połączenie SSH z instancją,
- aktualizacja systemu,
- instalacja Pythona, pip i Git,
- pobranie repozytorium,
- utworzenie virtualenv,
- instalacja zależności,
- migracje,
- `collectstatic`,
- instalacja `gunicorn`,
- dalsza konfiguracja `systemd`, `nginx` i SSL.

Przykład użycia:

```python
deployer = EC2Deployer(
    host="54.123.45.67",
    username="ec2-user",
    key_filename="/path/to/my-key.pem",
)

deployer.connect()
deployer.deploy_django_app(
    repo_url="https://github.com/username/myapp.git",
    app_name="myapp",
)
deployer.disconnect()
```

> [!warning]
>
> Nigdy nie udostępniaj publicznie klucza `.pem`. Ten plik daje dostęp do serwera.

## 14. S3

> [!definition]
>
> S3 to usługa object storage w AWS. Dane są przechowywane w bucketach jako obiekty.

S3 jest używane do:

- plików statycznych,
- uploadów użytkowników,
- backupów,
- logów,
- data lake,
- hostingu statycznych stron.

Najważniejsze pojęcia:

- `bucket` - kontener na obiekty, nazwa jest globalnie unikalna,
- `object` - plik razem z metadanymi,
- `key` - ścieżka/nazwa obiektu,
- `storage class` - sposób przechowywania i naliczania kosztów,
- `versioning` - wiele wersji tego samego pliku.

Storage classes:

- `S3 Standard`,
- `S3 Intelligent-Tiering`,
- `S3 Standard-IA`,
- `S3 Glacier`,
- `S3 Glacier Deep Archive`.

## 15. Podstawowe operacje na S3

Materiał pokazuje klasę `S3Manager`.

Najważniejsze metody:

- `create_bucket`,
- `upload_file`,
- `download_file`,
- `list_objects`,
- `delete_object`.

Przykład użycia:

```python
s3 = S3Manager()

# s3.create_bucket("my-unique-bucket-name-12345")
# s3.upload_file("logo.png", "my-unique-bucket-name-12345", public=True)
# s3.list_objects("my-unique-bucket-name-12345")
# s3.download_file("my-unique-bucket-name-12345", "logo.png", "downloaded_logo.png")
# s3.delete_object("my-unique-bucket-name-12345", "logo.png")
```

<p style="color:red"><strong>Komentarz mentora:</strong> Materiał pokazuje `ACL = "public-read"` dla publicznego pliku. W nowych bucketach S3 ACL są domyślnie wyłączone, a dostęp najlepiej kontrolować przez bucket policy, IAM, CloudFront albo presigned URLs.</p>

## 16. Django i S3

Materiał pokazuje konfigurację `django-storages`:

```python
INSTALLED_APPS = [
    # ...
    "storages",
]

AWS_STORAGE_BUCKET_NAME = "my-django-app-media"
AWS_S3_REGION_NAME = "eu-central-1"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
```

Po takiej konfiguracji pliki z `ImageField` albo `FileField` mogą trafiać do S3.

<p style="color:red"><strong>Komentarz mentora:</strong> `DEFAULT_FILE_STORAGE` jest starym stylem konfiguracji. Od Django 4.2 preferowany jest słownik `STORAGES`, na przykład konfiguracja pod kluczem `"default"`.</p>

## 17. Presigned URLs

Presigned URL to tymczasowy link pozwalający pobrać albo wysłać prywatny plik bez otwierania całego bucketa publicznie.

Przykład pobierania:

```python
url = s3_client.generate_presigned_url(
    "get_object",
    Params={
        "Bucket": bucket_name,
        "Key": object_name,
    },
    ExpiresIn=3600,
)
```

Przykład uploadu:

```python
response = s3_client.generate_presigned_post(
    Bucket=bucket_name,
    Key=object_name,
    Fields={"Content-Type": "image/jpeg"},
    Conditions=[
        {"Content-Type": "image/jpeg"},
        ["content-length-range", 1, 10485760],
    ],
    ExpiresIn=300,
)
```

To dobry sposób na:

- prywatne pliki użytkowników,
- materiały kursu,
- upload dużych plików bezpośrednio z frontendu do S3.

## 18. Lifecycle S3

Lifecycle policies automatycznie przenoszą dane między klasami przechowywania.

Przykład:

```text
S3 Standard
po 30 dniach -> S3 Standard-IA
po 90 dniach -> S3 Glacier
```

Najlepsze praktyki S3:

- używaj lifecycle policies,
- włącz versioning dla krytycznych danych,
- używaj bucket policies zamiast ACL,
- włącz encryption at rest,
- monitoruj koszty,
- używaj CloudFront dla często pobieranych plików.

> [!warning]
>
> Publiczne buckety to częsty problem bezpieczeństwa. Domyślnie nowe buckety powinny zostać prywatne.

## 19. AI w DevOps i Cloud

AI może pomagać w:

- analizie logów,
- znajdowaniu przyczyn błędów,
- generowaniu konfiguracji Infrastructure as Code,
- tworzeniu checklist deploymentu,
- analizie kosztów.

Materiał pokazuje przykład analizy logów:

```python
def analyze_logs_with_ai(error_logs: list[str]) -> str:
    logs_text = "\n".join(error_logs[-50:])

    prompt = f"""Jesteś ekspertem DevOps. Przeanalizuj logi:
{logs_text}
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Jesteś ekspertem DevOps i debugowania."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content
```

AI może też generować szkic Terraform na podstawie opisu wymagań.

<p style="color:red"><strong>Komentarz mentora:</strong> Nie wysyłaj do modelu AI surowych logów z sekretami, tokenami, danymi osobowymi albo prywatnymi adresami. Najpierw anonimizuj dane.</p>

## 20. Podsumowanie

W tej lekcji najważniejsze są:

- DevOps jako połączenie development i operations,
- automatyzacja CI/CD,
- deployment aplikacji Python,
- health checki i backupy,
- podstawy AWS,
- EC2 jako serwery wirtualne,
- S3 jako object storage,
- `boto3` jako SDK AWS dla Pythona,
- zarządzanie kosztami,
- bezpieczeństwo kluczy i uprawnień,
- użycie AI jako wsparcia w DevOps.

Materiał kończy się zdaniem: `Gratulacje! Ukończyłeś Lekcję 43!`

<p style="color:red"><strong>Komentarz mentora:</strong> To wygląda na literówkę w PDF-ie. Ten plik dotyczy lekcji 35.</p>
