.PHONY: runserver
runserver:
	poetry run python -m flask --app morse_api run --port 8000 --debug
