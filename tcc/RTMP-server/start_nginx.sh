#!/bin/bash
# Inicia o NGINX em segundo plano
nginx -g "daemon off;" &

# Aguarda o NGINX iniciar (ajuste se necessário)
sleep 15

# Executa o comando desejado
echo "Executando comando pós-inicialização do NGINX..."
spawn-fcgi -s /var/run/fcgiwrap.socket -M 766 /usr/sbin/fcgiwrap 

# Mantém o container rodando
wait
