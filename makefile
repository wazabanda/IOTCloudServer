migrations:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

run-local:
	python manage.py runserver 0.0.0.0:8000

daphne:
	daphne -b 0.0.0.0 -p 8000 IOTCloudServer.asgi:application --verbosity 2
# daphne -b 0.0.0.0 -p 8000 IOTCloudServer.asgi:application

collectstatic:
	python manage.py collectstatic

watch-flowbite:
	npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
