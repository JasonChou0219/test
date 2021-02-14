#!/bin/sh
export DEVICE_MANAGER_ENV_PRODUCTION=1
pipenv run python3 scheduler.py
