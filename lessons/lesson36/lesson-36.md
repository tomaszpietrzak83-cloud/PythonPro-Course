# Lekcja 36: AWS - RDS, Load Balancing i Deployment

`#lekcja` `#python` `#aws` `#cloud` `#rds` `#elb` `#route53` `#devops`

W tej lekcji zagłębiamy się w usługi AWS potrzebne do budowy skalowalnych i bardziej niezawodnych aplikacji.

Główne tematy:

- RDS,
- Read Replicas,
- ELB i ALB,
- Route53,
- AWS CLI,
- deployment aplikacji Python w AWS,
- Auto Scaling,
- CI/CD z GitHub Actions,
- monitoring i disaster recovery.

## 1. RDS

> [!definition]
>
> RDS, czyli Relational Database Service, to zarządzana usługa baz danych relacyjnych w AWS.

RDS automatyzuje część pracy administracyjnej:

- backupy,
- snapshoty,
- patching,
- monitoring,
- replikację,
- high availability.

Obsługiwane silniki obejmują między innymi:

- PostgreSQL,
- MySQL,
- MariaDB,
- Oracle,
- SQL Server,
- Amazon Aurora.

## 2. Tworzenie instancji RDS

Materiał pokazuje tworzenie instancji PostgreSQL przez `boto3`:

```python
import boto3

rds_client = boto3.client("rds", region_name="eu-central-1")

response = rds_client.create_db_instance(
    DBInstanceIdentifier="myapp-postgres-db",
    DBInstanceClass="db.t3.micro",
    Engine="postgres",
    EngineVersion="15.3",
    MasterUsername="admin",
    MasterUserPassword="SuperSecretPass123!",
    AllocatedStorage=20,
    StorageType="gp3",
    PubliclyAccessible=False,
    BackupRetentionPeriod=7,
    MultiAZ=False,
    VpcSecurityGroupIds=["sg-0123456789abcdef0"],
    Tags=[
        {"Key": "Environment", "Value": "Development"},
        {"Key": "Project", "Value": "MyApp"},
    ],
)
```

`PubliclyAccessible=False` oznacza, że baza nie jest wystawiona publicznie do internetu.

<p style="color:red"><strong>Komentarz mentora:</strong> Hasło w przykładzie jest zapisane w kodzie tylko edukacyjnie. W realnym projekcie użyj AWS Secrets Manager, zmiennych środowiskowych albo mechanizmu IAM. Przed użyciem sprawdź też aktualnie wspierane wersje PostgreSQL w RDS dla wybranego regionu.</p>

## 3. Endpoint RDS i połączenie z bazą

Po utworzeniu bazy trzeba poczekać, aż będzie dostępna.

Materiał pokazuje użycie waitera `boto3`:

```python
def get_rds_endpoint(db_identifier):
    rds_client = boto3.client("rds", region_name="eu-central-1")

    waiter = rds_client.get_waiter("db_instance_available")
    waiter.wait(DBInstanceIdentifier=db_identifier)

    response = rds_client.describe_db_instances(
        DBInstanceIdentifier=db_identifier,
    )

    db_instance = response["DBInstances"][0]
    endpoint = db_instance["Endpoint"]["Address"]
    port = db_instance["Endpoint"]["Port"]

    return endpoint, port
```

Następnie aplikacja może połączyć się z PostgreSQL, na przykład przez `psycopg2`.

## 4. Read Replica

Read Replica służy do skalowania odczytu.

Zasada:

- zapisy idą do głównej bazy,
- odczyty mogą iść do repliki,
- replikacja jest asynchroniczna,
- może pojawić się niewielkie opóźnienie danych.

Przykład:

```python
def create_read_replica(source_db_identifier, replica_identifier):
    rds_client = boto3.client("rds", region_name="eu-central-1")

    response = rds_client.create_db_instance_read_replica(
        DBInstanceIdentifier=replica_identifier,
        SourceDBInstanceIdentifier=source_db_identifier,
        DBInstanceClass="db.t3.micro",
        PubliclyAccessible=False,
        Tags=[
            {"Key": "Type", "Value": "ReadReplica"},
            {"Key": "Environment", "Value": "Production"},
        ],
    )

    return response
```

Read Replica jest przydatna, gdy aplikacja ma dużo zapytań `SELECT`.

## 5. Best practices dla RDS

Najważniejsze zasady:

- używaj Multi-AZ dla aplikacji produkcyjnych,
- twórz Read Replicas dla dużego ruchu odczytowego,
- przechowuj sekrety poza kodem,
- włącz monitoring,
- ustaw backup retention,
- używaj Parameter Groups do tuningu.

