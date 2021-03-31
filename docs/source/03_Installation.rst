Installation
=============

This software depends on third-party software. At the time of this release, all third-party software is free-to use and
open-source. The respective version numbers are indicated. It cannot be guaranteed that this software will remain
compatible with future releases of these packages. Hence, we recommend installing the appropriate software version as
specified in this guide or as specified in the pipfile. The repository and this document will be updated to reflect
major version updates of third-party software.

Guide
------
Download
^^^^^^^^^^
Download the installation files using wget or download them directly from the `SiLA 2 manager repository website <https://gitlab.com/lukas.bromig/sila2_manager/-/tree/master>`_.
Extract the compressed *tar.gz* file using tar:

.. code-block:: console

    sudo wget https://gitlab.com/lukas.bromig/sila2_manager/-/archive/master/sila2_manager-master.tar.gz
    sudo tar -xvf sila2_manager-master.tar.gz

or clone the git repository with:

.. code-block:: console

    git clone https://gitlab.com/lukas.bromig/sila2_manager.git


Setting up the python environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This project requires python3.6 or higher. The latest python distribution can be downloaded `here <https://pypi.org/project/pipenv/>`_.

Before running any code in this project, all required python packages must be installed.
It is strongly recommended to set up a virtual environment. The project is shipped with a pipfile that contains
information on all required packages and their respective versions and dependencies.
To set up the python environment in the most user friendly way, *pipenv* is recommended.
*Pipenv* provides both, a virtual environment and the well known *pip* python package management.
If you want to install your virtual environment and manage your packages with pip separately,
feel free to use the supplied requirements.txt

1. Install pipenv

   To install the pipenv package visit the `pipenv project page <https://pypi.org/project/pipenv/>`_ for more installation options or run:

.. code-block:: console

    pip install pipenv

2. Install the project pipfile

   Move to the project main directory, where the pipfile and the pipfile.lock are located. Install the
   python packages and the virtual environment by running:

.. code-block:: console

   pipenv install

3. Entering the virtual environment

   Most IDE's support automatic detection of virtual environments and will start the console in this environment.
   For some IDE's this requires some manual changes in the settings menu.
   If no IDE is used you can enter the environment by entering the following code from the project main directory:

.. code-block:: console

   pipenv shell

4. [Windows only] Manual re-installation of protobuf

    The standard wheel installation of protobuf doesn't allow the use of multiple files with the same name in the same
    pool. All SiLA devices implement the standard features, thus every device will add a file with that feature name to
    the pool. The protobuf --no-binary installation is different to the pre-compiled wheel installation and allows
    multiple files with the same name in the pool. Run the *protobuf_no_binary_install.bat* in the main directory to
    replace the existing wheel installation. The issue is discussed in this thread in the
    `protobuf GitHub repository issue #3002 <https://github.com/protocolbuffers/protobuf/issues/3002>`_.

.. code-block:: console

   protobuf_no_binary_install.bat


Setting up the javascript run-time environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The frontend is written in typescript. A javascript run-time environment is needed to compile the code. It is recommended
to install *node.js*. To download *node.js* visit the `node.js download website <https://nodejs.org/en/download/>`_ (Windows) or install using *apt-get* (Linux):

.. code-block:: console

    sudo apt-get install nodejs


The *node.js* package manager *npm* can downloaded from the `npm download website <https://nodejs.org/en/>`_ (Windows) or using *apt-get*:

.. code-block:: console

   sudo apt-get install npm

The node.js packages can be installed by executing the following code from within the frontend directory:

.. code-block:: console

    cd frontend
    npm install

To compile the frontend files from source, move into the frontend directory and run:

.. code-block:: console

    cd frontend
    npm start

Installing docker
^^^^^^^^^^^^^^^^^^
Docker containers are used for the execution of experiments. Furthermore, they are used in the development version
for running the postgreSQL and the redis database. In the deployment version, these are replaced with a system wide installation.
You can download docker (v2.3.0.5) on the `docker website <https://www.docker.com/products/docker-desktop>`_ here.

1. Create the user-script docker image.

   You can modify the docker container that is used for experiments by changing the dockerfile in 'user_script_env'
   to include packages that you want to use in the scripting environment.To create the container run:

.. code-block:: console

   cd user_script_env
   docker build -t user_script

2. For the development version the containers for the postgrSQL and redis DB need to be downloaded:

.. code-block:: console

   docker run --name postgres -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 postgres
   docker run --name redis -d -p 6379:6379 redis

3. Once downloaded, the containers can be started:

