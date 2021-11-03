FROM nodered/node-red

COPY settings.js /data/

RUN cd /data/

RUN npm install node-red-contrib-flow-manager