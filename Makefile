# Makefile
install:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
	poetry install

run:
	nohup poetry run python3 magnit_test/app.py >./magnit_test.log 2>./err.log &

format:
	black magnit_test
	isort magnit_test

check:
	pylint magnit_test
	mypy magnit_test

test:
	pytest --cov=magnit_test

.PHONY: test