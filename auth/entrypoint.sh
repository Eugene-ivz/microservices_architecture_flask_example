#!/bin/bash

echo "Apply database migrations"
python manage.py makemigrations server;
python manage.py makemigrations;
python manage.py migrate server;
python manage.py migrate;


gunicorn --bind 0.0.0.0:5010 --workers 2 app.main:create_app() 