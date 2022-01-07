# Master Thesis Robert Zechlin

## Installation

Requirements: [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/).

1) Clone the [_idprz_ branch of the SiLA 2 Manager](https://gitlab.com/lukas.bromig/sila2_manager/-/tree/idprz)
2) Run `docker-compose up -d` to start the stack
3) Refer to the documentation of the SiLA 2 Manager for further information if issues occur
4) Access the Node-Red Workflow Editor under http://localhost:1880

A documentation of the API can be found at http://localhost/docs/

Access the database under http://localhost:5050 and use username `admin@lamas.biovt.mw.tum.de` 
and password `1234` to log in.

Add connections in pgadmin to the Workflow Designer's and Scheduler's databases.
1) Select _Object/Create/Server..._
2) Input _Name_ of choice
3) Under _Connection_, input 
   1) Host name: `db-workflow-designer` or `db-workflow-scheduler`
   2) Username: `postgres`
   3) Password: `DIB-central`
 
## Code Repositories

* [SiLA 2 Manager](https://gitlab.com/lukas.bromig/sila2_manager/-/tree/idprz)
* [node-red-contrib-flow-manager-postgres](https://gitlab.com/RZechlin/node-red-contrib-flow-manager-postgres)
* [node-red-contrib-sila2-node](https://gitlab.com/RZechlin/node-red-contrib-sila2-node)
* [node-red-contrib-flow-manager](https://flows.nodered.org/node/node-red-contrib-flow-manager)
* [node-red-contrib-storagemodule-postgres](https://github.com/WeekendWarrior1/node-red-contrib-storagemodule-postgres)