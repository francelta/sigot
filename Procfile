web: daphne -b 0.0.0.0 -p $PORT sigot.boot.asgi:application
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput


