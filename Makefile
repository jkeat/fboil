.PHONY: virtualenv

VENV = config/env
export PYTHONPATH := $(PYTHONPATH):.

config/env: requirements.txt
	virtualenv $@
	. $@/bin/activate && pip install --requirement $<\

install: $(VENV)

server: $(VENV)
	. $(VENV)/bin/activate; python run.py

foreman: $(VENV)
	. $(VENV)/bin/activate && \
	foreman start -f Procfile.dev

database: $(VENV)
	source $(VENV)/bin/activate && \
	python manage.py db init && \
	python manage.py db migrate && \
	python manage.py db upgrade

shell:
	python -i shell.py

test: $(VENV)
	source $(VENV)/bin/activate && \
	nosetests

coverage: $(VENV)
	source $(VENV)/bin/activate && \
	nosetests --with-coverage --cover-package=app
