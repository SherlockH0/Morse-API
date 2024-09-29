.PHONY: install 
install:
	poetry install

.PHONY: shell 
shell:
	poetry run python -m morse_api.manage shell

.PHONY: migrate
migrate: 
	poetry run python -m morse_api.manage migrate

.PHONY: migrations 
migrations: 
	poetry run python -m morse_api.manage makemigrations
	
.PHONY: runserver
runserver:
	poetry run python -m morse_api.manage runserver

.PHONY: superuser
superuser:
	poetry run python -m morse_api.manage createsuperuser

.PHONY: update
update: install migrate ;
