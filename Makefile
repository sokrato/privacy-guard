.PHONY: test install uninstall clean fmt publish

test:
	python -m pytest --cov-report html:htmlcov --cov=privacy_guard tests/

install:
	pip install -e .

uninstall:
	pip uninstall privacy_guide

clean:
	rm -rf htmlcov *.egg-info .coverage dist/

fmt:
	black src/ tests/

publish:
	rm -rf dist/
	hatch build
	hatch publish
