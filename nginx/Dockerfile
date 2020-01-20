# Getting Base Image
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y nginx
RUN apt-get install -y nginx-extras

# Port
EXPOSE 80 3000
WORKDIR /usr/src/app/

COPY nginx.sh /usr/src/app/
COPY nginx.conf /etc/nginx/
#CMD ["/usr/sbin/nginx", "-g", "'daemon off;'"]
CMD ["/usr/src/app/nginx.sh"]
