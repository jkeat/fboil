.PHONY: virtualenv

ENV = development
PYTEST_OPTIONS = -vv --exitfirst -n 8
VENV = config/$(ENV)/env
export PYTHONPATH := $(PYTHONPATH):.

# Run a local web server
server: $(VENV)
	. $(VENV)/bin/activate; python run.py

install: $(VENV)

config/%/env: config/%/requirements.txt
	virtualenv $@
	. $@/bin/activate && pip install --requirement $<

shell:
	python -i shell.py

test: $(VENV)
	. $(VENV)/bin/activate; py.test $(PYTEST_OPTIONS) tests/
