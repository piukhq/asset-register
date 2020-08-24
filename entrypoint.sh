#!/bin/sh
echo "Waiting for linkerd to be up"
sleep 20

echo "Collecting statics"
python ./manage.py collectstatic

echo "Starting gunicorn"
exec "$@"