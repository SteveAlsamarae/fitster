#! /bin/bash

function mgrun() {
    # Description:
    #   Migrate the database and run the application.
    #
    # Usage:
    #   ./migrate_n_run.sh
    #
    # Example:
    #   ./migrate_n_run.sh
    #
    # Returns:
    #   0 - Success
    #   1 - Failure
    #

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
}