FAQ
=====

Error 500: Internal Server Error
---------------------------------
**Error**:

.. code-block:: console

        Error 500: Internal Server Error

The device manager frontend issues a token to a user upon login. The token has an expiration date and is only valid for
X min. If the user is inactive for a longer period of time, the token is not refreshed and access is denied. A token may
invalidate for other reasons as well. Access from multiple browsers by the same user may also cause this issue.

**Solution**: Logout and log back in again. This will renew your token. Close device manager tabs in other browsers.

.. note::  You can set the expiration time and the extension time for a token-refresh in the *backend.py* file in line 87-88.


Protobuf: A file with this name is already in the pool
-------------------------------------------------------
**Error**:

.. code-block:: console

        TypeError: Couldn't build proto file into descriptor pool!
        Invalid proto descriptor for file "messages.proto":
          messages.proto: A file with this name is already in the pool.

This error will show in the backend console and it's logs. It is a known error on windows machines and related to the
protobuf package. The standard wheel installation of protobuf doesn't allow the use of multiple files with the same name
in the same pool. All SiLA devices implement the standard features, thus, this is problematic. The protobuf --no-binary
installation is different to the wheel and allows just that.

**Solution**: Run the *protobuf_no_binary_install.bat* script which is located in the root directory of this software. The
script uninstalls the standard protobuf installation and replaces it with the binary build. Pipenv doesn't implement the
--no-binary flag, thus pip is used. Protobuf is added to the pipfile afterwards for completeness sake.

Psycopg2 (PostgreSQL client): Connection Pool Exhausted
-------------------------------------------------------
**Error**:

The number of connections to the connection pool (SimpleConnectionPool) is exhausted. The error message reads:

.. code-block:: console

        Traceback (most recent call last):
        File "scheduler.py", line 380, in <module>
          main()
        File "scheduler.py", line 374, in main
          schedule_future_experiments_from_database()
        File "scheduler.py", line 258, in schedule_future_experiments_from_database
          for exp in experiment.get_scheduling_info():
        File "/usr/device-manager/source/device_manager/experiment.py", line 125, in get_scheduling_info
          conn = get_database_connection()
        File "/usr/device-manager/source/device_manager/database.py", line 34, in get_database_connection
          return storage['pool'].getconn()
        File "/usr/device-manager/.venv/lib/python3.8/site-packages/psycopg2/pool.py", line 92, in _getconn
           raise PoolError("connection pool exhausted")
        psycopg2.pool.PoolError: connection pool exhausted

**Solution:**
Generally, a connection is returned and closed after use. A maximum number of connections is allowed. This number is
specified in the file */source/device_manager/database.py* in the function *get_database_connection*. Each user
requires several connections. If multiple users access the device manager, the total number of connections may get
exhausted. Increasing the number of *maxconn* of the SimpleConnectionPool will solve this problem.

SiLA 2 Python (sila2lib) Error: KeyError 'HOME'
-------------------------------------------------------
**Error**:

The SiLA 2 Manager is run as a service. This service doesn't have access to the environmental variables of the user. The
SiLA 2 library is trying to get the path of the home directory. The command *os.environ* returns a dictionary of the
environmental variables. The key ['HOME'] is not contained and hence the operation raises a KeyError:

.. code-block:: console

        Traceback (most recent call last):
        File "./source/device_manager/device_layer/sila_device.py", line 14, in create_and_init_dynamic_client
          client = DynamicSiLA2Client(name=f'{name}-client',
        File "./source/device_manager/device_layer/dynamic_client.py", line 93, in __init__
          super().__init__(name, description, server_name, client_uuid, version,
        File "/home/david/sila2_device_manager/.venv/lib/python3.8/site-packages/sila2lib/sila_client.py", line 117, in __init__
          self.sila2_config = read_config_file('client', name)
        File "/home/david/sila2_device_manager/.venv/lib/python3.8/site-packages/sila2lib/_internal/config.py", line 22, in read_config_file
          config_dir = get_config_dir(subdir=name)
        File "/home/david/sila2_device_manager/.venv/lib/python3.8/site-packages/sila2lib/_internal/config.py", line 12, in get_config_dir
          path = os.path.join(os.environ['HOME'], '.config', 'sila2')
        File "/usr/lib/python3.8/os.py", line 675, in __getitem__
            raise KeyError(key) from None
        KeyError: 'HOME'
        None

**Solution:**
Replace the following line in file: sila2_device-manager/.venv/lib/python3.8/site-packages/sila2lib/_internal/config.py
Line 13:
path = os.path.join(os.environ['HOME'], '.config', 'sila2')
with the explicit path of your home directory or the home directory that you created for the SiLA 2 Manager:
path = os.path.join('/home/device-manager', '.config', 'sila2')

To-do:
-------
- Incorporate SiLA client meta-data in python repository
- Incorporate observable commands in device manager
- Implement lock/authorization feature
- Edit experiment and update bookings and experiments in backend properly
