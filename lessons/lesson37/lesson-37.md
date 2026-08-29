# Lekcja 37: Docker i Konteneryzacja Aplikacji

`#lekcja` `#python` `#docker` `#devops` `#konteneryzacja`

W tej lekcji poznajesz Docker, czyli technologię używaną do pakowania, uruchamiania i wdrażania aplikacji w kontenerach.

Główne tematy:

- konteneryzacja i wirtualizacja,
- podstawy Dockera,
- `Dockerfile`,
- obrazy i kontenery,
- sieci Docker,
- mapowanie portów,
- Docker Compose,
- aplikacja Django REST Framework w kontenerach,
- Redis, PostgreSQL i Nginx,
- AI w kontenerach.

## 1. Konteneryzacja i wirtualizacja

Konteneryzacja rozwiązuje klasyczny problem:

```text
Na moim komputerze działa.
```

Aplikacja jest pakowana razem z zależnościami, dzięki czemu może działać spójnie na różnych środowiskach.

> [!definition]
>
> Konteneryzacja to metoda pakowania aplikacji wraz z jej zależnościami w izolowane jednostki zwane kontenerami.

Porównanie:

| Aspekt | Wirtualizacja (VM) | Konteneryzacja |
|---|---|---|
| Izolacja | własny system operacyjny | współdzielony kernel hosta |
| Rozmiar | zwykle GB | zwykle MB |
| Start | minuty | sekundy |
| Wydajność | narzut hypervisora | prawie natywna |
| Przenośność | średnia | wysoka |

Kontenery są lżejsze od maszyn wirtualnych, ale nie zastępują ich w każdym przypadku.

## 2. Kiedy kontener, a kiedy VM?

Kontenery są dobre dla:

- mikroserwisów,
- CI/CD,
- aplikacji webowych,
- środowisk developerskich,
- szybkiego skalowania.

VM są lepsze, gdy potrzebujesz:

- pełnej izolacji systemu,
- różnych systemów operacyjnych,
- legacy aplikacji wymagającej konkretnego OS,
- mocniejszej separacji bezpieczeństwa.

> [!warning]
>
> Kontenery współdzielą kernel hosta. Jeśli kernel zostanie skompromitowany, zagrożone mogą być wszystkie kontenery.

## 3. Docker

> [!definition]
>
> Docker to platforma do tworzenia, wdrażania i uruchamiania aplikacji w kontenerach.

Podstawowe pojęcia:

- `Docker Engine` - daemon zarządzający kontenerami,
- `Docker Image` - szablon tylko do odczytu z aplikacją,
- `Docker Container` - uruchomiona instancja obrazu,
- `Dockerfile` - plik z instrukcjami budowania obrazu,
- `Docker Hub` - publiczny rejestr obrazów.

Historia z materiału: Docker został wydany w 2013 roku przez firmę dotCloud, później Docker Inc.

## 4. Podstawowy Dockerfile

Przykładowy `Dockerfile` dla aplikacji Python:

```dockerfile
FROM python:3.11-slim

LABEL maintainer="developer@example.com"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser $APP_HOME
USER appuser

EXPOSE 8000

CMD ["python", "main.py"]
```

Ważne elementy:

- `FROM` wybiera obraz bazowy,
- `WORKDIR` ustawia katalog pracy,
- `COPY` kopiuje pliki,
- `RUN` wykonuje komendę podczas budowania obrazu,
- `USER` pozwala uruchomić aplikację bez roota,
- `EXPOSE` dokumentuje port,
- `CMD` definiuje komendę startową.

## 5. Prosta aplikacja w kontenerze

Przykład aplikacji `aiohttp`:

```python
from aiohttp import web


async def hello(request):
    return web.Response(text="Hello from Docker!")


async def health(request):
    return web.json_response({"status": "healthy"})


app = web.Application()
app.router.add_get("/", hello)
app.router.add_get("/health", health)


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8000)
```

Struktura projektu:

```text
my-app/
    Dockerfile
    requirements.txt
    main.py
```

Budowanie i uruchomienie:

```bash
docker build -t my-python-app:1.0 .
docker run -d -p 8000:8000 --name my-app my-python-app:1.0
curl http://localhost:8000/
```

<p style="color:red"><strong>Komentarz mentora:</strong> W kontenerze aplikacja musi nasłuchiwać na `0.0.0.0`, a nie tylko na `127.0.0.1`, bo inaczej mapowanie portu z hosta może nie działać.</p>

## 6. Warstwy obrazu i cache

