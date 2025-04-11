full-rebuild:
	docker compose down --volumes && docker compose -f docker-compose.yaml up --build -d
reload-nginx:
	docker compose exec nginx nginx -s reload
dev:
	docker compose -f docker-compose.dev.yaml up -d