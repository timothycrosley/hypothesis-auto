#!/bin/bash -xe

poetry run isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=100 --recursive hypothesis_auto/ tests/
poetry run black hypothesis_auto tests/ -l 100
