import os
from django.http import JsonResponse
from django.urls import path

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "lesson-only")
ROOT_URLCONF = __name__
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes"]
DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql",
                         "NAME": "lesson", "USER": "lesson", "PASSWORD": "lesson-local",
                         "HOST": "database", "PORT": 5432}}


def health(request):
    return JsonResponse({"status": "ready"})


urlpatterns = [path("health", health)]
