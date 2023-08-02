#!/bin/bash

until cd /code/src
do
    echo "Вход в директорию проекта"
done

python manage.py makemigrations

until python manage.py migrate
do 
    echo "Migrations db applying"
    sleep 2
done
 
python manage.py create_superuser_from_settings
python manage.py runserver 0.0.0.0:8000