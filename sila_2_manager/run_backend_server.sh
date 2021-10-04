#!/bin/bash

export DEVICE_MANAGER_ENV_PRODUCTION=0
python3 replace_files.py
uvicorn --reload --host=0.0.0.0 --port=5000 backend:app  
