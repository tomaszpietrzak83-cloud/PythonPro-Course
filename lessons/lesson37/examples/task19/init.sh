#!/bin/sh
set -eu
django-admin migrate --settings=web --noinput
django-admin shell --settings=web -c 'from django.contrib.auth import get_user_model; import os; users = get_user_model().objects; username = os.environ["DJANGO_SUPERUSER_USERNAME"]; users.create_superuser(username, password=os.environ["DJANGO_SUPERUSER_PASSWORD"]) if not users.filter(username=username).exists() else None'
