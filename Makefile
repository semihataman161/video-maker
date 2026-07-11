PYTHON_VERSION=3.11.8

VENV_MAIN=.venv-main
VENV_IMAGE=.venv-image

activate_venv_main:
	@echo "Run this command to activate main environment:"
	@echo "source $(VENV_MAIN)/bin/activate"

activate_venv_image:
	@echo "Run this command to activate image environment:"
	@echo "source $(VENV_IMAGE)/bin/activate"

activate_venvs: activate_venv_main activate_venv_image

create_venv_main:
	pyenv install -s $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	pyenv exec python -m venv $(VENV_MAIN)
	$(VENV_MAIN)/bin/pip install --upgrade pip
	$(VENV_MAIN)/bin/pip install -r requirements-main.txt
	@echo "✅ Main environment created and dependencies installed."

create_venv_image:
	pyenv install -s $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	pyenv exec python -m venv $(VENV_IMAGE)
	$(VENV_IMAGE)/bin/pip install --upgrade pip
	$(VENV_IMAGE)/bin/pip install -r requirements-image.txt
	@echo "✅ Image environment created and dependencies installed."

create_venvs: create_venv_main create_venv_image

delete_venvs:
	rm -rf $(VENV_MAIN) $(VENV_IMAGE)
	pip cache purge
	@echo "🗑️ Virtual environments deleted."

run-audio:
	PYTHONPATH=. $(VENV_MAIN)/bin/python -m src.main audio

run-srt:
	PYTHONPATH=. $(VENV_MAIN)/bin/python -m src.main srt

run-images:
	PYTHONPATH=. $(VENV_IMAGE)/bin/python -m src.main images

run-video:
	PYTHONPATH=. $(VENV_MAIN)/bin/python -m src.main video

run-thumbnails:
	PYTHONPATH=. $(VENV_IMAGE)/bin/python -m src.main thumbnails

run-text-on-thumbnails:
	PYTHONPATH=. $(VENV_IMAGE)/bin/python -m src.main text-on-thumbnails

run:
	$(MAKE) run-audio
	$(MAKE) run-srt
	$(MAKE) run-images
	$(MAKE) run-video