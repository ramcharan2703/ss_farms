#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --noinput

python manage.py shell -c "
import os
from django.contrib.auth.models import User

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and password:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email or ''}
    )

    if created:
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
    else:
        user.is_staff = True
        user.is_superuser = True
        user.save()
"