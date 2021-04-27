docker start postgres
docker start redis
start "Backend" run_backend_server.bat
start "Scheduler" python scheduler.py
start "Frontend" /d frontend npm start
