start: 
		docker-compose up -d

stop:
	docker-compose stop

build:
	docker-compose build web

pytest:
	docker-compose exec -T web pytest -v

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser: 
	docker-compose exec -e DJANGO_SUPERUSER_PASSWORD=root web python manage.py createsuperuser --username root --email root@example.com --noinput

black:
	docker run --rm -v /$$(pwd):/data cytopia/black ./rubbish_collection_day_2_root
