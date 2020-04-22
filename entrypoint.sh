#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
#rm -rf easy_data/migrations
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear
#python manage.py runserver 0.0.0.0:8000
gunicorn FakeNews.wsgi:application --bind 0.0.0.0:8000
exec "$@"