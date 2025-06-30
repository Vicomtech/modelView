FROM node:latest as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build

FROM nginx as production-stage
COPY --from=build-stage /app/dist /var/www/html
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./resources/*.pem /etc/ssl