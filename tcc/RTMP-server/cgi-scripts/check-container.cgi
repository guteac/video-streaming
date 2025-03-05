#!/bin/bash

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
RESPONSE_BODY=$(mktemp)
HTTP_CODE=$(curl -s -o "$RESPONSE_BODY" -w "%{http_code}" \
  -X 'POST' 'http://svc-api-agent:8000/check' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "{\"videoId\": \"$VIDEO_ID\"}")

# Verifica o código de saída do curl
if [ "$HTTP_CODE" -eq 200 ]; then
  # Retorna a resposta da API
  echo "Status: 200 OK"
  echo "Content-Type: text/plain"
  echo ""
  echo "Container up"
elif [ "$HTTP_CODE" -eq 404 ]; then
  echo "Status: 404 Not Found"
  echo "Content-Type: text/plain"
  echo ""
  echo "Erro: Container não encontrado $VIDEO_ID."
  exit 1
else
  echo "Status: 500 Internal Server Error"
  echo "Content-Type: text/plain"
  echo ""
  echo "Erro: Algo deu errado. Código de status: $HTTP_CODE"
  exit 1
fi

# Remove o arquivo temporário
rm -f "$RESPONSE_BODY"