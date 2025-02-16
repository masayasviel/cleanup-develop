up:
	docker-compose up -d

down:
	docker-compose down

down_volume:
	docker-compose down -v

venv:
	python3 -m venv .venv
	. .venv/bin/activate
	.venv/bin/pip install -r requirements.txt
