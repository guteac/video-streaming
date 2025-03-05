#!/bin/bash

read body

# Recebe o argumento (videoId)
VIDEO_ID=$body

# Diretório de origem
SOURCE_DIR="/usr/local/nginx/html/stream/hls"


# Verifica se o parâmetro foi passado
if [ -z "$VIDEO_ID" ]; then
  echo "Status: 400 Bad Request"
  echo "Content-Type: text/plain"
  echo ""
  echo "Erro: Parâmetro 'videoId' não fornecido."
  exit 1
fi

if [[ -e "$SOURCE_DIR/$VIDEO_ID.m3u8" && -e "$SOURCE_DIR/$VIDEO_ID-0.ts" ]]; then
  echo "Status: 200 OK"
  echo "Content-Type: text/plain"
  echo ""
  echo "Arquivos encontrados com sucesso."
else
  echo "Status: 404 Not Found"
  echo "Content-Type: text/plain"
  echo ""
  echo "Erro: Arquivos não encontrados."
  exit 1
fi