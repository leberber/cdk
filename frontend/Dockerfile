
FROM nginx:alpine

# Copy the pre-built Angular app
COPY dist/frontend/browser /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

