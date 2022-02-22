FROM nodered/node-red:2.1.3

COPY settings.js /data/

RUN cd /data/

RUN npm install https://gitlab.com/RZechlin/node-red-contrib-flow-manager-postgres
RUN npm install https://gitlab.com/RZechlin/node-red-contrib-sila2-node