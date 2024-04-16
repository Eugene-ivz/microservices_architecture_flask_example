#!/bin/bash

status=$(curl -s -o /dev/null -w "%{http_code}" host.docker.internal:8050/api/overview --user guest:guest)

if [ $status = "200" ]; then
   echo "rabbitMQ running"
fi

status=$(curl -s -o /dev/null -w "%{http_code}" host.docker.internal:27017)

if [ $status = "200" ]; then
   echo "mongodb running"
fi
echo "Starting server"

gunicorn --bind 0.0.0.0:5020 --workers 2 'app.main:create_app()'

echo "Server started"