.. code-block:: console

   docker start postgres
   docker start redis

4. Experiments are run in docker containers. The container can be customized. To create the container, run the *create_container_image* script* in the *user_script_env* folder:

.. code-block:: console

   cd user_script_env
   create_container_image.sh

You can modify the container image by editing the Dockerfile or by adding new python packages to the requirements.txt.

Setup of a development server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The development servers scan the code base and will restart if changes to the source code of the frontend or backend are detected.

1. Activate the development mode
    Run the following code from inside your pipenv environment (Linux):

.. code-block:: console

    export DEVICE_MANAGER_ENV_PRODUCTION=0


For Windows:
.. code-block:: console

    set DEVICE_MANAGER_ENV_PRODUCTION=0


2. Set up a test database

   A test database is created that includes pre-defined users, devices, scripts and experiments.
   Run the following code in your pipenv shell from the main directory:

.. code-block:: python

   python setup_test_db.py

2. Create a configuration file

   The configuration file specifies the secret key for the encryption between the frontend and the backend, as well as the database connection details for the postgreSQL database.
   To create the file run the supplied script 'generate_config.py' in your pipenv environment.

.. code-block:: python

   python generate_config.py

Starting the device manager in development mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To start the device manager in the development mode, the respective modules must be started individually.

1. Start the backend development server

   On Windows:

   .. code-block:: console

        ./run_backend_server.bat

   On Linux:

   .. code-block:: console

        ./run_backend_server.sh

2. Start the frontend server
    In a separate process run:

    .. code-block:: console

        cd frontend
        ng serve

3. Start the scheduler application.
    The scheduler application is responsible for the experiment execution using docker containers. In a new process run:

    .. code-block:: console

        python scheduler.py


Setup of a deployment server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This documentation will guide you through the installation process of the SiLA 2 Manager.
Server deployment is explained for systems running Ubuntu 12.04.

**First Install**

1. Install nginx
    To run the device manager web-service, *nginx* is required. *Nginx* is an open-source webserver-software. On Linux
    systems it can be installed using *apt* (Linux):

.. code-block:: console

    sudo apt install nginx

in this project *nginx* v.1.18.0 is used.

2. Install PostgreSQL
    `Download the PostgreSQL <https://www.postgresql.org/download/>`_ database and install it (Windows and others).
    PostgreSQL can also be installed using *apt* (Linux):

.. code-block:: console

    sudo apt install postgresql-12
    sudo apt install postgresql-client-12

In this project *postgreSQL* v.13 is used.

.. seealso::If the default port and password aren't used, make sure to update the config file generated by the *generate_config.py* script.