> [!warning]
>
> Częste błędy: publiczna baza bez poprawnego Security Group, brak backupów, zbyt mała instancja dla produkcji i hardcodowane hasła.

## 6. ELB

> [!definition]
>
> ELB, czyli Elastic Load Balancing, rozdziela ruch przychodzący między wiele celów, na przykład instancje EC2, kontenery albo adresy IP.

Load Balancer:

- przyjmuje ruch od użytkowników,
- przekazuje go do zdrowych instancji,
- wykonuje health checki,
- pomaga budować aplikacje wysokodostępne.

Typy Load Balancerów:

- `ALB` - Application Load Balancer, warstwa 7, HTTP/HTTPS,
- `NLB` - Network Load Balancer, warstwa 4, TCP/UDP/TLS,
- `Gateway Load Balancer` - dla urządzeń sieciowych,
- `CLB` - Classic Load Balancer, starsza generacja.

<p style="color:red"><strong>Komentarz mentora:</strong> Materiał miejscami mówi o 3 typach ELB, ale aktualna dokumentacja AWS opisuje także Gateway Load Balancer, a Classic Load Balancer traktuje jako poprzednią generację. Dla nowych aplikacji webowych zwykle wybierasz ALB.</p>

## 7. Application Load Balancer

Przykład tworzenia ALB przez `boto3`:

```python
import boto3


def create_application_load_balancer():
    elbv2_client = boto3.client("elbv2", region_name="eu-central-1")

    response = elbv2_client.create_load_balancer(
        Name="myapp-alb",
        Subnets=[
            "subnet-12345abc",
            "subnet-67890def",
        ],
        SecurityGroups=["sg-0123456789abcdef0"],
        Scheme="internet-facing",
        Type="application",
        IpAddressType="ipv4",
    )

    load_balancer = response["LoadBalancers"][0]
    return load_balancer["LoadBalancerArn"], load_balancer["DNSName"]
```

ALB wymaga subnetów w co najmniej dwóch Availability Zones.

## 8. Target Group i Listener

Target Group grupuje instancje, do których ALB kieruje ruch.

Przykład:

```python
tg_response = elbv2_client.create_target_group(
    Name="myapp-tg",
    Protocol="HTTP",
    Port=8000,
    VpcId=vpc_id,
    HealthCheckProtocol="HTTP",
    HealthCheckPath="/health",
    HealthCheckIntervalSeconds=30,
    HealthCheckTimeoutSeconds=5,
    HealthyThresholdCount=2,
    UnhealthyThresholdCount=3,
    TargetType="instance",
)
```

Listener nasłuchuje na porcie, na przykład `80`, i przekierowuje ruch do Target Group:

```python
elbv2_client.create_listener(
    LoadBalancerArn=load_balancer_arn,
    Protocol="HTTP",
    Port=80,
    DefaultActions=[
        {
            "Type": "forward",
            "TargetGroupArn": target_group_arn,
        }
    ],
)
```

## 9. Health check endpoint

Health check powinien mówić, czy aplikacja naprawdę może obsłużyć ruch.

Przykład w `aiohttp`:

```python
from aiohttp import web
import asyncio
import psutil


async def check_database_connection():
    await asyncio.sleep(0.1)
    return True


async def health_check(request):
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 95:
        return web.Response(status=503, text="Unhealthy: High CPU usage")

    memory = psutil.virtual_memory()
    if memory.percent > 95:
        return web.Response(status=503, text="Unhealthy: High memory usage")

    db_healthy = await check_database_connection()
    if not db_healthy:
        return web.Response(status=503, text="Unhealthy: Database connection failed")

    return web.json_response(
        {
            "status": "healthy",
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "database": "connected",
        }
    )
```

> [!note]
>
> ELB usuwa z rotacji instancje, które nie przechodzą health checków.

<p style="color:red"><strong>Komentarz mentora:</strong> `psutil.cpu_percent(interval=1)` blokuje request na około sekundę. W produkcyjnym health checku zwykle robisz krótkie, przewidywalne sprawdzenie, na przykład status aplikacji i lekkie `SELECT 1` do bazy.</p>

## 10. Best practices dla ELB

Najważniejsze zasady:

- używaj ALB dla HTTP/HTTPS,
- implementuj endpoint `/health`,
- włącz access logs,
- używaj HTTPS z AWS Certificate Manager,
- ustaw poprawny deregistration delay,
- pozwól instancjom na spokojny start przez `HealthCheckGracePeriod`.

