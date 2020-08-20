start: 
		docker-compose up -d

stop:
	docker-compose stop

build:
	docker-compose build web

pytest:
	docker-compose exec -T web pytest -v

migrate:
	docker-compose run --rm web python manage.py migrate

makemigrations:
	docker-compose run --rm web python manage.py makemigrations

createsuperuser: 
	docker-compose run --rm -e DJANGO_SUPERUSER_PASSWORD=root web python rubbish_collection_day_2_root/manage.py createsuperuser --username root --email root@example.com --noinput

black:
	docker run --rm -v /$$(pwd):/data cytopia/black ./rubbish_collection_day_2_root
