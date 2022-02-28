
# install "power-hello"
install:
	pip3 install -e .

# uninstall "power-hello"
uninstall:
	pip3 uninstall power-hello

test:
	python3 -m mypy power_hello

# create virtual environment
venv:
	python3 -m venv .venv

# install for development(at venv)
dev-install:
	pip install -r requirements.txt
