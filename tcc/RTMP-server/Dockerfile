FROM tiangolo/nginx-rtmp

RUN apt-get update -y

RUN apt-get install fcgiwrap -y

#RUN cp /usr/share/doc/fcgiwrap/examples/nginx.conf /etc/nginx/fcgiwrap.conf

COPY fcgiwrap.conf /etc/nginx/

RUN mkdir -p /usr/lib/cgi-bin

# Enviando a configuracao para o container
COPY nginx.conf /etc/nginx/nginx.conf

COPY cgi-scripts /usr/lib/cgi-bin/

RUN chown -R www-data.www-data /usr/lib/cgi-bin/

RUN chmod -R 755 /usr/lib/cgi-bin/

# Cria um diretório para os fragmentos HLS
RUN mkdir -p /usr/local/nginx/html/stream/hls
RUN mkdir -p /usr/local/nginx/html/stream/most-viewed

ADD start_nginx.sh /

RUN chmod +x /start_nginx.sh

# Inicia o servidor
CMD ["/start_nginx.sh"]