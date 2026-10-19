# Lesson 27 Cache Lab

The shared presentation app lives in this directory. Three Django projects load
it, each with its own settings and a presentation copy of its database. The
launcher also serves a lightweight control page on port 7999. This page remains
available when all three Django servers are stopped.

## Start the presentation

From the repository root, in PowerShell:

```powershell
.\.venv\Scripts\python.exe lessons\lesson27\cache_demo\run_demo.py
```

Alternatively, open `cache_demo/start_app.py` in VS Code and press Play with the
repository's `.venv` interpreter selected. The terminal prints a clickable link:

```text
Control panel ready: http://127.0.0.1:7999/
```

Pressing Play again recognizes an existing Cache Lab controller, prints its URL
and avoids duplicate processes. Home has a `runserver` / `Stop server` button
for each project, and reports the PID of running servers. All three may be stopped
and restarted while Home stays available. Home links on task pages return to the
controller. Only child processes owned by this launcher can be stopped.

The launcher creates SQLite copies in `cache_demo/runtime/` on first startup,
applies existing migrations to those copies and starts:

| Project | URL | Homework backend | Tasks |
| --- | --- | --- | --- |
| l27_pro | http://127.0.0.1:8000/ | LocMemCache | 1–5, 7–9 |
| l27_pro_2 | http://127.0.0.1:8001/ | FileBasedCache | 6 |
| l27_pro_3 | http://127.0.0.1:8002/ | Redis | 10 |

Redis is an additional storage service on port 6379, not a fourth Django server.
If Redis is unavailable, the launcher tries the existing `redis-cache` Docker
container, or creates one from `redis:7-alpine`. Start Docker Desktop first.
An unavailable Redis service is shown as a real connection failure; tasks 1–9
remain usable. The launcher never substitutes a fake cache.

The browser opens automatically at http://127.0.0.1:7999/. Ctrl+C stops the control
service and all three Django child processes.
Redis is left running because other lessons may use it. Python edits require a
launcher restart: `--noreload` ensures exactly three Django processes.

Optional flags:

```powershell
.\.venv\Scripts\python.exe lessons\lesson27\cache_demo\run_demo.py --no-browser
.\.venv\Scripts\python.exe lessons\lesson27\cache_demo\run_demo.py --skip-redis-start
.\.venv\Scripts\python.exe lessons\lesson27\cache_demo\start_app.py --no-autostart
```

Stop unrelated existing servers on ports 7999–8002 before launching; the script checks for
occupied ports and does not terminate unrelated processes.

## Present a task

1. Choose a task on Home. Its link opens the appropriate server port.
2. Choose Quick demo or Homework settings. The original homework times remain
   visible. Task 7's existing homework timeout is already 7 seconds.
3. Optionally enter custom whole-second lifetimes from 1 to 3600.
4. Click Apply & restart. Staged inputs do not change active entries silently.
5. Use Next step, or the individual operation buttons. Inspect the result,
   SQL count, server duration, response and request history.
6. Explain the flow using What did Python do? and the expandable homework source.
7. Switch PL / ENG at any time. This changes text without resetting requests or
   timers. The language is preserved on reload and in cross-port navigation.

Task 2 provides an original API link. The Debug Toolbar remains available on HTML
pages, initially collapsed to avoid covering the presentation controls. Its
panels describe their captured requests; the demo history measures each action.

Reset scenario preserves applied lifetimes and resets the walkthrough.
Previous step selects the preceding walkthrough instruction; Next step can
execute it again. It does not reverse real writes or restore an earlier cache
state. Use Reset scenario to begin a fresh demonstration.

Each task has five bilingual questions with answers. The first two are visible
initially, with answers collapsed. Click a question to reveal its answer; the
Want more simple questions? button reveals one additional collapsed question.
Changing language preserves open answers and already revealed questions.

## Modules to study individually

