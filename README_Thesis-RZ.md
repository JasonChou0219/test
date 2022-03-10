# Master Thesis Robert Zechlin

## Installation

Requirements: [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/).

1) Clone the [_node-red-final_ branch of the SiLA 2 Manager](https://gitlab.com/lukas.bromig/sila2_manager/-/tree/node-red-final)
2) Run `docker-compose up -d` to start the stack
3) Refer to the documentation of the SiLA 2 Manager for further information if issues occur
4) Access the Frontend under http://localhost:4200
5) Log-in on the top-right with credentials `admin@lamas.biovt.mw.tum.de` 
and password `1234` 
6) Create flows under Workflow Design / Node-RED and click deploy
7) Create a Job template under Jobs / Create Job by selecting the workflow
8) Schedule the job for execution under Jobs / Schedule Job (Schedule one hour early) 

A documentation of the API can be found at http://localhost/docs/

### Database

Access the database under http://localhost:5050 and use username `admin@lamas.biovt.mw.tum.de` 
and password `1234` to log in.

Add connections in pgadmin to the Workflow Designer's and Scheduler's databases.
1) Select _Object / Create / Server..._
2) Input _Name_ of choice
3) Under _Connection_, input 
   1) Host name: `db-workflow-designer` or `db-workflow-scheduler`
   2) Username: `postgres`
   3) Password: `DIB-central`
4) Find stored flows under _Databases / workflow-designer / Schemas / public / Tables / flow_
 
### Workflow Execution
In order to access the Scheduler's API, authentication needs to occur first. Log in by sending a POST request to 
``http://localhost/api/v1/login/access-token`` with username `admin@lamas.biovt.mw.tum.de` 
and password `1234` to receive an _access_token_.

To run a workflow, send a POST request to `http://localhost/api/v1/jobs/` specifying the minimum requirements in the
request's body like so:
```
{
  "execute_at": "2022-01-01T12:00:00.0Z",
  "title": "Test Job",
  "flow_id": "f6f2187d.f17ca8"
}
```
Retrieve the _flow_id_ from Node-Red or the database and authorize the request with the received _access_token_.
You might need to account for time zone discrepancies.

## Code Repositories

* [SiLA 2 Manager](https://gitlab.com/lukas.bromig/sila2_manager/-/tree/idprz)
* [node-red-contrib-flow-manager-postgres](https://gitlab.com/RZechlin/node-red-contrib-flow-manager-postgres)
* [node-red-contrib-sila2-node](https://gitlab.com/RZechlin/node-red-contrib-sila2-node)
* [node-red-contrib-flow-manager](https://flows.nodered.org/node/node-red-contrib-flow-manager)
* [node-red-contrib-storagemodule-postgres](https://github.com/WeekendWarrior1/node-red-contrib-storagemodule-postgres)