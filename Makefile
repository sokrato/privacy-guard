.PHONY: test install clean fmt

test:
	python -m pytest --cov-report html:htmlcov --cov=hide tests/

install:
	pip install -e .

clean:
	rm -rf htmlcov *.egg-info .coverage dist/

fmt:
	black hide/ tests/

publish:
	hatch build
	hatch publish
