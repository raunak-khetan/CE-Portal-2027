#!/bin/sh
python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --no-input
gunicorn cityelimination.wsgi:application --bind 0.0.0.0:80 --log-level=debug --timeout 180  --workers 4
