lint:
	poetry run flake8 aton_test

dev:
	poetry run flask --app aton_test.app run --debug
