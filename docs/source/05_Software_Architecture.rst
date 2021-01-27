Software Arcitecture
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

Backend
========
include a pictogram of the backend that is more detailed than the general one. Include redis, postgreSQL, device layer,
dynamic client, sila_device, data-handler, influxDB, FatsAPI, scheduler, experiment environment and how they interact
Written in python.

Create documentation of backend API automatically using sphinx.

Auto-discovery of SiLA devices
-------------------------------
Explain the zeroconf concept and explain what information is broadcasted via the network. Explain, that it is necessary/
better to name the server.

Dynamic client
---------------


Execution of Experiments
-------------------------
postgreSQL -> script as tar -> container (docker_helper.py -> put archive) -> extract -> use

The data handler
-----------------

Backend API
------------


.. include:: backend.rst


Frontend
=========
Angular, material design, long term support, industry standard,  written in TypeScript (JavaScript compatible),

Create documentation of frontend API automatically using sphinx.
