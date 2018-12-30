FROM nginx:1.15.8-alpine as nginx
EXPOSE 80
COPY nginx.conf /etc/nginx
COPY sites.conf /etc/nginx
CMD ["nginx", "-g", "daemon off;"]
