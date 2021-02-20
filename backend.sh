#!/bin/bash
export DEVICE_MANAGER_ENV_PRODUCTION=1
source .venv/bin/activate
gunicorn --workers=1 --error-logfile /var/log/device-manager/device-manager.log -k uvicorn.workers.UvicornWorker backend:app
#uvicorn --host=127.0.0.1 --port=8000 backend:app
