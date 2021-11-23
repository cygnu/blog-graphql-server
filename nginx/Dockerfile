FROM nginx:1.20.2-alpine

RUN rm -f /etc/nginx/conf.d/defalut.conf
COPY ./defalut.conf /etc/nginx/conf.d

CMD [ "nginx", "-g", "daemon off;" ]
