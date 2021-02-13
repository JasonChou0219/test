python replace_files.py
set DEVICE_MANAGER_ENV_PRODUCTION=0
uvicorn --reload --host=0.0.0.0 --port=5000 backend:app
