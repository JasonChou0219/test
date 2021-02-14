#!/bin/sh
export DEVICE_MANAGER_ENV_PRODUCTION=1
pipenv run python3 replace_files.py
pipenv run uvicorn --host=0.0.0.0 --port=5000 backend:app  