3. Install Docker
    Use the [official instructions](https://docs.docker.com/engine/install/ubuntu/)

4. Install Redis
    `Download the redis <https://redis.io/download>`_  in-memory database and install it. Redis can be installed using apt as well:

.. code-block:: console

    sudo apt install redis-server

In this project *redis v.6.0.9* is used.

5. Install supervisor

.. code-block:: console

    sudo apt install supervisor

6. Install and run pipenv

.. code-block:: console

    sudo apt install pipenv
    sudo mkdir .venv
    sudo pipenv sync

7. Fix protobuf installation
Uninstall protobuf and reinstall it using the --no-binary flag.

.. code-block:: console

    pipenv shell
    sudo pipenv uninstall protobuf

Check that protobuf has been uninstalled (Replace <usr> with your username!):

.. code-block:: console

    pip3 list
    sudo pip3 install --no-binary=:all: -t /home/<usr>/sila2_device_manager/.venv/lib/python3.8/site-packages protobuf==3.15.0
    [sudo pip3 install --no-binary=:all: protobuf==3.15.0]

Check that protobuf has been reinstalled.

8. Replace some files in the sila2lib of the virtual environment:

.. code-block:: console

    sudo pipenv run python3.8 replace_files.py

9. Install and enable nginx config

.. code-block:: console

    sudo cp server-config/device-manager.conf /etc/nginx/sites-available/
    sudo ln -s /etc/nginx/sites-available/device-manager.conf
    /etc/nginx/sites-enabled/device-manager.conf


10. Install supervisor config

.. code-block:: console

    sudo cp server-config/device-manager-backend.supervisor.conf /etc/supervisor/conf.d
    sudo cp server-config/device-manager-scheduler.supervisor.conf /etc/supervisor/conf.d

11. Create the device-manager user and group and add yourself

.. code-block:: console

    sudo adduser --system --no-create-home --group --ingroup docker device-manager
    sudo gpasswd -a your-user-name device-manager

12. Create www directory

.. code-block:: console

    sudo mkdir /var/www/html/device-manager-frontend
    chmod -R device-manager /var/www/html/device-manager-frontend
    chgrp -R device-manager /var/www/html/device-manager-frontend
    chmod -R 775 /var/www/html/device-manager-frontend

13. Create backend config directory

.. code-block:: console

    sudo mkdir /etc/device-manager/

14. Start and enable PostgreSQL

.. code-block:: console

    sudo systemctl enable postgresql.service
    sudo systemctl start postgresql.service

15. Set PostgreSQL password

.. code-block:: console

    sudo -u postgres psql postgres
    \password postgres
    <enter password>
    \q

Fill the database with some initial values and example/ test information:

.. code-block:: console

    python setup_db.py


16. Start and enable Docker

.. code-block:: console

    sudo systemctl enable docker.service
    sudo systemctl start docker.service

17. Enable and configure Redis
edit /etc/redis/redis.conf and change *supervised no* to *supervised systemd*

.. code-block:: console

    sudo systemctl enable redis.service
    sudo systemctl start redis.service

18. Create the user-script docker image

.. code-block:: console

    cd user_script_env
    sudo docker build -t user_script .
    cd ..

19. Deploy backend service

.. code-block:: console

    sudo pipenv run ./deploy_backend.sh

20. Edit Device-Manager Configuration File
The configuration files are located in the main directory under:

.. code-block:: console

    ./server-config/device-manager.conf
    ./server-config/device-manager-backend.supervisor.conf
    ./server-config/device-manager-scheduler.supervisor.conf

21. Build and install frontend

.. code-block:: console

    cd frontend
    sudo make
    sudo make install
    cd ..

22. Start and enable Nginx

.. code-block:: console

    sudo systemctl enable nginx.service
    sudo systemctl start nginx.service

23. Start and enable Supervisor

.. code-block:: console

    sudo systemctl enable supervisor.service
    sudo systemctl start supervisor.service

**Deploying new versions**
To deploy a new version its often enough to repeat step 19 and 21. Then restart nginx
and supervisor by using:

.. code-block:: console

    sudo systemctl restart nginx.service
    sudo systemctl restart supervisor.service

If you made changes to the PostgreSQL database entries, you need to delete old entries and setup a new one. Don't forget
to adjust the database setup script according to the changes made. Run the following code from within the root directory
of the repository/ your installation.

.. code-block:: console

        pipenv shell
        python3.8 delete_db.py
        python3.8 setup_db.py


**Server management**
You can use *supervisorctl* to manage the backend and scheduler processes separately.
The logs of the backend and the scheduler can be viewed under: */var/log/device-manager*.
The logs of the docker containers are located here: */$TEMPDIR/device-manager/container*
To restart the backend or the scheduler service, use *supervisorctl*. Enter *supervisorctl*:

.. code-block:: console

    sudo supervisorctl

and run the restart command for the respective service:

.. code-block:: console

    restart backend:device-manager-backend-0
    restart scheduler:device-manager-scheduler-0


**Important paths**
The most important paths are listed below. If you have trouble with the services, check out the log files! You have to
replace <your_username> with the username respective username you are using (Either your username or the username you created for
the SiLA Manager.

.. list-table:: Under Linux
   :widths: 50 50
   :header-rows: 1

   * - Content
     - File Path
   * - The installation directory of the SiLA 2 Manager
     - /home/<your_username>/sila2_device_manager
   * - The directory of the virtual environment
     - /home/<your_username>/sila2_device_manager/.venv
   * - The logs of the backend and scheduler service
     - /var/log/device-manager
   * - The logs of the supervisord service software
     - /var/log/supervisor
   * - The SiLA client files generated by the dynamic client
     - /tmp/device-manager/SiLA
   * - The container logs of the experiments
     - /tmp/device_manager/container


.. list-table:: Under Windows
   :widths: 50 50
   :header-rows: 1

   * - Content
     - File Path
   * - The directory of the virtual environment
     - <your_install_directory>\sila2_device_manager\.venv or C:\Users\<your_username>\.virtualenvs
   * - The logs of the backend and scheduler service
     - Todo: Add Windows equivalent for: /var/log/device-manager
   * - The SiLA client files generated by the dynamic client
     - C:\Users\<your_username>\AppData\Local\Temp\device-manager\SiLA
   * - The container logs of the experiments
     - C:\Users\<your_username>\AppData\Local\Temp\device-manager\container