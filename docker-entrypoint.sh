#!/bin/bash

set -e

FLAG_FILE=/app/.initialized

if [ ! -f "$FLAG_FILE" ]; then
  python manage.py migrate
  python manage.py shell <<EOF
from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Admin123')
EOF
  python manage.py load_file /app/inputs/input.json
  python manage.py load_file /app/inputs/input.xml

  touch "$FLAG_FILE"
fi

python manage.py runserver 0.0.0.0:8000

exec "$@"
