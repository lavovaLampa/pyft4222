test-python39:
    just test-python 3.9

test-python310:
    just test-python 3.10

test-python311:
    just test-python 3.11

test-python312:
    just test-python 3.12

test-python313:
    just test-python 3.13

test-python314:
    just test-python 3.14

test-python VERSION:
    uv run --isolated --python={{VERSION}} pytest

test-all: test-python39 test-python310 test-python311 test-python312 test-python313 test-python314

test:
    uv run --isolated pytest

lint:
    ruff check

format:
    ruff format

type-check:
    uv run pyright

build:
    uv build

publish:
    uv publish

