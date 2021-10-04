#!/bin/bash
export DEVICE_MANAGER_ENV_PRODUCTION=0
python3 generate_config.py
python3 setup_db.py
