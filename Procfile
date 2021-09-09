web: gunicorn config.wsgi
celery: celery -A config.celery worker --pool=solo -l info
