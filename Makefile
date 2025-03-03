.PHONY: runserver

runserver:
	@while true; do \
		echo "Starting Django server..."; \
		python backend/manage.py runserver || echo "Server crashed. Restarting..."; \
		sleep 2; \
	done


makemigrations:
	python backend/manage.py makemigrations

migrate:
	python backend/manage.py migrate

createsuperuser:
	python backend/manage.py createsuperuser

shell:
	python backend/manage.py shell

generate_schema:
	python backend/manage.py spectacular --color --file schema.yml