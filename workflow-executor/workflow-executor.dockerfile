FROM nodered/node-red-docker:v10

COPY settings.js /data/

RUN cd /data/

RUN npm install https://gitlab.com/RZechlin/node-red-contrib-flow-manager-postgres