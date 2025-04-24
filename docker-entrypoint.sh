#!/bin/sh

echo "Still Waiting for postgres..."
echo "$POSTGRES_HOST $POSTGRES_PORT"
#while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
 #   sleep 0.1
#done
echo "PostgreSQL started"

flask db upgrade

exec "$@"

#gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app