
FROM nginx:alpine

# Copy the pre-built Angular app
COPY dist/frontend/browser /usr/share/nginx/html


EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