Docker buduje obrazy warstwami. Każda instrukcja w `Dockerfile` tworzy warstwę.

Zła kolejność:

```dockerfile
FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

Lepsza kolejność:

```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Dlaczego to ma znaczenie:

- zależności zmieniają się rzadziej niż kod,
- Docker może użyć cache,
- kolejne buildy są szybsze.

## 7. Multi-stage build

Multi-stage build pozwala stworzyć mniejszy obraz produkcyjny.

Przykład:

```dockerfile
FROM python:3.11 AS builder

WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY main.py .

RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["python", "main.py"]
```

Pierwszy etap buduje zależności, a drugi zawiera tylko to, co jest potrzebne do uruchomienia aplikacji.

## 8. Podstawowe komendy Docker

Najważniejsze komendy:

```bash
docker build -t nazwa:tag .
docker images
docker run -d -p 8000:8000 --name kontener nazwa:tag
docker ps
docker ps -a
docker stop kontener
docker rm kontener
docker logs kontener
docker logs -f kontener
docker exec -it kontener bash
docker rmi nazwa:tag
docker system prune -a
```

> [!warning]
>
> `docker system prune -a` usuwa nieużywane obrazy, kontenery i sieci. Używaj świadomie.

## 9. .dockerignore

`.dockerignore` działa podobnie do `.gitignore`.

Typowa zawartość:

```text
__pycache__/
*.pyc
.git/
.env
venv/
```

Cel:

- mniejszy context builda,
- szybszy build,
- mniej przypadkowych plików w obrazie,
- mniejsze ryzyko skopiowania sekretów.

> [!warning]
>
> Nigdy nie commituj sekretów do obrazów. Używaj zmiennych środowiskowych albo systemów secrets management.

## 10. Sieci Docker

> [!definition]
>
> Sieć Docker to wirtualna sieć umożliwiająca komunikację między kontenerami oraz między kontenerami i światem zewnętrznym.

Typy sieci:

- `bridge` - domyślna sieć dla pojedynczego hosta,
- `host` - kontener używa sieci hosta,
- `none` - brak sieci,
- `overlay` - sieć rozproszona dla Docker Swarm,
- `macvlan` - kontener dostaje własny adres MAC.

Tworzenie sieci:

```bash
docker network create my-app-network
docker network ls
docker network inspect my-app-network
```

Uruchomienie kontenerów w tej samej sieci:

```bash
docker run -d --name backend --network my-app-network backend-image
docker run -d --name frontend --network my-app-network frontend-image
```

W niestandardowej sieci kontenery mogą komunikować się po nazwach:

```text
http://backend:8000/api
```

## 11. Mapowanie portów

Mapowanie portów udostępnia usługę kontenera na hoście.

Format:

```text
-p host_port:container_port
```

Przykłady:

```bash
docker run -p 8000:8000 myapp
docker run -p 80:8000 myapp
docker run -p 127.0.0.1:8000:8000 myapp
docker run -p 8000 myapp
docker run -p 8000:8000 -p 8001:8001 myapp
```

## 12. Docker DNS i service discovery

Docker ma wbudowany DNS w obrębie niestandardowej sieci.

Przykład:

```python
import asyncpg


async def connect_to_database():
    connection = await asyncpg.connect(
        host="database",
        port=5432,
        user="postgres",
        password="secret",
        database="myapp",
    )
    version = await connection.fetchval("SELECT version()")
    await connection.close()
    return version
```

Zamiast hardcodować IP, aplikacja używa nazwy serwisu lub kontenera.

<p style="color:red"><strong>Komentarz mentora:</strong> W domyślnej sieci `bridge` nazwy kontenerów nie działają tak wygodnie jak w niestandardowych sieciach. Dla aplikacji wielokontenerowych twórz własną sieć albo używaj Docker Compose.</p>

## 13. Docker Compose

> [!definition]
>
> Docker Compose to narzędzie do definiowania i uruchamiania wielokontenerowych aplikacji Docker.

Compose pozwala opisać w YAML:

- serwisy,
- sieci,
- wolumeny,
- zmienne środowiskowe,
- zależności między kontenerami.

Korzyści:

- jedna deklaratywna konfiguracja,
- łatwe uruchamianie wielu kontenerów,
- automatyczne sieci i wolumeny,
- prostsze środowiska developerskie.

## 14. Przykładowy docker-compose.yml

Materiał pokazuje aplikację z backendem, PostgreSQL i Redis:

