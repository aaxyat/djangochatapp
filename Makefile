.PHONY: runserver

runserver:
	@while true; do \
		echo "Starting Django server..."; \
		uv run python backend/manage.py runserver || echo "Server crashed. Restarting..."; \
		sleep 2; \
	done


makemigrations:
	uv run python backend/manage.py makemigrations

migrate:
	uv run python backend/manage.py migrate

createsuperuser:
	python backend/manage.py createsuperuser

shell:
	python backend/manage.py shell

generate_schema:
	python backend/manage.py spectacular --color --file schema.yml