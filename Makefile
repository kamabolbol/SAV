.PHONY: up down logs ollama restart status clean

up:
	cd docker && docker compose up -d

down:
	cd docker && docker compose down

logs:
	cd docker && docker compose logs -f

ollama:
	cd docker && ./init-ollama.sh

restart:
	cd docker && docker compose restart

status:
	cd docker && docker compose ps

clean:
	cd docker && docker compose down -v
