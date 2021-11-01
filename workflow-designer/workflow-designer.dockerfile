FROM nodered/node-red

COPY settings.js /data/

RUN cd /data/

RUN npm install https://gitlab.com/RZechlin/node-red-contrib-flow-manager-postgres
