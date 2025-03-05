#!/bin/bash

read body

# Recebe o argumento (videoId)
VIDEO_ID=$body

# Diretórios de origem e destino
SOURCE_DIR="/usr/local/nginx/html/stream/hls"
DEST_DIR="/usr/local/nginx/html/stream/most-viewed"

# Verifica se o parâmetro foi passado
if [ -z "$VIDEO_ID" ]; then
  echo "Status: 400 Bad Request"
  echo "Content-Type: text/plain"
  echo ""
  echo "Erro: Parâmetro 'videoId' não fornecido."
  exit 1
fi

# Move os arquivos que começam com o videoId
mv "$SOURCE_DIR/$VIDEO_ID"* "$DEST_DIR/"

# Verifica se o comando foi bem-sucedido
if [ $? -eq 0 ]; then
  echo "Status: 200 OK"
  echo "Content-Type: text/plain"
  echo ""
  echo "Arquivos movidos com sucesso."
else
  echo "Status: 404 Not Found"
  echo "Content-Type: text/plain"
  echo ""
  echo "Erro: Arquivos não encontrados."
  exit 1
fi