# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:14 as build-stage

WORKDIR /app

RUN npm i -g @angular/cli && npm cache clean --force && npm cache verify

#COPY ./nginx.conf /nginx.conf
COPY package*.json /app/
COPY ./ /app/

RUN npm install
RUN npm run config

EXPOSE 4200

#Disabled we are running on an development server for the time being, this should not be the case for deployment due to
#security concerns

#ARG FRONTEND_ENV=production
#ENV ANGULAR_APP_ENV=${FRONTEND_ENV}

# Comment out the next line to disable tests
# RUN npm run test:unit

CMD ["ng","serve","--host", "0.0.0.0", "--poll"]

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
#FROM nginx:1.15

#Disabled we use angulars prod server to enable hot-reload functionality
#TODO swap back to prod environment for deployment/add deployment tag

#COPY --from=build-stage /app/dist/frontend /usr/share/nginx/html

#COPY --from=build-stage /nginx.conf /etc/nginx/conf.d/default.conf
#COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
