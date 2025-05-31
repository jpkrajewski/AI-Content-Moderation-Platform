FROM nginx:latest

RUN mkdir -p /app

COPY ./dist /app/

COPY ./config /app/

COPY ./assets/ /app/assets/

COPY nginx.conf.template /etc/nginx/nginx.conf


RUN apk update libexpat libxml2 libcurl libssl libxpm aom-libs libdav1d && apk upgrade


EXPOSE 80

CMD /usr/local/bin/envtpl /app/index.html -o /app/index.html && \
    /usr/local/bin/envtpl /etc/nginx/nginx.conf.template -o /etc/nginx/nginx.conf && \
    exec nginx -g 'daemon off;'
