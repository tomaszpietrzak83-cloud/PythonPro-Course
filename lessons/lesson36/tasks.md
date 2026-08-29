# Lesson 36 - Zadania

## TASK 01 - Tworzenie RDS Instance (proste)

Napisz skrypt, który:

- tworzy instancję RDS PostgreSQL `db.t3.micro`,
- ustawia backup retention na 3 dni,
- tworzy snapshot po utworzeniu.

Oczekiwany rezultat:

- działająca instancja RDS,
- jeden manual snapshot.

<p style="color:red"><strong>Komentarz mentora:</strong> To zadanie może tworzyć płatne zasoby AWS. Przed wykonaniem sprawdź region, limity Free Tier, budżety i upewnij się, że po ćwiczeniu usuniesz zasoby.</p>

## TASK 02 - Health Check Endpoint (proste)

Zaimplementuj endpoint:

```text
/health
```

w `aiohttp`.

Endpoint ma:

- zwracać status `200`, gdy aplikacja działa,
- sprawdzać użycie pamięci,
- zwracać JSON z informacjami o statusie.

## TASK 03 - Security Groups (proste)

Stwórz Security Group, która:

- zezwala na HTTP `80` z internetu,
- zezwala na HTTPS `443` z internetu,
- blokuje wszystkie inne porty.

## TASK 04 - S3 Upload (proste)

Napisz funkcję, która:

- kompresuje folder aplikacji do ZIP,
- uploaduje ZIP do bucketa S3,
- wyświetla URL do uploadowanego pliku.

## TASK 05 - AWS CLI Basic Commands (proste)

Użyj AWS CLI do:

- wylistowania wszystkich instancji EC2,
- sprawdzenia statusu baz RDS,
- wylistowania bucketów S3.

Zapisz output do pliku:

```text
aws-resources.txt
```

## TASK 06 - Route53 A Record (proste)

Stwórz rekord `A` w Route53, który:

- wskazuje na adres IP `1.2.3.4`,
- ma TTL `300` sekund,
- działa dla subdomeny `test.yourdomain.com`.

## TASK 07 - Target Group (proste)

Stwórz Target Group, która:

- używa protokołu HTTP na porcie `8000`,
- ma health check endpoint `/health`,
- ma health check interval `30` sekund.

## TASK 08 - Read Replica (proste)

Napisz skrypt, który:

- tworzy Read Replica dla istniejącej bazy RDS,
- czeka, aż replika będzie `available`,
- wyświetla endpoint repliki.

## TASK 09 - Multi-AZ RDS z Failover (średnie)

Zaimplementuj:

- Multi-AZ RDS instance,
- skrypt testujący połączenie,
- symulację failover przez reboot with failover,
- pomiar downtime podczas failover.

Oczekiwany rezultat:

- raport z czasem niedostępności podczas failover.

<p style="color:red"><strong>Komentarz mentora:</strong> Failover i Multi-AZ są dobrym ćwiczeniem architektury, ale w realnym AWS mogą generować koszty. Do nauki możesz najpierw napisać wersję symulowaną.</p>

## TASK 10 - Application Load Balancer Setup (średnie)

Stwórz kompletny setup ALB:

- ALB w dwóch subnetach,
- Target Group z health checks,
- Listener na porcie `80`,
- 2 zarejestrowane instancje EC2.

Przetestuj, czy ruch jest równomiernie dystrybuowany.

## TASK 11 - Weighted Routing Test (średnie)

Zaimplementuj weighted routing w Route53:

- 80% ruchu do primary endpoint,
- 20% ruchu do canary endpoint.

Napisz skrypt, który wysyła 100 requestów i zlicza, który endpoint otrzymał request.

Wynik powinien być zbliżony do `80/20`.

## TASK 12 - Automated Backup Script (średnie)

Napisz skrypt, który:

- codziennie tworzy snapshot RDS o `2:00 AM`,
- usuwa snapshoty starsze niż 7 dni,
- wysyła email notification po zakończeniu,
- loguje wszystkie operacje do pliku.

