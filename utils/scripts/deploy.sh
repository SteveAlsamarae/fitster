#! /bin/bash

. ./utils/envs/env.sh

function heroku_deploy(){
    # Description:
    #   Deploy the project to Heroku.
    #   This script will:
    #     - Create a new Heroku app.
    #     - Add the Heroku Postgres addon.
    #     - Set necessary environment variables.
    #     - Run makemigrations and migrate.
    #     - Create a superuser.
    #     - Push the code to Heroku.
    #     - Restart the app.

    heroku login
    echo -p "Enter the name of the Heroku app: "
    read app_name
    echo "Creating a new Heroku app..."
    heroku apps:create $app_name
    echo "Adding Heroku Postgres addon..."
    heroku addons:create heroku-postgresql:hobby-dev

    echo "Setting environment variables..."
    heroku config:set DEBUG=0
    echo "DEBUG is now turn off."
    heroku config:set SECRET_KEY=`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
    echo "Set SECRET_KEY environment variable."
    heroku config:set DISABLE_COLLECTSTATIC=1
    echo "DISABLE_COLLECTSTATIC is now turn off."

    echo "Setting SMTP environment variables..."
    heroku config:set EMAIL_HOST_USER=$EMAIL_HOST_USER
    heroku config:set EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD

    echo "Setting stripe environment variables........"
    heroku config:set STRIPE_LIVE_SECRET_KEY=$STRIPE_LIVE_SECRET_KEY
    heroku config:set STRIPE_TEST_SECRET_KEY=$STRIPE_TEST_SECRET_KEY
    heroku config:set STRIPE_PUBLIC_KEY=$STRIPE_PUBLIC_KEY
    heroku config:set DJSTRIPE_WEBHOOK_SECRET=$DJSTRIPE_WEBHOOK_SECRET
    heroku config:set STRIPE_LIVE_MODE=$STRIPE_LIVE_MODE
    heroku config:set DJSTRIPE_FOREIGN_KEY_TO_FIELD=id

    echo "Setting AWS S3 environment variables........"
    heroku config:set AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME
    heroku config:set AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
    heroku config:set AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
    heroku config:set AWS_S3_REGION_NAME=$AWS_S3_REGION_NAME

    echo "Pushing code to Heroku..."
    git push heroku master

    echo "Running makemigrations and migrate..."
    heroku run python manage.py makemigrations
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser

    echo "All done! Restarting app..."
    heroku scale web=1
    heroku restart
    echo "Congrats! Your app is now live at: https://$app_name.herokuapp.com"
}