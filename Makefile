.PHONY: test install uninstall clean fmt publish build

test:
	python -m pytest --cov-report html:htmlcov --cov=ptk tests/

install:
	pip install -e .

uninstall:
	pip uninstall privacy_toolkit

clean:
	rm -rf htmlcov *.egg-info .coverage dist/

fmt:
	black src/ tests/

build:
	mkdir -p dist
	hatch build

publish: clean build
	hatch publish
