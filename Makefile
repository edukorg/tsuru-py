dependencies:
	@pip install -U pip
	@pip install pipenv --upgrade
	@pipenv install --dev --skip-lock

update:
	@pipenv clean
	@pipenv lock --clear
	@pipenv sync

test:
	@make check
	@make lint
	@make unit

check:
	@pipenv check

lint:
	@echo "Checking code style ..."
	@pipenv run pylint tsuru tests

unit:
	@echo "Running unit tests ..."
	ENV=test pipenv run pytest --cov=tsuru --cov-report xml

clean:
	@printf "Deleting dist files"
	@rm -rf dist .coverage build/ tsuru.egg-info/

publish:
	@make clean
	@printf "\nPublishing lib"
	@pipenv run python setup.py build sdist
	@pipenv run twine upload dist/*
	@make clean

setup:
	@pipenv run python setup.py develop

.PHONY: lint publish clean unit test dependencies setup
