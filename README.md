# SiLA2_Device_manager

Lamas/SiLA2_Device_Manager is an open-source framework for laboratory automation with a modern IoT interface. It provides the user with a device management system for SiLA devices, a scheduler and a scripting and experiment planning utility.


## Device Manager

### Setup
1. Install Docker (v2.3.0.5)  
Visit `https://www.docker.com/products/docker-desktop`   

2. Download and start the images of PostgreSQL and redis: 
Run `docker run --name postgres -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 postgres`  
Run `docker run --name redis -d -p 6379:6379 redis`
The next time you want use the containers you can start them directly: 
`docker start postgres`
`docker start redis`
	
3. Create the user-script docker image
`cd user_script_env`
`docker build -t user_script .`

4. Setup a test database:  
Run `python setup_test_db.py` from inside your pipenv enviroment.


### Starting the Backend development Server

#### Linux
Run `./run_backend_server.sh` from inside your pipenv enviroment.

#### Windows
Run `./run_backend_server.bat` from inside your pipenv enviroment.

