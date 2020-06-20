SHELL := /bin/bash

init:
	@pip install -r requirements.txt

lint:
	flake8 mock8s/
	black --line-length 79 --check mock8s/

test: lint

