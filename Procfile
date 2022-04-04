release: python manage.py migrate

web: gunicorn django_react.wsgi --log-file -

worker: celery -A app worker -l INFO -Q fast_queue -c 1
