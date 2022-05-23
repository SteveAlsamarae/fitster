#! /bin/bash

function clean_mgs(){
    # Description:
    #   Clean the migrations files.
    #
    # Usage:
    #   ./clean_migrations_files.sh
    #
    # Example:
    #   ./clean_migrations_files.sh
    #
    # Returns:
    #   0 - Success
    #   1 - Failure
    #
    
    root_dir=$(pwd)
    
    find $root_dir -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find $root_dir -path "*/*/migrations/*.py" -not -name "__init__.py" -delete
    find $root_dir -path "*/migrations/*.pyc"  -delete
    find $root_dir -path "*/*/migrations/*.pyc"  -delete

    find $root_dir -path "*/db.sqlite3" -delete

    DJANGO_SUPERUSER_PASSWORD="admin"
    export DJANGO_SUPERUSER_PASSWORD


    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser --noinput --username admin --email admin@mail.com
}