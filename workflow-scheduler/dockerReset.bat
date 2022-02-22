docker rm sila2_manager-workflow-scheduler-1 -f
docker rmi gitlab.com/lukas.bromig/sila2_manager/workflow-scheduler
cd..
docker-compose up -d workflow-scheduler
docker-compose logs workflow-scheduler