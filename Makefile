.PHONY: test

test:
	coverage run -m pytest -s -vv
	coverage report
	coveralls