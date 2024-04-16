#!/bin/bash

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

echo "Apply database migrations"
flask --app app.main db init;
flask --app app.main db migrate;
flask --app app.main db upgrade;

echo "Starting server"

gunicorn --bind 0.0.0.0:5010 --workers 2 'app.main:create_app()'

echo "Server started"