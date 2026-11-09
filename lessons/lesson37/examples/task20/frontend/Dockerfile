FROM node:22-alpine AS build
WORKDIR /site
COPY package.json .
RUN npm install
COPY index.html main.jsx ./
RUN npm run build
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /site/dist /usr/share/nginx/html
