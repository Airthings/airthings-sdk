.PHONY: install generate lint format check

install:
	poetry install

generate:
	cd .. && openapi-python-client generate \
		--path python/openapi.yaml \
		--config python/config.yaml \
		--meta none \
		--overwrite \
		--output-path python
	rm -rf api/ models/ __pycache__/
	rm -f __init__.py client.py errors.py types.py py.typed
	git checkout -- airthings_sdk/ examples/

lint:
	poetry run black --check airthings_sdk examples
	poetry run pylint airthings_sdk examples
	poetry run mypy airthings_sdk examples

format:
	poetry run black airthings_sdk examples

check: format lint
