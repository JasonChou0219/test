#!/bin/bash
export DEVICE_MANAGER_ENV_PRODUCTION=1
source .venv/bin/activate
pipenv run python3 scheduler.py
