VENV_DIR=venv

server:
	@. $(VENV_DIR)/bin/activate; cd src; python main.py

$(VENV_DIR)/bin/activate:
	@virtualenv $(VENV_DIR)

install: $(VENV_DIR)/bin/activate
	@. $(VENV_DIR)/bin/activate; pip install -r requirements.txt

tests: $(VENV_DIR)/bin/activate
	@. $(VENV_DIR)/bin/activate; cd src; nosetests tests/

clean:
	@rm -rf $(VENV_DIR)

clean-pyc:
	@ find . -name "*.pyc" -exec rm -rf {} \;

.PHONY: server console install clean clean-pyc