## TASK 13 - Zero-Downtime Deployment (challenge)

Zaimplementuj pełny zero-downtime deployment:

- Auto Scaling Group z minimum 2 instancjami,
- Launch Template z User Data script,
- rolling update strategy z `MinHealthyPercentage=50`,
- health checks na poziomie Load Balancera,
- automatyczny rollback, jeśli health check nie przejdzie.

Przetestuj deployment i zmierz downtime. Oczekiwany downtime powinien wynosić `0`.

<p style="color:red"><strong>Komentarz mentora:</strong> Traktuj `0 downtime` jako cel, a nie gwarancję wynikającą z jednej flagi. Musisz dobrze ustawić capacity, health checks, warmup i rollback.</p>

## TASK 14 - Disaster Recovery (challenge)

Zaimplementuj disaster recovery plan:

- primary region: `eu-central-1`,
- backup region: `us-east-1`,
- Route53 failover routing z health checks,
- automatyczna replikacja S3 między regionami,
- RDS snapshot copy do backup regionu.

Zasymuluj awarię primary regionu i zmierz czas przełączenia.

## TASK 15 - Custom Metrics i Auto Scaling (challenge)

Stwórz custom metric w CloudWatch:

- metric: liczba active connections do aplikacji,
- publish metric co 1 minutę,
- Auto Scaling policy bazująca na tej metryce,
- scale out, gdy connections `> 100`,
- scale in, gdy connections `< 20`.

Przetestuj z load testing tool, na przykład:

```text
locust
```

## TASK 16 - Blue-Green Deployment (challenge)

Zaimplementuj blue-green deployment:

- dwie Auto Scaling Groups: `blue` i `green`,
- jeden Target Group,
- skrypt przełączający ruch między `blue` i `green`,
- health check validation przed przełączeniem,
- możliwość instant rollback.

Deploy nową wersję do `green`, zwaliduj ją, a potem przełącz ruch.

## TASK 17 - CI/CD z GitHub Actions (challenge)

Stwórz kompletny CI/CD pipeline:

- testy unit i integration przy każdym push,
- automated deployment do staging environment,
- manual approval do production,
- Slack notifications,
- rollback capability.

Pipeline powinien działać end-to-end.

<p style="color:red"><strong>Komentarz mentora:</strong> Przy AWS w GitHub Actions preferuj OIDC i rolę IAM zamiast długotrwałych `AWS_ACCESS_KEY_ID` oraz `AWS_SECRET_ACCESS_KEY`.</p>

## TASK 18 - Cost Optimization (challenge)

Zaimplementuj strategię optymalizacji kosztów:

- scheduled scaling, czyli scale down w nocy,
- Spot Instances dla non-critical workloads,
- S3 Lifecycle policies przenoszące stare release do Glacier,
- kalkulacja RDS Reserved Instances,
- dashboard kosztów w CloudWatch.

Wygeneruj raport z oszacowaniem oszczędności.

## TASK 19 - Monitoring i Alerting (challenge)

Stwórz kompletny monitoring setup:

- CloudWatch Logs dla aplikacji,
- custom metrics: request rate, error rate, latency,
- CloudWatch Alarms:
  - CPU `> 80%` przez 5 minut,
  - error rate `> 5%`,
  - latency `> 2s`,
- SNS notifications do Slack lub email,
- dashboard z kluczowymi metrykami.

## TASK 20 - Full Production Infrastructure (challenge)

Zbuduj kompletną production infrastructure.

Wymagania:

- VPC z publicznymi i prywatnymi subnetami w 3 AZ,
- Multi-AZ RDS z Read Replicas,
- Application Load Balancer z SSL,
- Auto Scaling Group od 2 do 20 instancji,
- Route53 z weighted routing: 90% stable, 10% canary,
- S3 z versioning i lifecycle policies,
- CloudWatch monitoring i alarms,
- CI/CD pipeline z GitHub Actions,
- IAM Roles z zasadą least privilege,
- Secrets Manager dla credentials,
- WAF dla security.

Wszystko potraktuj jako Infrastructure as Code przez `boto3`.
