python manage.py makemigrations
python manage.py migrate
export DEBUG=True
# gunicorn conf.wsgi:application --workers 3
python manage.py runserver