> [!warning]
>
> Częste błędy: `/health` zwraca 404 lub 500, timeout jest zbyt krótki, Security Group blokuje ruch z Load Balancera albo brakuje logów.

## 11. Route53

> [!definition]
>
> Route53 to usługa DNS w AWS. Pozwala zarządzać domenami, rekordami DNS, routing policies i health checks.

Kluczowe pojęcia:

- `Hosted Zone` - kontener rekordów DNS dla domeny,
- `Record Sets` - rekordy DNS, na przykład `A`, `AAAA`, `CNAME`, `MX`, `TXT`,
- `Routing Policies` - sposób kierowania ruchu,
- `Health Checks` - sprawdzanie dostępności zasobów.

Nazwa Route53 pochodzi od portu 53 używanego przez DNS.

## 12. Hosted Zone i rekord Alias

Przykład tworzenia Hosted Zone:

```python
def create_hosted_zone(domain_name):
    route53_client = boto3.client("route53")

    response = route53_client.create_hosted_zone(
        Name=domain_name,
        CallerReference=str(hash(domain_name)),
        HostedZoneConfig={
            "Comment": "Hosted zone for MyApp",
            "PrivateZone": False,
        },
    )

    hosted_zone = response["HostedZone"]
    name_servers = response["DelegationSet"]["NameServers"]

    return hosted_zone["Id"], name_servers
```

Rekord `A` typu Alias może wskazywać na Load Balancer.

Zaletą Alias records jest integracja z zasobami AWS, na przykład z ALB.

## 13. Weighted Routing

Weighted routing pozwala podzielić ruch między kilka wersji aplikacji.

Przykład:

```text
stable: 90%
canary: 10%
```

To przydatne przy canary deployment:

- mała część użytkowników trafia na nową wersję,
- monitorujesz błędy,
- jeśli wszystko działa, zwiększasz wagę,
- jeśli są problemy, wracasz do stable.

## 14. Failover Routing

Failover routing przekierowuje ruch do zapasowego endpointu, gdy primary jest niedostępny.

Przykład architektury:

```text
myapp.com
Route53
Health Check
PRIMARY: EU Load Balancer
SECONDARY: US Load Balancer
```

To element disaster recovery.

## 15. AWS CLI

> [!definition]
>
> AWS CLI to narzędzie terminalowe do zarządzania usługami AWS.

AWS CLI przydaje się do:

- automatyzacji,
- CI/CD,
- backupów,
- debugowania,
- sprawdzania stanu zasobów.

Przykładowe komendy:

```bash
aws sts get-caller-identity
aws ec2 describe-instances
aws elbv2 describe-load-balancers
aws rds describe-db-instances
aws s3 ls
```

Można filtrować wyniki przez `--query` i formatować je przez `--output`.

<p style="color:red"><strong>Komentarz mentora:</strong> Materiał pokazuje programowe ustawianie `aws_access_key_id` i `aws_secret_access_key`. Do nauki to wyjaśnia mechanizm, ale w praktyce unikaj statycznych kluczy i preferuj IAM Roles, profile AWS CLI albo OIDC w CI/CD.</p>

## 16. Uruchamianie AWS CLI z Pythona

Materiał pokazuje helper:

```python
import subprocess


def run_aws_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout
```

<p style="color:red"><strong>Komentarz mentora:</strong> `shell=True` z dynamicznie budowanymi komendami jest ryzykowne. Gdy możesz, przekazuj listę argumentów do `subprocess.run([...])` albo użyj `boto3`, które daje strukturalne API.</p>

## 17. Deployment przez AWS CLI

Materiał pokazuje klasę `AWSDeployer`, która:

- kompresuje kod aplikacji,
- uploaduje paczkę do S3,
- tworzy nową wersję Launch Template,
- uruchamia rolling update Auto Scaling Group,
- czeka na zakończenie instance refresh,
- sprawdza `/health`.

Schemat:

```text
zip aplikacji
upload do S3
nowa wersja Launch Template
instance refresh Auto Scaling Group
health check przez Load Balancer
```

<p style="color:red"><strong>Komentarz mentora:</strong> Samo `MinHealthyPercentage=50` nie gwarantuje pełnego zero-downtime w każdej sytuacji. Potrzebujesz poprawnych health checków, wystarczającej pojemności, warmup time, rollbacku i obserwowalności.</p>

## 18. Backup RDS przez AWS CLI

Materiał pokazuje `RDSBackupManager`, który:

