#!/bin/sh

# Initialzing the shell and if fails, it will stop the execution
set -e

while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for the database start ($DB_HOST:$DB_PORT)"
  sleep 2
done

echo "Database Started ($DB_HOST:$DB_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
