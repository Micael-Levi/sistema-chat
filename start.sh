#!/bin/bash

# echo "Aplicando migrações..."
# python manage.py migrate --noinput
echo "Banco de dados disponível. Aplicando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando o uWSGI..."
uwsgi --ini /app/uwsgi/uwsgi.ini