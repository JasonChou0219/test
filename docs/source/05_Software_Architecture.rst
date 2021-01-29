Software Architecture
=====================

General architecture
---------------------
Include a pictogram that includes all parts of the device manager on a high level of abstraction (Database-Backend-Frontend-level)
Based solely on freely available, open-source code. Used packages were selected with long-term support and respective
low maintenance considerations.

Current Implementation is based on the SiLA-Python repository. The SiLA-python repository currently doesn't support the
full standard yet.  The standards implementations are still being actively  developed. We work closely together with the
SiLA-Python working group and some of our members are actively contributing too both repositories. As the standards
python implementation evolves, the Device manager updates will incorporate new changes.

Include C4 diagrams of software architecture
Maybe include UML diagrams here as well.

// .. image:: _static/figures/Still missing.png
//    :width: 800
//    :alt: General architecture on a high level of abstraction


// .. image:: _static/figures/Still missing.png
//    :width: 800
//    :alt: Architecture on a more detailed level

Clarify:
- General interaction between modules.
- Interaction with redis DB and postgreSQL
- Interaction with scheduler.py
- Interaction with data-handler.py


Backend
========
include a pictogram of the backend that is more detailed than the general one. Include redis, postgreSQL, device layer,
dynamic client, sila_device, data-handler, influxDB, FatsAPI, scheduler, experiment environment and how they interact
Written in python.

Create documentation of backend API automatically using sphinx.

Discovery of SiLA devices
-------------------------------
Explain the zeroconf concept and explain what information is broadcasted via the network. Explain, that it is necessary/
better to name the server.

All SiLA servers implement Multicast DNS (mDNS) and DNS-based Service Discovery (DNS-SD). The SiLA2 specifications for
device discovery are defined in the `SiLA Part (B) - Mapping Specification <https://docs.google.com/document/d/1-shgqdYW4sgYIb5vWZ8xTwCUO_bqE13oBEX8rYY_SJA/edit#heading=h.w2jcp32bd1a5>`_.
The SiLA2 Device Manager uses the `python-zeroconf <https://github.com/jstasiak/python-zeroconf>`_ implementation to
discover registered services.

The backend code used for the discovery feature is located in the folder *source.device_manager.sila_auto_discovery*.

.. automodule:: source.device_manager.sila_auto_discovery.sila_auto_discovery
    :members:
    :undoc-members:
    :show-inheritance:


**Discovery Example**

The discovery functionality can easily be explored by running the *find()* function from the root directory of this project:

.. code-block:: python

    import os
    import sys
    sys.path.insert(0, os.path.abspath('.'))
    from source.device_manager.sila_auto_discovery.sila_auto_discovery import find


    servers = find()
    print(servers)

Dynamic client
---------------
The dynamic client is capable of connecting to a server without any prior knowledge of the servers functionality. In SiLA2
this is made possible by standard features. The SiLA Service feature contains the necessary functions
(Get_ImplementedFeatures(), and Get_FeatureDefinition()) to query the information necessary to construct the client once a
connection has been established.

The SiLA2 Device Manager uses the SiLA_python dynamic client. The created client files are stored as temporary data on the
host machine the device machine is running on. The client files are deleted if the device is deleted within the application.
When a device is added to application, a UUID is assigned for internal reference. This UUID is displayed in the expandable device detail information
on the frontend main page and is used. This UUID is also used as storage name for the device client files.

**Dynamic client Example**

.. automodule:: source.device_manager.device_layer.dynamic_client
    :members: DynamicSiLA2Client
    :undoc-members:
    :show-inheritance:

The dynamic client is located at *source.device_manager.device_layer*. The dynamic client can be executed freely without
the application. If invoked directly, the respective code snippet at the bottom of the file can be un-commented. The basic
connection and code generation functionality can be achieved with the code snippet below. Further examples can be found
in the file itself.

.. code-block:: python

    if __name__ == "__main__":
         # Add source to path to enable imports
         import os
         import sys
         sys.path.insert(0, os.path.abspath('.'))

         # or use logging.INFO (=20) or logging.ERROR (=30) for less output
         # logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.INFO)
         client = DynamicSiLA2Client(name="DynamicClient", server_ip='127.0.0.1', server_port=50051)

         # create the client files
         client.generate_files()
         # start the client, which will load all data from the server
         client.run()

Execution of Experiments
-------------------------
postgreSQL -> script as tar -> container (docker_helper.py -> put archive) -> extract -> use

The data handler
-----------------


Backend API
------------

The python backend uses the `FastAPI web framework <https://fastapi.tiangolo.com/>`_. The source code is open-source and
available in the `fastapi repository <https://github.com/tiangolo/fastapi>`_.

.. automodule:: backend
    :members:


Frontend
=========

To-Do:
- Which framework is used and what technology is it based on?
- Used interface design guidelines and why? mat design
- used programming languages
- Include: Angular, material design, long term support, industry standard,  written in TypeScript (JavaScript compatible),

