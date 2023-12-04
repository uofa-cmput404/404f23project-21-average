release: python manage.py migrate
web: gunicorn project.wsgi --log-file - --log-level debug
