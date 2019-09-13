#!/bin/bash -xe

./scripts/lint.sh
poetry run pytest -s --cov=hypothesis_auto --cov=tests --cov-report=term-missing ${@} --cov-report html
