Installation
=============

This software depends on third-party software. At the time of this release, all third-party software is free-to use and open-source. The respective version numbers are indicated. It cannot be guaranteed that this software will remain compatible with future releases. The repository and this document will be updated to reflect major version updates of third-party software.

Prerequisites
----------------
Hardware:

Software:

Guide
------


Setting up the python environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This project requires python3.6 or higher. The latest python distribution can be downloaded `here <https://pypi.org/project/pipenv/>`_.

Before running any code in this project, all required python packages must be installed.
It is strongly recommended to set up virtual environment. The project is shipped with a pipfile that contains
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
   For some IDE's this requires some changes in the settings menu.
   If no IDE is used you can enter the environment by entering the following code from the project main directory:

.. code-block:: console

   pipenv shell

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
You can download docker on the `docker website <https://www.docker.com/products/docker-desktop>`_ here.

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

Setup of a development server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The development servers scan the code base and will restart if changes to the source code of the frontend or backend are detected.

1. Set up a test database

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

4. Start the data-handler application
    If the data-handler is used, this application must be started. The data-handler application records the data of
    devices that are used in active experiments. In a new process run:

    .. code-block:: console

        python data_handler.py

Setup of a deployment server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To run the device manager web-service, *nginx* is required. *Nginx* is an open-source webserver-software. To install the
software on windows, download it from their `nginx website <http://nginx.org/en/download.html>`_, extract and install. On Linux
systems it can be installed using *apt* (Linux):

.. code-block:: console

    sudo apt install nginx

in this project *nginx* v.1.18.0 is used.

`Download the PostgreSQL <https://www.postgresql.org/download/>`_ database and install it (Windows and others).
PostgreSQL can also be installed using *apt* (Linux):

.. code-block:: console

    sudo apt install postgresql

In this project *postgreSQL* v.13 is used.

.. seealso::If the default port and password aren't used, make sure to update the config file generated by the *generate_config.py* script.

`Download the redis <https://redis.io/download>`_  in-memory database and install it. Redis can be installed using apt as well:

.. code-block:: console

    sudo apt install redis-server

To install the redis server on windows, follow this `guide-for-redis-on-windows <https://redislabs.com/ebook/appendix-a/a-3-installing-on-windows/a-3-2-installing-redis-on-window/>`_.
In this project *redis v.6.0.9* is used.
