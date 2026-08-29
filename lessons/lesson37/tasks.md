# Lesson 37 - Zadania

## TASK 01 - Pierwszy kontener (proste)

Stwórz prosty `Dockerfile` dla aplikacji Python, która wyświetla:

```text
Hello, Docker!
```

Zbuduj obraz i uruchom kontener.

## TASK 02 - Zmienne środowiskowe (proste)

Zmodyfikuj kontener z zadania 1, aby przyjmował zmienną środowiskową:

```text
NAME
```

Program ma wyświetlać:

```text
Hello, {NAME}!
```

Uruchom kontener z różnymi wartościami `NAME`.

## TASK 03 - Mapowanie portów (proste)

Stwórz prosty serwer HTTP w Pythonie, na przykład `aiohttp`, który nasłuchuje na porcie `8000`.

Uruchom go w kontenerze i zmapuj na port `3000` hosta.

## TASK 04 - Wolumin dla danych (proste)

Stwórz kontener, który zapisuje logi do pliku.

Użyj woluminu, aby logi przetrwały restart kontenera.

## TASK 05 - Multi-stage build (proste)

Przepisz `Dockerfile` z zadania 3, używając multi-stage build.

Porównaj rozmiary obrazów:

- przed multi-stage build,
- po multi-stage build.

## TASK 06 - Docker Compose podstawowy (proste)

Stwórz `docker-compose.yml` dla aplikacji z dwoma serwisami:

- `backend` - aplikacja Python,
- `database` - PostgreSQL.

Backend powinien połączyć się z bazą danych.

<p style="color:red"><strong>Komentarz mentora:</strong> W nowych projektach możesz używać komendy `docker compose` bez myślnika. Starsze materiały często pokazują `docker-compose`.</p>

## TASK 07 - Health checks (proste)

Dodaj health check do serwisu PostgreSQL w `docker-compose.yml`.

Backend powinien czekać, aż baza będzie zdrowa.

Użyj:

```yaml
depends_on:
  database:
    condition: service_healthy
```

## TASK 08 - Sieć niestandardowa (proste)

Stwórz dwa kontenery w niestandardowej sieci `bridge`.

Sprawdź, czy mogą komunikować się po nazwach.

## TASK 09 - API z cache (średnie)

Stwórz aplikację API w `aiohttp` albo FastAPI z Redis cache.

Zasada działania:

- pierwszy request pobiera dane z "bazy", może być symulowana,
- kolejne requesty pobierają dane z cache.

Użyj `docker-compose`.

Serwisy:

- `backend`,
- `redis`.

## TASK 10 - CRUD API w kontenerach (średnie)

Stwórz pełne CRUD API dla prostej encji, na przykład książki.

Użyj:

- Django albo FastAPI,
- PostgreSQL,
- Docker Compose.

Endpointy:

```text
GET /books
POST /books
PUT /books/{id}
DELETE /books/{id}
```

## TASK 11 - Nginx reverse proxy (średnie)

Dodaj Nginx jako reverse proxy przed backend z zadania 10.

Nginx powinien:

- przekierowywać requesty do backendu,
- serwować pliki statyczne.

## TASK 12 - Środowiska dev/prod (średnie)

Stwórz dwa pliki:

- `docker-compose.yml` - konfiguracja bazowa,
- `docker-compose.prod.yml` - konfiguracja produkcyjna.

W development:

- montuj kod jako volume,
- umożliw hot reload.

W production:

- nie montuj kodu jako volume,
- uruchamiaj kod z obrazu.

Przetestuj oba tryby.

## TASK 13 - Microservices architecture (challenge)

Stwórz architekturę mikroserwisów z trzema serwisami:

- `users-service` - zarządzanie użytkownikami,
- `posts-service` - posty użytkowników,
- `api-gateway` - agreguje dane z obu serwisów.

Każdy serwis ma mieć własną bazę danych.

Użyj wzorca:

```text
database per service
```

i uruchom wszystko przez Docker Compose.

## TASK 14 - Message queue z Celery (challenge)

Stwórz aplikację z:

- Django,
- Celery,
- Redis jako broker,
- PostgreSQL jako database.

Backend przyjmuje zadania, na przykład generowanie raportu.

Celery worker przetwarza zadania w tle.

Serwisy:

- `backend`,
- `celery-worker`,
- `redis`,
- `database`.

## TASK 15 - Monitoring z Prometheus (challenge)

Dodaj monitoring do aplikacji z zadania 10.

Użyj:

- Prometheus do zbierania metryk,
- Grafana do wizualizacji.

Backend powinien eksponować endpoint:

```text
/metrics
```

Serwisy:

- `backend`,
- `database`,
- `prometheus`,
- `grafana`.

## TASK 16 - Scaling serwisów (challenge)

Zmodyfikuj `docker-compose.yml` z zadania 11, aby uruchamiał 3 instancje backendu.

Nginx powinien load balancować między nimi metodą round-robin.

Użyj:

```bash
docker-compose up --scale backend=3
```

<p style="color:red"><strong>Komentarz mentora:</strong> Przy skalowaniu w Compose unikaj stałej nazwy `container_name` dla backendu, bo blokuje uruchomienie wielu kopii tego samego serwisu.</p>

## TASK 17 - CI/CD pipeline (challenge)

Stwórz GitHub Actions workflow, który:

- buduje obraz Docker,
- uruchamia testy w kontenerze,
- pushuje obraz do Docker Hub, jeśli testy przeszły.

## TASK 18 - WebSocket chat w kontenerach (challenge)

Stwórz aplikację chat w czasie rzeczywistym przez WebSocket.

Użyj Redis Pub/Sub do komunikacji między instancjami.

Uruchom wiele instancji backendu. Użytkownicy podłączeni do różnych instancji powinni widzieć swoje wiadomości.

Serwisy:

- `backend` x3,
- `redis`,
- `nginx`.

## TASK 19 - Init containers pattern (challenge)

Stwórz init container albo osobny skrypt startowy, który przed startem backendu:

- czeka, aż baza będzie dostępna,
- uruchamia migracje,
- tworzy superusera, jeśli nie istnieje.

Wykorzystaj:

- Docker Compose `depends_on`,
- custom entrypoint scripts.

## TASK 20 - Full-stack app z AI (challenge)

Stwórz kompletną aplikację full-stack.

Temat:

```text
System rekomendacji książek wykorzystujący embeddings z OpenAI.
```

Komponenty:

- frontend: React albo Vue w kontenerze z Nginx,
- backend: FastAPI z endpointem do AI, OpenAI API albo Ollama local,
- database: PostgreSQL,
- cache: Redis,
- queue: Celery dla długich zadań AI.

<p style="color:red"><strong>Komentarz mentora:</strong> Kluczy API nie zapisuj w `Dockerfile` ani w obrazie. Przekazuj je przez zmienne środowiskowe, sekrety CI/CD albo lokalny plik `.env`, którego nie commitujesz.</p>
