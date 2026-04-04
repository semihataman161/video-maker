PYTHON_VERSION=3.11.8
VENV_NAME=.venv

create_env:
	pyenv install -s $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	python -m venv $(VENV_NAME)
	$(VENV_NAME)/bin/pip install --upgrade pip
	$(VENV_NAME)/bin/pip install -r requirements.txt
	@echo "✅ Environment created and dependencies installed."

delete_env:
	rm -rf $(VENV_NAME)
	pip cache purge
	@echo "🗑️ Virtual environment deleted."

run:
	PYTHONPATH=. $(VENV_NAME)/bin/python -m src.main