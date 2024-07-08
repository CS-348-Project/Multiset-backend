.PHONY: build up migrate seed down

# Build the Docker images
build:
	docker-compose build

# Start up all services defined in docker-compose.yml
up:
	docker-compose up -d postgres
	docker-compose up -d web pgadmin

# Start up the scheduler
scheduler:
	docker-compose up -d scheduler

# Apply Django migrations
migrate:
	docker-compose exec web python manage.py migrate

# Run the Django seed command
seed:
	docker-compose exec web python manage.py seed

# Shut down all services
down:
	docker-compose down

clean:
	docker-compose down --rmi all -v

# Shortcut for initialization for the first time
init: build up

# Shortcut to reinitialize
reinit: down build up

# Shortcut to initialize database
initdb: migrate seed