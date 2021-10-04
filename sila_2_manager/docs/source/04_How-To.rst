How-To
=========

Connecting to the SiLA 2 Manager
-----------------------------------

If your device manager server is running on your local machine or on a computer within your network, you can
connect to the frontend from any internet capable device with a modern browser. Simply connect using one of the
following URLs:

If the server is running locally:

    `localhost:4200 <http://localhost:4200>`_ or `127.0.0.1:4200 <http://127.0.0.1:4200>`_

If the server is running on another computer within your network:

    <host-server-ip\>:4200

Login page
-------------

The log-in view is a security feature, that ensures that only registered users have access to the services in your
network. The Open Authorization protocol 2 (OAuth2) is used to secure communication between the backend and frontend.
Once logged-in, you can add new users, delete users and reset passwords. The device manager frontend uses the Angular
Authentication tool (AuthInterceptor) which relies on a HttpInterceptor interface to grant access to permitted users.
If accessed from the host machine, the url of the login-page is `<localhost:4200/login>`_. The default username is
**admin** and the default password is **1234**. It is strongly recommended to change the default password of the admin
account.

.. image:: _static/figures/login.png
    :width: 800
    :alt: A view of the login page with entered admin credentials


Main page - Services
---------------------
The devices page is the SiLA 2 Managers main view. Registered services are listed here and some useful detail is provided
on first sight. This includes the services server name, address, port. Furthermore, the connection status is indicated.
In a future version other devices types than SiLA 2, such as offline devices, custom device or OPC-UA types could be supported.
The software structure allows for such adaptations.
Several buttons allow the user to expand the visible detail of the service, change its current name, or
remove the service from the SiLA 2 Manager.

Clicking on the service name or the information icon expands the view of the selected
service, showing the implemented features and the respective descriptions. Each feature can be expanded even further to
investigate which (observable) commands and (observable) properties are implemented by the feature. Exploring individual
commands and properties shows the user useful information on functionality and usage. Required parameters and responses
are displayed with the attributed SiLA-datatype.

.. image:: _static/figures/services.png
    :width: 800
    :alt: A view of the main page, the service list, including general service details

.. note::
    In this documentation and the code base the word SiLA Device and SiLA Service are often used unanimously. However,
    a SiLA Device is just a special case of a SiLA Service. Both are always special implementations of a SiLA Server.
    A SiLA Server can implement a broad variety of soft- and hardware, such as laboratory device, virtual machines,
    software solution or API wrappers.


