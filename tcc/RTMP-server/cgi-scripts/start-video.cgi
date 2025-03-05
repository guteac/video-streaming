#!/bin/bash

echo "Content-Type: application/json"
echo ""

read body

# Recebe o argumento (videoId)
VIDEO_ID=$body


# Verifica se o parâmetro foi passado
if [ -z "$VIDEO_ID" ]; then
  echo "Status: 400 Bad Request"
  echo "Content-Type: text/plain"
  echo ""
  echo "Erro: Parâmetro 'videoId' não fornecido."
  exit 1
fi

RESPONSE=$(curl -X 'POST' \
  'http://svc-api-agent:8000/start' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "{\"videoId\": \"$VIDEO_ID\"}")


# Verifica o código de saída do curl
if [ $? -eq 0 ]; then
  # Retorna a resposta da API
  echo "$RESPONSE"
else
  # Retorna uma mensagem de erro em caso de falha
  echo '{"error": "Falha ao conectar à API de destino"}'
  exit 1
fi