# SiLA2_Device_manager

Lamas/SiLA2_Device_Manager is an open-source framework for laboratory automation with a modern IoT interface. 
It provides the user with a device management system for SiLA devices, a scheduler and a scripting and experiment 
planning utility.

# Installation
Read the [docs](https://sila2-device-manager.readthedocs.io/en/latest/) for more detailed information.

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

6. Install and rund pipenv
`sudo apt install pipenv`
`mkdir .venv`
`pipenv sync`

7. Install and Enable Nginx Config
`sudo cp server-config/device-manager.conf /etc/nginx/sites-available/`
`sudo ln -s /etc/nginx/sites-available/device-manager.conf /etc/nginx/sites-enabled/device-manager.conf`

8. Install Supervisor Config
`sudo cp server-config/device-manager-backend.supervisor.conf /etc/supervisor/conf.d`
`sudo cp server-config/device-manager-scheduler.supervisor.conf /etc/supervisor/conf.d`

9. Create the device-manager user and group and add youself
`sudo adduser --system --no-create-home --group --ingroup docker device-manager`
`sudo gpasswd -a your-user-name device-manager`

10. Create www directory
`sudo mkdir /var/www/html/device-manager-frontend`
`chmod -R device-manager /var/www/html/device-manager-frontend`
`chgrp -R device-manager /var/www/html/device-manager-frontend`
`chmod -R 775 /var/www/html/device-manager-frontend`

11. Create Backend Config Directory
`sudo mkdir /etc/device-manager/`

12. Start and Enable PostgreSQL
`sudo systemctl enable postgresql.service`
`sudo systemctl start postgresql.service`

13. Set Postgres password
`sudo -u postgres psql postgres`
`\password postgres`
enter the password
`\q`

14. Start and Enable Docker
`sudo systemctl enable docker.service`
`sudo systemctl start docker.service`

15. Create the user-script docker image
`cd user_script_env`
`sudo docker build -t user_script .`

16. Deploy Backend
`sudo pipenv run ./deploy_backend.sh`

17. Edit Device-Manager Configuration File

18. Build and Install Frontend
`cd frontend`
`make`
`make install`

19. Start and Enable Nginx
`sudo systemctl enable nginx.service`
`sudo systemctl start nginx.service`

21. Start and Enable Supervisor
`sudo systemctl enable supervisor.service`
`sudo systemctl start supervisor.service`


### Deploying New Versions
To deploy a new version its often enough to repeate step 16 and 18.
Then restart nginx and supervisor by using `sudo systemctl restart nginx.service` and
`sudo systemctl restart supervisor.service`

You can use `supervisorctl` to manage the backend and scheduler processes seperately.
The logs can be viewed under /var/log/device-manager.

# License
This code is licensed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License)
