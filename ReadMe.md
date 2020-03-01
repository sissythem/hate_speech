## Datasets

1) german.csv --> https://github.com/UCSM-DUE/IWG_hatespeech_public
2) fox_news.json --> https://github.com/sjtuprog/fox-news-comments/blob/master/full-comments-u.json
3) CONAN.json --> https://github.com/marcoguerini/CONAN
4) hate-speech-dataset/annotations_metadata.csv
   hate-speech-dataset/all_files/               ==>  https://github.com/aitor-garcia-p/hate-speech-dataset

## Update db

1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py migrate --run-syncdb
4. python manage.py createsuperuser
5. python manage.py runserver 
6. python manage.py generateschema > openapi-schema.yml
7. export DJANGO_SETTINGS_MODULE=exec_registry.settings
8. python manage.py collectstatic   

## Generating an OpenAPI Schema

* pip install pyyaml
* ./manage.py generateschema > openapi-schema.yml

## Docker

docker-compose build
docker-compose up -d