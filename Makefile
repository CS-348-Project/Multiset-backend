.PHONY: build up migrate seed down

# Build the Docker images
build:
	docker-compose build

# Start up all services defined in docker-compose.yml
up:
	docker-compose up -d

# Apply Django migrations
migrate:
	docker-compose exec web python manage.py migrate

# Run the Django seed command
seed:
	docker-compose exec web python manage.py seed

# Shut down all services
down:
	docker-compose down

# Shortcut for full initialization (build, start, migrate, seed)
init: build up migrate seed

# Shortcut to reinitialize everything (shutdown, rebuild and restart)
reinit: down build up migrate seed