Service discovery
^^^^^^^^^^^^^^^^^^
The SiLA 2 Manager uses the SiLA 2 auto-discovery functionality which relies on multicast DNS service discovery
(`zeroconf <https://pypi.org/project/zeroconf/>`_) to register its services in
the network. New services can be added by clicking the "plus"-button on the top right of the service table. Service
discovery is started from within a new pop-up window. The discovery mode scans for SiLA 2 services in the network and displays the
basic information it was registered with by the server. This information is used to connect to the server using a
dynamic SiLA 2 python client. The client files are stored in the local temporary folder named after the services server-UUID:
Relative path to the directory: *[...]temp/device-manager/SiLA/<device-UUID>/*

.. image:: _static/figures/discovery.png
    :width: 800
    :alt: A view of the discovery feature for adding new services to the manager

SiLA Explorer - The service tree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Each service that is added to the SiLA 2 Manager is assigned an internal UUID. This way services with the same server
name can be uniquely identified. The service tree enables the user to run commands and request properties interactively
from within the browser. On the lowest level of the service tree, the command/property level, a run button can be clicked
to execute the function. For functions that require user input, the parameters can be entered in the corresponding text
box. The syntax by which the call can be incorporated into python scripts in the scripting environment is shown.

.. image:: _static/figures/service-tree.png
    :width: 800
    :alt: A view of the discovery feature for adding new services to the SiLA 2 Manager

The data handler
------------------
`InfluxDB <https://portal.influxdata.com/downloads/>`_ databases can be registered and linked to a service. InfluxDB is a time-series
database that is well suited for experimental data. To be able to use this feature, an InfluxDB server must be running
within your network. Providing the connection details to the SiLA 2 Manager is sufficient. A username and password can
be added optionally for additional security. A registered database can be linked to a service to setup automatic data
transfer. Data transfer is started as soon as the booking of a service commences, i.e. the experiment the service is
used in is started. The database-service link can be deleted by selecting the empty database in the dropdown menu.

The data handler will execute the configured calls in the user-specified polling intervals and
store the responses in the linked database with experiment name, service name, and user name as tags. To activate the data
acquisition for a selected service, the "active"-checkbox must be ticked. If responses of certain functions, or features
all together, should not be stored, further checkboxes can be found on the lower levels of the service tree to deactivate
data transfer. This is crucial to disable the execution of set commands for example.

Most types of data can be classified as either meta-data or measurement data. Typically, meta-data doesn't need to be
queried on a continuous basis. In most cases, requesting meta data (device ID, calibration data, etc. etc.) once at the
beginning of an experiment is sufficient. Measurement data (Temperature, pressure, etc. etc.) on the contrary is usually
queried on a more frequent basis. The data handler distinguishes between the two data types. Since there is no way to
distinguish the type of data queried by a call automatically in a reliable fashion, the user can specify the type for
each command using the meta-checkbox. Depending on the selection, a default value is implemented
(1h for meta-data, 30s for measurement data). Obviously, different users have different needs regarding polling
intervals, thus the defaults can be overwritten to transfer data according to a custom polling interval.

.. image:: _static/figures/data-handler.png
    :width: 800
    :alt: A view of the data handler feature

Only one configuration can be stored at a time. Future releases will include the possibility to upload and download
configuration files and select configuration files for a specific booking. The data handler simplifies data-acquisition
and encourages collection of all data and meta-data for improved data integrity. The separation of the data acquisition
from the user script used in the experiment has several advantages:

    1. The query calls are not part of the user-script, improving readability and making the script shorter.
    2. Reduces the amount of code that needs to be written by the operator.
    3. Data-acquisition is out-sourced to a separate process. This way data-acquisition is guaranteed to continue in case an experiment crashes.
    4. The data can be easily accessed from within the user script. An example script is provided in the scripts-section of the application.

.. image:: _static/figures/data-handler-tree.png
    :width: 800
    :alt: A view of the data handler feature

Scripting environment - Scripts
----------------------------------

This page allows the user to upload, create and edit scripts. The main view shows a list of all saved scripts.
Clicking on the script name or the **<>**-icon opens the script editor. The code editor is based on the
`Monaco Editor <https://www.npmjs.com/package/ngx-monaco-editor>`_ and includes syntax highlighting. Auto-completion is
not supported. Registered scripts can be assigned to experiments in the experiment section. A script assigned to an
experiment is executed in a docker container. The docker image is created based on the provided dockerfile which is
stored in the folder *user_script_env*. If non-standard python packages are required for the script execution, they must
be specified in the *requirements.txt*.

.. image:: _static/figures/scripts.png
    :width: 800
    :alt: A view of the scripting environment

.. warning::

    Scripts are not checked for programming errors. Check your code in an IDE before scheduling any experiments!

Tutorial 1: Hello SiLA 2 Manager!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *Hello device!* example is one of three pre-installed example scripts. You can find this example among the others
in the \'Scripts\'-tab. Assign this script to a new experiment and schedule it for execution. The output should be
printed to the experiment console view.

.. code-block:: python

        """
        TUTORIAL 1: Hello_SiLA_2_Manager
        ---------------------------------------------

        1.1 You can use this code editor like a regular scripting environment.
            If you require specific python packages for your script, you can import them here.

        Hint 1: Packages you want to import must be specified in the dockerfiles requirements.txt!
            The file is located in your SiLA 2 Manager Installation directory. The default location
            on Linux is /home/<your_username>/sila2_device_manager/user_script_env/requirements.txt.
            If you change the requirements, you need to rerun the create_container.sh to update the
            docker container image.
        """
        import sys
        import time
        import logging
        import numpy as np

        """
        1.2 You can use the python logging package and configure the output format here. Logging statements
            are transferred via the stderr of the docker container and are flushed by default by the logging function.
            All output is forwarded to the SiLA 2 Manager frontend. You can display the logs in the "experiments"
            tab by clicking on an experiment.
            When an script crashes straight-away, the logs may fail to arrive at the frontend so you have to open
            the files directly.
            The log files are stored locally on your computer:
            Linux:   /tmp/device_manager/container
            Windows: C:\\Users\\<your_username>\\AppData\\Local\\Temp\\device-manager\\container
        """

        logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)
        logger = logging.getLogger(name=__name__)

        """
        1.3 When the experiment is started, the function run() is called. Therefore, every script must
            contain a run() function. The run function requires one argument: services. This argument
            is used to pass the SiLA Server clients information into the script. You have to supply this
            argument, even if you don't use it!

        Hint 2: Use the flush argument when using print statements or add a newline character (\n) to the
            end of your string. Logging statements are flushed automatically.

        """


        def run(services):
            """ Required to import and instantiate devices """

            print('Hello SiLA2 Manager')
            # The above print statement will not be shown in the experiment terminal before the statement below is executed and flushed.
            time.sleep(5)
            print('Yay me, i got flushed!', flush=True)
            print(f'A random number: {np.random.rand()}', flush=True)

            write_logging_statement()
            write_to_output()
        """
        1.4 You can call other functions from within thr run() function. The function "write_logging_statement"
            writes logging statements of all available log_levels.
        """


        def write_logging_statement():
            """Writes logging statements"""
            time.sleep(1)
            logger.debug('A debug statement')
            time.sleep(1)
            logger.info('An info statement')
            time.sleep(1)
            logger.warning('A warning statement')
            time.sleep(1)
            logger.critical('A critical warning statement')
            time.sleep(1)
            logger.error('An error statement\n')
            time.sleep(3)

        """
        1.5 If direct calls to stdout and stderr are made, they won't get flushed either. Output has to be flushed explicitly.

        Hint 2: Use the flush argument when using print statements and the sys.stderr.flush and sys.stdout.flush function for
            write operations with sys.
        """


        def write_to_output():
            """Writes message to stderr"""
            sys.stderr.write('Error\n')
            sys.stderr.flush()
            time.sleep(1)
            sys.stdout.write('All Good\n')
            sys.stdout.flush()


Tutorial 2: Incorporating SiLA Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All registered services can be accessed in the scripting environment. However, used services should be selected in the
experiment setup phase. A dictionary with all service clients can be imported. Instantiating the client enables the user
to execute all functions the service offers. Further information on the python syntax for the service object access can be
found in the *'service example'* in the scripting environment. It is recommended to select all used services during the
experiment setup phase to avoid multi-access and interference with other experiments. Selecting a service will reserve
the service for exclusive use for that script.

.. code-block:: python

        """
        TUTORIAL 2: Incorporating SiLA 2 Clients
        ---------------------------------------------

        This example uses the SiLA Python HelloSiLA_Full example server.
        You can download it from the repository at https://gitlab.com/SiLA2/sila_python/-/tree/master/examples/HelloSiLA2/HelloSiLA2_Full

        To run this example follow these steps:

        2.1. Add a SiLA Server to your Services (Ideally the HelloSiLA example from the SiLA Python or Tecan repository)
        2.2. Go to the Data Handler tab and deactivate the "Active" checkmark for the device you want to use
        2.3. Set up an experiment with and select this script and the device you want to use
        2.4. Hit the run button or wait for the scheduled execution time (You can click on the experiment
            name to get the docker container stdout, i.e the output of your script)

        Hint 3: The command/property call syntax is displayed in the "Services" tab. It is shown under
            "Usage" on the lowest level of the device tree for every command and property.
        """
        import time


        def run(services):
            """ Instantiates selected devices for this experiment """
            client = services[0]
            print(f'Service instantiated: {client.name}@{client.ip}:{client.port}', flush=True)
            client.connect()
            # A GET command. A call to the SiLAService feature. Request the server name.
            response = client.call_property("SiLAService\n", "ServerName")
            ServerName = response
            print(response, flush=True)

            for i in range(10):
                response = client.call_property("SiLAService\n", "ServerName")
                print(f'{i}. call:', response, flush=True)
                time.sleep(1.5)
            OldServerName = response

            # A Set command. A call to the SiLAService feature. Change the server name.
            client.call_command("SiLAService\n","SetServerName", parameters={"ServerName/constrained/String": "MyNewName"})
            response = client.call_property("SiLAService\n", "ServerName")
            print('Changed name to: ', response['servername/constrained/string'], flush=True)
            # Change the ServerName back to the original one
            client.call_command("SiLAService\n","SetServerName", parameters={
                "ServerName/constrained/String": OldServerName['servername/constrained/string']})
            response = client.call_property("SiLAService\n", "ServerName")
            print('Changed name back to:', response['servername/constrained/string'], flush=True)


.. note::

    The syntax of the command call is shown in the service tree on the lowest level of each function call.
    You need to replace the "yourObject" part of the displayed call with the client object of that service!

Tutorial 3: Using the Data Handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The data handler allows the user to link a SiLA Service to a time-series database (InfluxDB). The data handler can be
configured for every SiLA Service to poll data in a user specified interval for selected commands and roperties. If data
transfer is activated for a Service, the data acquisition is started automatically for as soon as the respective
experiment is started.

.. code-block:: python

        """
        TUTORIAL 3: Using the Data Handler
        ---------------------------------------------
        3.1 The data handler can be used without writing a script. Go to the data handler tab and setup a database. Influx
            databases are supported. The overview will show you whether a connection has been established between the SiLA 2
            Manager and the specified database. Depending on the security settings of your database, supplying a username or
            password may not be necessary.

        3.2 You can link a database to a specific SiLA service. Click on the link button and select the desired database. You
            can unlink a database by selecting the empty option [] in the drop-down menu.

        3.3 There are several levels of customization. Expand the Service tree and activate the SiLA Features you want the data-
            acquisition to be active for. Selecting "Data Transfer" on the top level will automatically activate all features.
            Start de-selecting.

        3.4 The data handler distinguishes between two types of data: Meta data and process/experimental data. They differ in
            the time interval they are queried in. Both types have a set default polling interval. However, you may customize
            the time interval for both of them for each SiLA Command and Property on the lowest level of the tree.

        3.5 If a command requires a parameter, you can set the parameter here.

        3.6 The data handler is active for the full duration of the experiment and does not stop when the script is finished.
            It will only stop at the specified time or if the experiment is stopped manually.

        Hint 4: If your parameter changes over time, you should exclude the command query from the data handler and add a
            respective function and command call to your experimental script.
        """


        def run(services):
            """ Required to import and instantiate devices """
            return


Tutorial 3: Incorporating Databases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example shows you how to include read and write operations to and from databases into your script. The client
package of the database must be included in the docker requirements.txt, so you can access the client object in the
scripting environment.  Specify the database connection details when instantiating the client object.

As a first step, we ping the database to check whether we can establish a connection. The ping operation should return
the version number of the used database. Afterwards, a datapoint is written to the database and queried subsequently.
This is repeated a hundred times with an in-built delay time of 10 seconds. Check the experiment output console and the
chronograf interface.

.. code-block:: python

        """
        TUTORIAL 4: Incorporating Databases
        ---------------------------------------------
        4.1 Import the InfluxDBClient and other packages you will need
        """
        from influxdb import InfluxDBClient
        from datetime import datetime
        import numpy as np
        import time

        """
        4.2 Instantiate the InfluxDBClient with the connection details of the respective database and check the connection by
            pinging the database server. Make sure to change the default connection details below to your database details!
        """


        def run(services):
            influx_client = InfluxDBClient(host='127.0.0.1', port=8086, username='root', password='root', database='SiLA_2_Manager')
            print(f'Checking connectivity. DB server version: {influx_client.ping()}', flush=True)

            """
            4.3 If you do not already have a database, creat a new one:
            """

            influx_client.create_database(dbname='SiLA_2_Manager')

            """
            4.4 Create a datapoint to write to the database. Add adequate tags so you can filter your data efficiently in
                chronograf. If your script is running, you can check your data live in your browser, if your chronograf server
                is running: <ip-of-the-chronograf/influxDB-server>:8888 .
            """

            for i in range(0, 25, 1):
                # This is an example write operation
                random_number = np.random.rand()
                data_point = {
                    "measurement": "testMeasurement",
                    "tags": {
                        "experiment_name": "influxDB_test",
                        "device": "experiment_docker_container"
                    },
                    "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fields": {
                        "test_number": random_number
                    }
                }

                try:
                    influx_client.write_points([data_point])
                    print(f'A random number was written to the database: {random_number}', flush=True)
                except:
                    print("This did not work...")

                """
                4.5 Query your data using the SQL-like Influx Query Language (InfluxQL). You can find information on the syntax at:
                    https://docs.influxdata.com/influxdb/v1.8/query_language/ . The following query will read the value that was
                    just written to the database.

                Hint 4: Copy and paste the query below to visualize the data in chronograf. Change the LIMIT to display the
                    number of last data points. Remove the escape character (backslash) around the influxDB_test in the query.
                    You can leave out the last part of the query, starting at ORDER BY, to display all available measurements
                    of this type.
                """

                # This is an example query.
                results = influx_client.query(
                    'SELECT test_number FROM "SiLA_2_Manager"."autogen"."testMeasurement" WHERE experiment_name = \'influxDB_test\' GROUP BY position ORDER BY DESC LIMIT 1')
                print('The latest random number was queried from the database: ',  flush=True)
                print(results, flush=True)
                time.sleep(5)


Process monitoring
^^^^^^^^^^^^^^^^^^^^^^^^^^
Scripts are executed in a docker container. Interaction with a running docker container is limited. The *stdout* of the
docker container is transferred to the frontend by WebSockets. For real-time visualization of process data we recommend
using `chronograf <https://www.influxdata.com/time-series-platform/chronograf/>`_. Chronograf offers a complete interface
for the influxDB database. All data collected by the data handler can be visualized using the chronograf IoT frontend.

.. note::

    [WIP] Interaction with running docker containers is currently not possible. This feature is planned for a future
    release. Feel free to help us out!

Experiments
-----------------
Automated experiments (or processes) require access to services via a well-specified interface, a script that
orchestrates service operation and a database to store relevant information. The experiments view enables the user to
setup such workflows and schedule their execution. On the experiments page new experiments can be created by pressing
the the 'plus'-symbol. The experiment execution time, the script to be executed, as well as the services required for
execution can be defined in a pop-up form. Creation of experiments that require the booking of services unavailable
during the desired time-frame is not possible. If two experiments must access the same service simultaneously, a booking
should be avoided. The device is still accessible to the script.

.. warning::

    This is a safety measure to avoid potentially detrimental consequences caused by multiple access to state-sensitive laboratory devices.

The main view of the experiments tab shows a list of scheduled experiments, accompanied by the most important
information such as the start and end time of the experiment, booked services, the user script and the current status of
the experiment. Scheduled experiments automatically create a booking entry in the calendar view.
The experiment status may be one of the following:

+------------+-------------------------------------------+
| Status     |                  Meaning                  |
+============+===========================================+
| unknown    | The experiment has not been started yet   |
+------------+-------------------------------------------+
| finished   | Docker container finished with exit code 0|
+------------+-------------------------------------------+
| running    | Docker container is still running. The    |
|            | scheduled end time has not yet elapsed    |
+------------+-------------------------------------------+
| error      | Docker container finished with exit code 1|
+------------+-------------------------------------------+

It is possible to start experiments before their scheduled starting time by pressing the 'play'-icon. A running
experiment can be aborted prematurely by pressing the 'stop'-button.

.. image:: _static/figures/experiments.png
    :width: 800
    :alt: A view of the experiment view

.. note::

    In development mode the scheduler.py script must be running for experiments to be executed.


Service calendar
---------------------
If a service is assigned to a specific experiment, a booking is automatically created for the entire timeframe of the experiment.
A service can only be assigned to an experiment if it is available throughout the experiments start and end time. The
calendar page visualizes these bookings and provides the user with additional information on the booking, such as the respective
experiment, script and the user who created it. Furthermore, it is possible to create bookings manually. This allows the
reservation of services. In a future release, non-SiLA services and "offline"-services will be available as well. The
calendar could be used as a laboratory-wide booking system for other legacy services such as autoclaves or other resources.

It is possible to delete bookings manually. Even automatically created bookings can be deleted. However, this would
circumvent the in-built security mechanism and may lead to services being accessed by multiple experimental scripts at
the same time.

.. image:: _static/figures/calendar.png
    :width: 800
    :alt: A view of service bookings. The calendar.

