#!/bin/sh
export DEVICE_MANAGER_ENV_PRODUCTION=1
pipenv run python3 replace_files.py
pipenv run gunicorn -k uvicorn.workers.UvicornWorker backend:app
