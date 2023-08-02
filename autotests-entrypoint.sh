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

python manage.py test  