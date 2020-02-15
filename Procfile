release: python manage.py migrate --noinput
release: python manage.py collectstatic --noinput
release: python manage.py migrate --noinput
release: python manage.py migrate
web: gunicorn conf.wsgi