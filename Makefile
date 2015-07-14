.PHONY: virtualenv

ENV = development
VENV = config/$(ENV)/env
export PYTHONPATH := $(PYTHONPATH):.

# Run a local web server
server: $(VENV)
	. $(VENV)/bin/activate; python run.py

foreman: $(VENV)
	. $(VENV)/bin/activate; foreman start

install: $(VENV)

database: $(VENV)
	source $(VENV)/bin/activate && python manage.py db init && python manage.py db migrate && python manage.py db upgrade

config/%/env: config/%/requirements.txt
	virtualenv $@
	. $@/bin/activate && pip install --requirement $<

shell:
	python -i shell.py

test: $(VENV)
	source $(VENV)/bin/activate && nosetests

coverage: $(VENV)
	source $(VENV)/bin/activate && nosetests --with-coverage --cover-package=app
