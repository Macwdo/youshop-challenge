run:
	@echo Starting application attached from terminal 🟢
	docker compose down
	docker compose up

up:
	@echo Starting application deattached from terminal 🟢
	docker compose down
	docker compose up -d

down:
	@echo Stopping application 🛑
	docker compose down
	docker compose up -d

attach:
	@echo Attaching in application 📦
	docker attach youshop_djangoapp

admin:
	@echo Creating admin user 👨💻
	docker exec -it youshop_djangoapp python manage.py createsuperuser

tests:
	@echo Running tests 🧪
	docker exec -it youshop_djangoapp python manage.py test

load_data:
	@echo Loading data 📦
	docker exec -i youshop_djangoapp sh -c 'python manage.py loaddata */fixtures/*.json'
