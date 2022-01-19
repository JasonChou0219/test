# APScheduler

# Create model, schema, endpoints for job object

# Create model, schema, endpoints for booking object (relation booking <-> job?)

# Create function for execution container

# Add execution container name/id to job (update job) to keep track of executor
# Create websocket endpoint to stream stdout/stderr of executor container

# Add python packages to workflow object
# Install python packages in container
# Add "files" for e.g. data to workflow object
# Inject "files" into container volume

# Add packages and files to frontend workflow designer python view

# Add a view for the running job:
# - A list of all jobs (running, exited, scheduled)
# - General details about the job like user, start, end-time,
# used services, scripts, data protocols, dataflows
# - 3 tabs for workflow, [data acquisition, and data flow] respectively
# - More detail on each flow type in tab like stdout/stderr, stop/pause/delete option, potentially input, link to database/chronograf
# Report generation of job, stored in PostgreSQL
