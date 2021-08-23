# SiLA_2_Manager

The SiLA_2_Manager is an open-source framework for laboratory automation with a modern IoT interface. 
It provides the user with a SiLA service management system, a scheduler, a scripting environment, a experiment 
planning utility, and a data handler to link service data to a database.

# Installation
Read the [docs](https://sila2-manager.readthedocs.io/en/latest/) for more detailed information.  

# Compatibility
The SiLA Manager is compatible with the [SiLA2 Python](https://gitlab.com/SiLA2/sila_python) repository and all SiLA 
servers generated with it. Follow the instructions in the SiLA2 Python repository to create your own SiLA servers or use 
the provided examples (HelloSiLA) to test the SiLA 2 Manager. You can also install the SiLA2 python 
[library](https://pypi.org/project/sila2lib/) and [codegenerator](https://pypi.org/project/sila2codegenerator/) from 
pypi using  pip. The other SiLA 2 repositories (like C# and Tecan) will be supported very soon.  

## Development Environment

### Setting up the python environment
1. Install pipenv  
Visit: `https://pypi.org/project/pipenv/`  
or try using `pip install pipenv`

2. Install the project pipfile  
Move to the project main directory, where the pipfile is located  
Run: `pipenv install`   
This will install all required python packages in a virtual environment.  

3. Entering the virtual environment  
Most IDE's support automatic detection of virtual environments and will start the console in this environment. 
For some IDE's this requires some changes in the settings menu.  
If no IDE is used you can enter the environment by entering: `pipenv shell`

### Generating the documentation
This README contains the bare essentials to get the device manager up and running. For a more detailed description and 
further information read the documentation. The documentation can be generated using sphinx.
1. Run the following command from within the docs folder  
To generate a pdf (Perl and latexmk required):
`make latexpdf`  
To generate a html-file
`make html`

2. The file will be stored in the _build folder inside the docs folder

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

4. Activate development mode
`export DEVICE_MANAGER_ENV_PRODUCTION=0` or 
`set DEVICE_MANAGER_ENV_PRODUCTION=0` 
if you are on windows 

5. Setup a test database:  
Run `python setup_db.py` from inside your pipenv environment.

6. Create Config File:  
Run `python generate_config.py` from inside your pipenv environment.

7. Create the docker container for the experiment execution environment
Run `create_container_image.sh` which is located in the folder usr_script_env.


### Starting the Backend development Server

#### Linux
Run `./run_backend_server.sh` from inside your pipenv environment.

#### Windows
Run `./run_backend_server.bat` from inside your pipenv environment.

## Server Deployment on Ubuntu 12.04

### First Install

1. Install nginx
On ubuntu this can be installed with apt  
`sudo apt install nginx`  

2. Install PostgreSQL  
`sudo apt install postgresql-12`  
`sudo apt install postgresql-client-12`  

3. Install Docker  
Use the [official instructions](https://docs.docker.com/engine/install/ubuntu/) 

4. Install Supervisor  
`sudo apt install supervisor`  

5. Install Redis
`sudo apt install redis-server`

6. Install and run pipenv  
`sudo apt install pipenv`  
`mkdir .venv`  
`pipenv sync`  

7. Fix protobuf installation  
Uninstall protobuf and reinstall it using the --no-binary flag.    
`pipenv shell`  
`sudo pip3 uninstall protobuf`  
Check that protobuf has been uninstalled:  
`pip3 list`  
`sudo pip3 install --no-binary=:all: -t $/home/<usr>/sila2_device_manager/.venv/lib/python3.8/site-packages protobuf==3.15.0`    
Check that protobuf has been reinstalled.  

8. Replace some files in the sila2lib of the virtual environment  
`sudo pipenv run python3.8 replace_files.py`  

9. Install and Enable Nginx Config  
`sudo cp server-config/device-manager.conf /etc/nginx/sites-available/`  
`sudo ln -s /etc/nginx/sites-available/device-manager.conf /etc/nginx/sites-enabled/device-manager.conf`  

10. Install Supervisor Config  
`sudo cp server-config/device-manager-backend.supervisor.conf /etc/supervisor/conf.d`  
`sudo cp server-config/device-manager-scheduler.supervisor.conf /etc/supervisor/conf.d`  

11. Create the device-manager user and group and add yourself  
`sudo adduser --system --no-create-home --group --ingroup docker device-manager`  
`sudo gpasswd -a your-user-name device-manager`  

12. Create www directory  
`sudo mkdir /var/www/html/device-manager-frontend`  
`chmod -R device-manager /var/www/html/device-manager-frontend`  
`chgrp -R device-manager /var/www/html/device-manager-frontend`  
`chmod -R 775 /var/www/html/device-manager-frontend`  

13. Create Backend Config Directory  
`sudo mkdir /etc/device-manager/`  

14. Start and Enable PostgreSQL  
`sudo systemctl enable postgresql.service`  
`sudo systemctl start postgresql.service`  

    Fill the database with the initial values and examples  
    `pipenv run python setup_db.py`

15. Set Postgres password  
`sudo -u postgres psql postgres`  
`\password postgres`  
enter the password  
`\q`  

16. Start and Enable Docker  
`sudo systemctl enable docker.service`  
`sudo systemctl start docker.service`  

17. Enable and configure Redis  
edit /etc/redis/redis.conf and change   
`supervised no` to `supervised systemd`  
`sudo systemctl enable redis.service`  
`sudo systemctl start redis.service`  

18. Create the user-script docker image  
`cd user_script_env`  
`sudo docker build -t user_script .`  
`cd ..`

19. Deploy Backend  
`sudo pipenv run ./deploy_backend.sh`  

20. Edit Device-Manager Configuration File  
The configuration files are located in the main directory under:  
    `./server-config/device-manager.conf`  
    `./server-config/device-manager-backend.supervisor.conf`    
    `./server-config/device-manager-scheduler.supervisor.conf`  
      
21. Build and Install Frontend  
`cd frontend`  
`sudo make`  
`sudo make install`  

22. Start and Enable Nginx  
`sudo systemctl enable nginx.service`  
`sudo systemctl start nginx.service`  

23. Start and Enable Supervisor  
`sudo systemctl enable supervisor.service`  
`sudo systemctl start supervisor.service`  


### Deploying New Versions
To deploy a new version its often enough to repeate step 17 and 19.
Then restart nginx and supervisor by using  
`sudo systemctl restart nginx.service`  
and  
`sudo systemctl restart supervisor.service`  

### Server management
You can use `supervisorctl` to manage the backend and scheduler processes separately.
The logs can be viewed under /var/log/device-manager.  
To restart the backend or the scheduler service, use supervisorctl. Enter supervisorctl:  
`sudo supervisorctl`   
and run the restart command for the respective service:  
`restart backend:device-manager-backend-0`  


# License
This code is licensed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License)