```yaml
version: "3.8"

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:secret@database:5432/myapp
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      - database
      - cache
    networks:
      - app-network
    restart: unless-stopped

  database:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

  cache:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
```

<p style="color:red"><strong>Komentarz mentora:</strong> Top-level `version: "3.8"` jest dziś zachowane głównie dla kompatybilności i Docker Compose v2 może ostrzegać, że jest obsolete. Materiał zostawiam, ale w nowych plikach możesz pominąć `version` i pisać według Compose Specification.</p>

## 15. Komendy Docker Compose

Materiał używa formy `docker-compose`:

```bash
docker-compose up
docker-compose up -d
docker-compose down
docker-compose down -v
docker-compose logs
docker-compose logs backend
docker-compose logs -f
docker-compose restart backend
docker-compose build
docker-compose up --build
docker-compose ps
```

<p style="color:red"><strong>Komentarz mentora:</strong> W nowszym Docker Compose standardową formą jest `docker compose` bez myślnika. `docker-compose` to starsze narzędzie standalone, nadal spotykane w materiałach i starszych projektach.</p>

## 16. Wiele środowisk w Compose

Materiał pokazuje podział konfiguracji:

```text
docker-compose.yml
docker-compose.override.yml
docker-compose.prod.yml
```

Przykład:

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    env_file:
      - .env
```

W development można montować kod jako volume:

```yaml
services:
  backend:
    volumes:
      - ./backend:/app
    environment:
      - DEBUG=true
```

W produkcji kod powinien być już w obrazie, a nie montowany z hosta.

## 17. depends_on i health checks

`depends_on` pozwala określić zależności między serwisami.

Z health checkami backend może czekać, aż baza i cache będą gotowe:

```yaml
services:
  backend:
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_healthy

  database:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
```

## 18. Aplikacja Django REST w kontenerach

Materiał pokazuje projekt:

```text
blog-api/
    docker-compose.yml
    .env
    .dockerignore
    backend/
        Dockerfile
        requirements.txt
        manage.py
        config/
        blog/
    nginx/
        Dockerfile
        nginx.conf
```

Usługi:

- Django REST Framework jako backend,
- PostgreSQL jako baza danych,
- Redis jako cache,
- Nginx jako reverse proxy,
- wolumeny dla danych i statycznych plików.

## 19. Backend Django w kontenerze

Przykładowy `Dockerfile`:

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN useradd -m -u 1000 django && chown -R django:django /app
USER django

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

Fragment ustawień Django:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "database",
        "PORT": "5432",
    }
}
```

## 20. docker-compose dla blog API

Schemat:

```text
User -> Nginx :80 -> Django Backend :8000
                      -> PostgreSQL :5432
                      -> Redis :6379
```

Wolumeny:

- `postgres-data`,
- `redis-data`,
- `static-files`.

Nginx przekazuje requesty do backendu:

```nginx
upstream backend {
    server backend:8000;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /static/;
    }
}
```

> [!warning]
>
> Dane w kontenerach są efemeryczne. Bez wolumenów dane znikną po usunięciu kontenera.

## 21. AI w kontenerach

Docker dobrze nadaje się do aplikacji AI:

- API używające OpenAI,
- lokalne modele ML,
- workers do długich zadań,
- oddzielne serwisy dla inference.

Przykład z materiału:

```python
import os

from aiohttp import web
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def chat_endpoint(request):
    data = await request.json()
    user_message = data.get("message")

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem."},
            {"role": "user", "content": user_message},
        ],
    )

    return web.json_response(
        {"response": response.choices[0].message.content}
    )
```

<p style="color:red"><strong>Komentarz mentora:</strong> Przykład z OpenAI pokazuje sens architektury, ale przed użyciem sprawdź aktualny model i aktualny styl SDK. Klucza `OPENAI_API_KEY` nie zapisuj w obrazie ani repozytorium.</p>

## 22. Podsumowanie

W tej lekcji najważniejsze są:

- różnica między konteneryzacją i wirtualizacją,
- budowanie obrazu przez `Dockerfile`,
- cache warstw,
- multi-stage build,
- podstawowe komendy Docker,
- `.dockerignore`,
- sieci Docker,
- mapowanie portów,
- Docker DNS,
- Docker Compose,
- health checki i `depends_on`,
- wolumeny,
- konteneryzacja aplikacji Django REST,
- Nginx jako reverse proxy,
- konteneryzacja aplikacji AI.

Docker dobrze łączy się z wcześniejszymi tematami: Aiohttp, FastAPI, PostgreSQL, Redis, AWS i DevOps.