- tworzy manual snapshot,
- listuje snapshoty,
- usuwa snapshoty starsze niż wskazany limit,
- może odtworzyć bazę ze snapshotu.

Przykładowe komendy AWS CLI:

```bash
aws rds create-db-snapshot
aws rds describe-db-snapshots
aws rds delete-db-snapshot
aws rds restore-db-instance-from-db-snapshot
```

> [!note]
>
> Automated backupy są zarządzane przez AWS. Manual snapshoty trzeba utrzymywać samodzielnie.

## 19. Production Deployment

Production deployment łączy kilka komponentów:

- VPC,
- publiczne i prywatne subnety,
- Security Groups,
- EC2,
- RDS,
- S3,
- Load Balancer,
- Auto Scaling Group,
- Route53,
- CloudWatch,
- CI/CD.

Materiał pokazuje klasę `ProductionDeployment`, która tworzy:

- VPC `10.0.0.0/16`,
- Internet Gateway,
- 2 publiczne subnety,
- 2 prywatne subnety,
- Security Group dla Load Balancera,
- Security Group dla EC2,
- Security Group dla RDS,
- Multi-AZ RDS,
- bucket S3 z versioning.

Zasada bezpieczeństwa:

```text
Internet -> Load Balancer: 80/443
Load Balancer -> EC2: 8000
EC2 -> RDS: 5432
```

## 20. Auto Scaling Group i Launch Template

Launch Template definiuje konfigurację instancji EC2:

- AMI,
- typ instancji,
- Security Groups,
- User Data,
- IAM Instance Profile,
- monitoring,
- tagi.

Auto Scaling Group utrzymuje oczekiwaną liczbę instancji i może skalować aplikację.

Przykładowe ustawienia z materiału:

```text
MinSize = 2
MaxSize = 10
DesiredCapacity = 2
HealthCheckType = ELB
HealthCheckGracePeriod = 300
Target CPU = 70%
```

<p style="color:red"><strong>Komentarz mentora:</strong> User Data w materiale zapisuje `.env` na instancji i pobiera sekret przez AWS CLI. To lepsze niż hardcodowanie hasła, ale w produkcji pilnuj uprawnień IAM, logów, dostępu do pliku `.env` i rotacji sekretów.</p>

## 21. CI/CD z GitHub Actions

Materiał pokazuje pipeline:

- checkout kodu,
- setup Pythona,
- instalacja zależności,
- testy `pytest`,
- coverage,
- konfiguracja AWS credentials,
- stworzenie release ZIP,
- upload do S3,
- nowa wersja Launch Template,
- instance refresh Auto Scaling Group,
- health check,
- powiadomienie Slack.

Fragment:

```yaml
name: Deploy to AWS

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
```

<p style="color:red"><strong>Komentarz mentora:</strong> Wersje akcji z materiału mogą być już stare. Dla nowych workflow sprawdź aktualne wersje `actions/checkout`, `actions/setup-python` i `aws-actions/configure-aws-credentials`. Dla AWS w GitHub Actions preferuj OIDC i `role-to-assume` zamiast długotrwałych kluczy w secrets.</p>

## 22. Best practices dla Production Deployment

Najważniejsze zasady:

- Multi-AZ dla krytycznych komponentów,
- Auto Scaling dla elastyczności,
- CI/CD zamiast ręcznych deploymentów,
- CloudWatch logs, metrics i alarms,
- Secrets Manager dla sekretów,
- IAM Roles zamiast hardcodowanych credentials,
- health checks na wielu poziomach,
- automated backupy,
- regularne testy disaster recovery,
- strategia rollbacku.

> [!warning]
>
> Częste błędy: Single AZ, brak backupów, brak monitoringów, brak health checków, deployment bez testów i brak rollback strategy.

## 23. Podsumowanie

W tej lekcji poznajesz:

- RDS jako zarządzaną bazę danych,
- Multi-AZ i Read Replicas,
- ELB/ALB do równoważenia ruchu,
- Route53 do DNS i routing policies,
- AWS CLI do automatyzacji,
- VPC i Security Groups,
- Auto Scaling Group,
- CI/CD pipeline,
- monitoring i alerting,
- disaster recovery.

Materiał łączy wcześniejsze lekcje o EC2, S3, Aiohttp, Django/DRF, Git i DevOps z pełniejszą architekturą produkcyjną.

<p style="color:red"><strong>Komentarz mentora:</strong> W podsumowaniu PDF pojawia się odwołanie „Lekcja 43”. To wygląda na błąd numeracji, bo ten plik dotyczy lekcji 36.</p>
