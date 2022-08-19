FROM nginx:1.17.6

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx
COPY mlflow.conf.template /etc/nginx/sites-enabled/
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh