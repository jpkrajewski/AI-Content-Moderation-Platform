# build stage
FROM node:lts-alpine as build-stage

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

# Copy built files from build stage to nginx html directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy your custom nginx config template to nginx.conf
COPY nginx.conf.template /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
