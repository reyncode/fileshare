# Build the frontend application
FROM node:20 as frontend-build

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

ARG REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}
ARG REACT_APP_STORAGE_URL=${REACT_APP_STORAGE_URL}
ARG REACT_APP_FILE_BUCKET_NAME=${REACT_APP_FILE_BUCKET_NAME}
ARG NODE_ENV=${NODE_ENV}

RUN npm run build

# Serve the frontend with Nginx
FROM nginx:latest

COPY --from=frontend-build /app/build/ /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
