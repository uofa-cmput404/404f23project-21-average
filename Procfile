release: python manage.py migrate
web: gunicorn mysite.wsgi --log-file - --log-level debug