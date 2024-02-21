#!/bin/sh

# Initialzing the shell and if fails, it will stop the execution
set -e

# python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
