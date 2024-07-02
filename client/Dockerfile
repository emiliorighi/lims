FROM node:17 as build-stage

ARG BASE_PATH

WORKDIR /client

COPY package*.json ./

RUN npm install

COPY . .

ENV VITE_BASE_PATH=${BASE_PATH}

RUN npm run build

# production stage
FROM nginx:stable-alpine

#  copy the nginx.conf in our filesystem into the image filesystem
COPY default.conf.template /etc/nginx/templates/default.conf.template

COPY --from=build-stage /client/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
