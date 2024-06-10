# Build the frontend application
FROM node:20 as frontend-build

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

ARG VITE_API_URL=${VITE_API_URL}

RUN npm run build

# Serve the frontend with Nginx
FROM nginx:latest

COPY --from=frontend-build /app/dist/ /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
