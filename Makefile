PYTHON_VERSION=3.11.8
VENV_NAME=.venv

setup:
	pyenv install -s $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	python -m venv $(VENV_NAME)
	$(VENV_NAME)/bin/pip install --upgrade pip
	$(VENV_NAME)/bin/pip install -r requirements.txt
	@echo "✅ Setup completed."

run:
	PYTHONPATH=src $(VENV_NAME)/bin/python src/main.py