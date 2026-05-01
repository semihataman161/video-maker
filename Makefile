PYTHON_VERSION=3.11.8
VENV_NAME=.venv

activate_venv:
	@echo "Run this command to activate:"
	@echo "source $(VENV_NAME)/bin/activate"

create_venv:
	pyenv install -s $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	pyenv exec python -m venv $(VENV_NAME)
	$(VENV_NAME)/bin/pip install --upgrade pip
	$(VENV_NAME)/bin/pip install -r requirements.txt
	@echo "✅ Environment created and dependencies installed."

delete_venv:
	rm -rf $(VENV_NAME)
	pip cache purge
	@echo "🗑️ Virtual environment deleted."

run:
	PYTHONPATH=. $(VENV_NAME)/bin/python -m src.main