# Documentation
## Definitions
In order to ensure consistency across the application development and its implementation, 
certain keywords shall have global definitions. These keywords should not be used in a way that does 
not comply to their definition within the code, documentation, and elsewhere.

| Key      | Definition                                                    |
|----------|---------------------------------------------------------------|
| Job      | A scheduled set of workflows                                  |
| Service  | A service in the architecture consisting of its own container |
| Workflow | A definition of actions in any programming language           |
## Abbreviations
### Services
| Key    | Definition                 |
|--------|----------------------------|
| FE     | Frontend                   |
| BGW    | Backend Gateway            |
| SM     | Service Manager            |
| WFD_Py | Workflow Designer Python   |
| WFD_NR | Workflow Designer Node-RED |
| WFS    | Workflow Scheduler         |
### Other
| Key  | Definition           |
|------|----------------------|
| DB   | Database             |
| NR   | Node-RED             |
| Py   | Python               |
| TS   | TypeScript           |
| TSDB | Time-Series Database |
| WF   | Workflow             |
## Commit Etiquette
1) If possible, limit commits to a single service.
2) Add the abbreviation of the affected service(s) to the commit message followed by a colon and a short description. 
   Example:
```
WFD_Py: Fixed DB connection
FE, BGW: Updated schema
```
3) Only use abbreviations found in the tables above.