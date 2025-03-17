# Makefile for LangChain Content Generator

VENV_NAME=lng-env

# Create virtual environment
setup:
	python -m venv $(VENV_NAME)

# Activate venv and install dependencies
install:
	. $(VENV_NAME)/bin/activate && pip install -r requirements.txt

# Run the app
run:
	. $(VENV_NAME)/bin/activate && python app.py

# Freeze deps
freeze:
	. $(VENV_NAME)/bin/activate && pip freeze > requirements.txt

# Remove the virtual environment
clean:
	rm -rf $(VENV_NAME)