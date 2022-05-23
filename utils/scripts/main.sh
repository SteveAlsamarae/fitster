#! /bin/bash
#
# To use these aliases, source this file:.
# RUN: source ./utils/scripts/main.sh
# 

. ./utils/scripts/migrate_n_run.sh
. ./utils/scripts/clean_migrations_files.sh
. ./utils/scripts/clean_media.sh

alias mmg="python manage.py makemigrations"
alias mg="python manage.py migrate"
alias run="python manage.py runserver"
alias shell="python manage.py shell"
alias suser="python manage.py createsuperuser"
alias dbs="python manage.py dbshell"
alias createapp="python manage.py startapp"
alias mrun="mgrun"
alias mclean="clean_mgs"
alias cmedia="clean_media"
alias env="python ./utils/scripts/autoenv.py"
