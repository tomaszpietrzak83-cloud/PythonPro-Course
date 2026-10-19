import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "lesson29-local-learning-only"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
ROOT_URLCONF = "academy.urls"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "learning",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / ".runtime/lesson.sqlite3",
        "OPTIONS": {"timeout": 30},
    }
}
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {},
    }
]
STATIC_URL = "/static/"
TIME_ZONE = "Europe/Warsaw"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# A real, local Celery broker. Redis can replace it without changing tasks.
RUNTIME_DIR = BASE_DIR / ".runtime"
for folder in ("queue", "processed", "results", "control"):
    (RUNTIME_DIR / folder).mkdir(parents=True, exist_ok=True)
CELERY_BROKER_URL = os.environ.get("LESSON29_BROKER_URL", "filesystem://")
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "data_folder_in": str(RUNTIME_DIR / "queue"),
    "data_folder_out": str(RUNTIME_DIR / "queue"),
    "processed_folder": str(RUNTIME_DIR / "processed"),
    "control_folder": str(RUNTIME_DIR / "control"),
    "store_processed": True,
    "polling_interval": 0.5,
}
CELERY_RESULT_BACKEND = os.environ.get(
    # Celery's filesystem backend uses the raw path after file:// and does
    # not decode %20 from Path.as_uri(). Keep spaces in local paths intact.
    "LESSON29_RESULT_BACKEND", "file://" + (RUNTIME_DIR / "results").as_posix()
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_PUBLISH_RETRY = False
CELERY_BROKER_CONNECTION_TIMEOUT = 3
CELERY_TIMEZONE = TIME_ZONE
# TASK 18
CELERY_TASK_DEFAULT_QUEUE = "default"
# TASK 18
CELERY_TASK_ROUTES = {
    "learning.tasks.send_notification": {"queue": "priority_queue"}
}
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # TASK 04
    "timestamp-every-ten-seconds": {
        "task": "learning.tasks.log_timestamp",
        "schedule": 10.0,
    },
    # TASK 06
    "users-at-23": {
        "task": "learning.tasks.count_users",
        "schedule": crontab(hour=23, minute=0),
    },
    # TASK 12
    "daily-log-cleanup": {
        "task": "learning.tasks.clean_logs",
        "schedule": crontab(hour=0, minute=15),
    },
    # TASK 13
    "hourly-page-title": {
        "task": "learning.tasks.scrape_title",
        "schedule": crontab(minute=0),
    },
}
