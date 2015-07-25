.PHONY: install server foreman database shell test coverage

install:
	virtualenv env
	source env/bin/activate && \
	pip install -r requirements.txt

server:
	python run.py

foreman:
	foreman start -f Procfile.dev

database:
	python manage.py db init && \
	python manage.py db migrate && \
	python manage.py db upgrade

shell:
	python -i shell.py

test:
	nosetests

coverage:
	nosetests --with-coverage --cover-package=app
