#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='ramcharan').exists() or User.objects.create_superuser('ramcharan','ramcharan0127@gmail.com','Charan@123')"