| File | Responsibility | Useful concepts |
| --- | --- | --- |
| configuration.py | Connect the shared app and isolated backend alias | dictionaries, deepcopy, project settings |
| catalog.py | Task metadata, translations, allowlisted source excerpts | pathlib, dictionaries, AST source inspection |
| views.py / urls.py | HTML routes, backend status and JSON actions | Django views, decorators, CSRF, JsonResponse |
| engine.py | Execute and measure homework operations | closures, subclassing, cache_page, query wrappers |
| start_app.py | VS Code Play entry point | imports, __main__, delegation |
| run_demo.py | Start the controller and prepare demo databases | argparse, ports, try/finally |
| controller.py | Serve Home and manage owned Django processes | HTTP handlers, subprocess, tokens, process lifecycle |
| static/cache_demo/api.js | Send same-origin JSON requests | fetch, async/await, CSRF token |
| questions.py / static/cache_demo/questions.js | Task question banks and progressive answer disclosures | dictionaries, reusable shapes, native details elements |
| static/cache_demo/scenarios.js | Describe presets and walkthrough steps | arrays, objects, data-driven actions |
| static/cache_demo/timers.js | Render independent countdowns | Map, monotonic time, expiration |
| static/cache_demo/i18n.js | Translate interface text | dictionaries, interpolation, localStorage |
| static/cache_demo/app.js | Connect controls with the other modules | events, DOM updates, state |

The original views remain in their project folders. The presentation removes
the fixed `cache_page` wrapper and reapplies Django's decorator with the selected
lifetime and demo alias. It does not replace full-view caching with a homemade
dictionary. A per-request closure tells us whether the inner view executed:
execution means MISS; a returned cached response means HIT.

The main homework module adds optional arguments to `get_complex_product_stats`
and small extension points to `ClientViewSet`. Their defaults preserve homework
behavior. The demo subclass reuses the student's detail read and `perform_update`
invalidation rather than duplicating that logic.

## Cache isolation and measurement

- `default` remains the homework cache; `demo` uses the same backend type with
  its own namespace. Memory uses a separate location, file cache a `presentation`
  subdirectory, and Redis prefixed keys in the existing database.
- Each browser and task has an isolated namespace. Reset advances its generation:
  old response keys become unreachable and expire naturally. Reset does not
  physically delete every old file or flush Redis.
- Task 5 uses a dedicated LocMem sandbox to demonstrate real `cache.clear()`
  without clearing other tasks or homework entries.
- Tasks 8–9 create separate, clearly named demo client rows for each task/browser.
  Reset restores only that row's initial city. Existing clients are never edited.
- A named demo product is created only if a project's product table is empty.
- With the launcher, every database operation uses the presentation copies.
  Running an individual `manage.py runserver` uses that project's normal database;
  prefer the shared launcher for presentations.
- Countdown starts after result creation, not at the start of a slow calculation.
  HIT does not renew it. A new request confirms expiration.
- SQL counts exclude fixture preparation but include the demonstrated operation.
  Server duration includes fixture preparation and the operation, not network
  transfer or browser rendering.
- Reading a countdown sends no HTTP requests. Backend health checks use unrelated
  keys. Browser caching is disabled for the action API.
- File presence does not imply a valid entry: expired files may remain on disk.
- Redis shows a real PING and the TTL of a companion marker with the same lifetime
  as the page response. The marker is not the internal Django page-cache key.

## UI sources

Bootstrap 5.3.8 supplies ready-made styles and interactive components. Exact source
links are also included in HTML comments beside the imports and component usage:

- https://getbootstrap.com/docs/5.3/getting-started/introduction/
- https://getbootstrap.com/docs/5.3/components/buttons/
- https://getbootstrap.com/docs/5.3/components/accordion/

Bootstrap CSS and JS load from jsDelivr. Internet access is needed for those CDN
assets. Request logic, scenarios, translations and timers are local project code.

## Verify the presentation

Run from each project's directory using the repository virtual environment:

```powershell
..\..\..\.venv\Scripts\python.exe manage.py check
..\..\..\.venv\Scripts\python.exe manage.py test cache_demo
```

Tests cover hit/miss detection, unchanged expiration on HIT, reset isolation,
file creation, selective caching, detail invalidation, independent cached lists,
timeout validation, correct task ports, CSRF protection, controller authorization
and process ownership. Main-project tests
are skipped in the other projects. The Redis integration test requires real Redis
and reports a skip when it is unavailable.
