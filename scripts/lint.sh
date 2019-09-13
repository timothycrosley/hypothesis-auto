#!/bin/bash -xe

poetry run mypy --ignore-missing-imports hypothesis_auto/
poetry run isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=100 --recursive --check --diff --recursive hypothesis_auto/ tests/
poetry run black --check -l 100 hypothesis_auto/ tests/
poetry run flake8 hypothesis_auto/ tests/ --max-line 100 --ignore F403,F401,W503
poetry run safety check
poetry run bandit -r hypothesis_auto
