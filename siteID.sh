#!/bin/bash
echo 'Enter the name of your heroku app url (ex: my-app.herokuapp.com):'
read APP_NAME
DJANGO_SITEID=$(python3 ./siteID.py $APP_NAME)
sed -i "s/local_id = [0-9]\+/local_id = $DJANGO_SITEID/g" louslist/settings.py
