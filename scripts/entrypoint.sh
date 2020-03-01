#!/bin/bash

port=8000
exec_path=/hate_speech

# Registry db initializations

until python $exec_path/manage.py makemigrations > /dev/null 2>&1 ;do
      echo "Waiting mysql docker to setup........"
      sleep 1
done

echo "Initializing....."
python $exec_path/manage.py makemigrations
python $exec_path/manage.py migrate
python $exec_path/manage.py migrate --run-syncdb

# Create superuser from localsettings
username="root"
password="root"

email=$username"@example.com"

echo "Creating super user....."

echo "from django.contrib.auth.models import User; User.objects.create_superuser('$username', '$email', '$password')" | python $exec_path/manage.py shell

echo "Starting web server...."

rm -rf $exec_path/resources/old_datasets/
rm -rf $exec_path/resources/embeddings/

# python $exec_path/manage.py runserver 0.0.0.0:$port
exec gunicorn  -w 9 -b 0.0.0.0:$port hate_speech.wsgi \
		--log-level debug \
                --backlog 0 \
                --timeout 120
