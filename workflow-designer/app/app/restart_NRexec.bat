docker stop noderedExec
docker rm noderedExec
docker volume rm node_red_exec_data
docker run -d -p 1337:1880 -v node_red_exec_data:/data --name workflow-executor nodered/node-red