How-To
=======

Connecting to the device manager
---------------------------------

If your device manager server is running on your local machine or on a computer within your network, you can
connect to the frontend from any internet capable device with a modern browser. Simply connect using one of the
following URLs:

If the server is running locally:

    `localhost:4200 <http://localhost:4200>`_ or `127.0.0.1:4200 <http://127.0.0.1:4200>`_

If the server is running on another computer within your network:

    <host-server-ip\>:4200

Login page
-----------

The log-in view is a security feature, that ensures that only registered users have access to the devices in your
network. The Open Authorization protocol 2 (OAuth2) is used to secure communication between the backend and frontend.
Once logged-in, you can add new users, delete users and reset passwords. The device manager frontend uses the Angular
Authentication tool (AuthInterceptor) which relies on a HttpInterceptor interface to grant access to permitted users.
If accessed from the host machine, the url of the login-page is `<localhost:4200/login>`_. The default username is
**admin** and the default password is **1234**. It is strongly recommended to change the default password of the admin
account.

.. image:: figures/login.png
    :width: 800
    :alt: A view of the login page with entered admin credentials


Main page - Devices
-------------
The devices page is the device managers main view. Registered devices are listed here and some useful detail is provided
on first sight. This includes the devices server name, address, port. Furthermore, the connection status is indicated. In a future version other devices types than SiLA, such as offline devices, custom device or OPC-UA types shall be supported.
Several buttons allow the user to expand the visible detail of the device, change its current name, or
remove the device from the manager. Clicking on the device name or the information icon expands the view of the selected
device, showing the implemented features and the respective descriptions. Each feature can be expanded even further to
investigate which (observable) commands and (observable) properties are implemented by the feature. Exploring individual
commands and properties shows the user useful information on functionality and usage. Required parameters and responses
are displayed with the attributed SiLA-datatype.

.. image:: figures/devices.png
    :width: 800
    :alt: A view of the main page, the devices list, including general device details

Device discovery
^^^^^^^^^^^^^^^^^^
The device manager uses the SiLA2 auto-discovery functionality which relies on multicast DNS service discovery
(`zeroconf <https://pypi.org/project/zeroconf/>`_) to register its services in
the network. New devices can be added by clicking the "plus"-button on the top right of the device table. Device
discovery is started from within a new pop-up window. The discovery mode scans for SiLA devices in the network and displays the
basic information it was registered with by the server. This information is used to connect to the server using a
dynamic client. The client files are stored in the local temporary folder named after the devices server-UUID:
Relative path to the directory: *[...]temp/device-manager/SiLA/<device-UUID>/*

.. image:: figures/discovery.png
    :width: 800
    :alt: A view of the discovery feature for adding new devices to the manager

SiLA Explorer - The device tree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Each device is that is added to the device manager is assigned an internal UUID. This way devices with the same server
name can be uniquely identified. The device tree enables the user to run commands and request properties interactively
from within the browser. On the lowest level of the device tree, the command/property level, a run button can be clicked
to execute the function. For functions that require user input, the parameters can be entered in the corresponding text
box. The syntax by which the call can be incorporated into python scripts in the scripting environment is shown.

.. image:: figures/device-tree.png
    :width: 800
    :alt: A view of the discovery feature for adding new devices to the manager

The data handler
------------------
`InfluxDB <https://www.influxdata.com/Y>`_ databases can be registered and linked to devices. InfluxDB is a time-series database that is well suited for
experimental data. To be able to use this feature, an InfluxDB server must be running within your network. Providing the
connection details to the device manager is sufficient. A registered database can be linked to a device for data
transfer. Data transfer is started as soon as the booking of a device commences.

The implementation of the data handler will run the configured commands in the user-specified polling intervals and
store the responses in the linked database with experiment name, device name and user name as tags. To activate the data
acquisition for a selected device, the "active"-checkbox must be ticked. If responses of certain functions, or features
all together, should not be stored, further checkboxes can be found on the lower levels of the device tree to deactivate
data transfer. This is crucial to disable the execution of set commands for example.

Most types of data can be classified as either meta-data or measurement data. Typically, meta-data doesn't need to be
queried on a continuous basis. In most cases, requesting meta data (device ID, calibration data, etc. etc.) once at the beginning of an experiment is sufficient.
Measurement data (Temperature, pressure, etc. etc.) on the contrary is usually queried on a more frequent basis. The
data handler distinguishes between the two. Since there is no way to distinguish the two automatically in a reliable
fashion, the user can specify the type for each command using the meta-checkbox. Depending on the selection, a default value is implemented
(1h for meta-data, 60s for measurement data). Obviously, different users have different needs regarding polling
intervals, thus the defaults can be overwritten to transfer data according to a custom polling interval.

Only one configuration can be stored at a time. Future releases will include the possibility to upload and download
configuration files and select configuration files for a specific booking.


//.. image:: src/data_handler_main_view.png
//    :width: 800
//    :height: 200
//    :alt: A view of the data handler feature

Scripting environment - Scripts
--------------------------------

//.. image:: src/my_scripts_view.png
//    :width: 800
//    :height: 200
//    :alt: A view of the scripting environment

Experiments
-----------------

//.. image:: src/experiments_view.png
//    :width: 800
//    :height: 200
//    :alt: A view of the experiment creation feature

Device calendar
------------------

//.. image:: src/booking_view.png
//    :width: 800
//    :height: 200
//    :alt: A view of the device booking system

