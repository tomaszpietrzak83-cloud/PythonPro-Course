# Lesson Setup

This lesson uses the course-level virtual environment in the repository root.

From the repository root, install the lesson dependencies with:

```bash
.venv\Scripts\python.exe -m pip install -r lessons\lesson27\requirements.txt
```

Run Django commands from the folder that contains the selected `manage.py`.

Main project for tasks 1-5 and 7-9:

```bash
cd lessons\lesson27\l27_pro
..\..\..\.venv\Scripts\python.exe manage.py runserver
```

File cache project for task 6:

```bash
cd lessons\lesson27\l27_pro_2
..\..\..\.venv\Scripts\python.exe manage.py runserver
```

Redis cache project for task 10:

```bash
cd lessons\lesson27\l27_pro_3
..\..\..\.venv\Scripts\python.exe myapp3\redis_cache_helper.py
..\..\..\.venv\Scripts\python.exe manage.py runserver
```

# Lesson27 Task Map

This file lists where the cache exercises are implemented and how to test them.

## Project Roles

- `l27_pro` is the main project using `LocMemCache`.
- `l27_pro_2` is a separate project using `FileBasedCache`.
- `l27_pro_3` is a separate project using Redis through `django-redis`.

Separate projects are used because `CACHES` is a project-level Django setting, not an app-level setting.

## Tagged Locations

- `l27_pro/l27_pro/settings.py`
  - `CACHES` uses `django.core.cache.backends.locmem.LocMemCache` for task 1.
  - `debug_toolbar` is added when the package is installed.
  - `rest_framework` and `myapp` are registered.
- `l27_pro/l27_pro/urls.py`
  - `/api/products/` maps to the task 3 cached product list.
  - `/api/task7/products-stats/` maps to the task 7 selective-cache view.
  - `/api/task8/clients/` maps to the task 8 and task 9 `ClientViewSet`.
- `l27_pro/myapp/models.py`
  - `Product` is used by product cache examples.
  - `Client` is used by the cached ViewSet examples.
- `l27_pro/myapp/views.py`
  - `# TASK 03` above `product_list`.
  - `# TASK 07` above `product_stats`.
  - `# TASK 08` above `ClientViewSet`.
  - task 9 logic is implemented in `retrieve`, `perform_update`, and `get_client_detail_cache_key`.
- `l27_pro/myapp/serializers.py`
  - `ClientSerializer` serializes the `Client` model for the ViewSet.
- `l27_pro/seed_products.py`
  - Seeds 20 products. 9 products have `short_description`, which is 45%.
- `l27_pro/seed_clients.py`
  - Seeds clients with `Faker("en_US")`.
- `task04.py`
  - Contains the shell outcome for `cache.set()` and `cache.get()`.
- `task05.py`
  - Contains the short answer about using `cache.clear()`.
- `l27_pro_2/l27_pro_2/settings.py`
  - `CACHES` uses `django.core.cache.backends.filebased.FileBasedCache`.
  - Cache files are written to `BASE_DIR / "django_cache"`.
- `l27_pro_2/myapp2/views.py`
  - `# TASK 06` above the cached product list view.
- `l27_pro_3/l27_pro_3/settings.py`
  - `CACHES` uses `django_redis.cache.RedisCache`.
  - Redis location is `redis://127.0.0.1:6379/1`.
- `l27_pro_3/myapp3/views.py`
  - `# TASK 10` above the Redis-cached product list.
  - `ProductViewSet` provides an additional cached DRF endpoint.
- `l27_pro_3/myapp3/redis_cache_helper.py`
  - Starts or creates the `redis-cache` Docker container.
  - Tests Django Redis cache with `cache.set()` and `cache.get()`.
- `requirements.txt`
  - Lists Django, DRF, Debug Toolbar, Faker, and `django-redis`.

## Useful Endpoints

- `http://127.0.0.1:8000/api/products/`
  - Task 3 product list cached for 60 seconds.
- `http://127.0.0.1:8000/api/task7/products-stats/`
  - Task 7 response where only the slow calculation is cached.
- `http://127.0.0.1:8000/api/task8/clients/`
  - Task 8 client list cached for 10 minutes.
- `http://127.0.0.1:8000/api/task8/clients/1/`
  - Task 8 and 9 client detail cached for 1 minute with manual invalidation after update.
- `http://127.0.0.1:8000/api/task6/products/`
  - Task 6 file-based cache endpoint in `l27_pro_2`.
- `http://127.0.0.1:8000/api/task10/products/`
  - Task 10 Redis cache endpoint in `l27_pro_3`.
- `http://127.0.0.1:8000/api/task10/products-viewset/`
  - Extra Redis-cached DRF ViewSet endpoint in `l27_pro_3`.

## Common Commands

Seed products in the main project:

```bash
cd lessons\lesson27\l27_pro
..\..\..\.venv\Scripts\python.exe seed_products.py
```

Seed clients in the main project:

```bash
cd lessons\lesson27\l27_pro
..\..\..\.venv\Scripts\python.exe seed_clients.py
```

Seed products in the Redis project:

```bash
cd lessons\lesson27\l27_pro_3
..\..\..\.venv\Scripts\python.exe seed_products.py
```

Start and test Redis for task 10:

```bash
cd lessons\lesson27\l27_pro_3
..\..\..\.venv\Scripts\python.exe myapp3\redis_cache_helper.py
```

Check a project:

```bash
..\..\..\.venv\Scripts\python.exe manage.py check
```

## Generated Django Files

These files are framework scaffolding or generated database state, so they do not need task markers unless custom lesson code is added there later.

- `l27_pro/manage.py`, `l27_pro_2/manage.py`, and `l27_pro_3/manage.py` are Django command-line entry points.
- `*/asgi.py` and `*/wsgi.py` are generated deployment entry points.
- `*/__init__.py` files mark Python packages.
- `*/apps.py` files contain generated app configs.
- `*/migrations/` folders contain Django migration files.
- `db.sqlite3` files are local database state and should stay outside version control.
- `django_cache/` folders and `.djcache` files are local cache state and should stay outside version control.

## Short Task Notes

- Task 01 configures `LocMemCache`.
- Task 02 configures Django Debug Toolbar.
- Task 03 uses `@cache_page(60)` on a simple product list API view.
- Task 04 tests low-level cache operations in Django shell.
- Task 05 explains that standard Django uses `cache.clear()` rather than a universal built-in `manage.py` cache-clear command.
- Task 06 uses a separate project with `FileBasedCache`.
- Task 07 caches only a simulated slow calculation, not the whole response.
- Task 08 caches `ClientViewSet.list` for 10 minutes and `retrieve` for 1 minute.
- Task 09 invalidates one client-detail cache key after `update` or `partial_update`.
- Task 10 uses Redis as the Django cache backend through `django-redis`.
