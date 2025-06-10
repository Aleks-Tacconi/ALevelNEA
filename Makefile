ifeq ($(OS), Windows_NT)
install: poetry.lock pyproject.toml
	poetry install --no-root

run: src/main.py
	poetry run python src/main.py
else
install: poetry.lock pyproject.toml
	poetry install --no-root

run: src/main.py 
	xhost +SI:localuser:root
	poetry run sudo python src/main.py
endif
