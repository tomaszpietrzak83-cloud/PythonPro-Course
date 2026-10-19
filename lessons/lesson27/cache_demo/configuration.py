"""Connect one shared app to three independent Django settings modules."""

import os
from copy import deepcopy
from pathlib import Path


def configure_demo(namespace):
    """Keep the homework backend intact and give the demo its own storage."""
    namespace["INSTALLED_APPS"].append("cache_demo")
    project = namespace["BASE_DIR"].name
    namespace["DEMO_PROJECT"] = project
    namespace["DEMO_CONTROL_PORT"] = os.environ.get("LESSON27_CONTROL_PORT")
    # Start collapsed so the diagnostic panel does not cover demo controls.
    # Source: https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#show-collapsed
    namespace["DEBUG_TOOLBAR_CONFIG"] = {**namespace.get("DEBUG_TOOLBAR_CONFIG", {}), "SHOW_COLLAPSED": True}
    namespace["DEMO_PORT"] = {"l27_pro": 8000, "l27_pro_2": 8001, "l27_pro_3": 8002}[project]
    backend = deepcopy(namespace["CACHES"]["default"])
    backend["KEY_PREFIX"] = "lesson27-demo"
    if project == "l27_pro":
        backend["LOCATION"] = "lesson27-demo-memory"
    elif project == "l27_pro_2":
        backend["LOCATION"] = namespace["BASE_DIR"] / "django_cache" / "presentation"
    else:
        backend["OPTIONS"] = {**backend.get("OPTIONS", {}), "SOCKET_CONNECT_TIMEOUT": 1, "SOCKET_TIMEOUT": 1}
    namespace["CACHES"]["demo"] = backend
    database = os.environ.get("LESSON27_DEMO_DATABASE")
    if database:
        # The launcher supplies a SQLite copy, so presentation edits cannot
        # change the student's original homework database.
        namespace["DATABASES"]["default"]["NAME"] = Path(database)
