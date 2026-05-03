#!/bin/sh

# Run migrations
python manage.py migrate

# Create superuser (optional - you'll need to set environment variables)
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --noinput
fi

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application
