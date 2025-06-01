.PHONY: test install uninstall clean fmt publish build

test:
	# python -m pytest --cov-report html:htmlcov --cov=ptk tests/
	uv run pytest -s --cov=ptk --cov-report html:htmlcov tests

install:
	pip install -e .

uninstall:
	pip uninstall privacy_toolkit

clean:
	rm -rf htmlcov *.egg-info .coverage dist/

fmt:
	# black src/ tests/
	uv run black src/ tests

lint:
	uv run ruff check --fix src tests

build:
	# mkdir -p dist && hatch build
	uv build

publish: clean build
	# hatch publish
	# uv pip install hatch first
	uv publish
