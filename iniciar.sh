#!/bin/bash
# Inicializa todo o ambiente do Assistente de Regulamento Esportivo
set -e
cd "$(dirname "$0")"

echo "=== Assistente de Regulamento Esportivo ==="

# 1. Carrega variáveis de ambiente
set -a && source .env && set +a

# 2. Túnel HTTPS (ngrok) — precisa vir antes do n8n para passar WEBHOOK_URL
if ! pgrep -f "ngrok http" > /dev/null; then
  echo "[1/4] Iniciando tunnel ngrok..."
  nohup ngrok http 5678 > /tmp/ngrok.log 2>&1 &

  # Aguarda API local do ngrok disponibilizar a URL (timeout de 30s)
  NGROK_URL=""
  for i in $(seq 1 30); do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null \
      | python3 -c "
import sys, json
t = json.load(sys.stdin).get('tunnels', [])
print(next((x['public_url'] for x in t if x['public_url'].startswith('https')), ''))
" 2>/dev/null || true)
    [ -n "$NGROK_URL" ] && break
    sleep 1
  done

  if [ -z "$NGROK_URL" ]; then
    echo "      ERRO: timeout aguardando URL do ngrok. Verifique /tmp/ngrok.log"
    exit 1
  fi
  echo "      Túnel: $NGROK_URL"
else
  NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null \
    | python3 -c "
import sys, json
t = json.load(sys.stdin).get('tunnels', [])
print(next((x['public_url'] for x in t if x['public_url'].startswith('https')), ''))
" 2>/dev/null || true)
  echo "[1/4] ngrok já está rodando: $NGROK_URL"
fi

# 3. n8n via Docker (com WEBHOOK_URL para que o Telegram Trigger saiba sua URL pública)
if ! docker ps --format '{{.Names}}' | grep -q n8n_regulamento; then
  echo "[2/4] Iniciando n8n..."
  docker run -d --rm \
    -p 5678:5678 \
    -v n8n_data:/home/node/.n8n \
    -e N8N_SECURE_COOKIE=false \
    -e WEBHOOK_URL="$NGROK_URL" \
    --name n8n_regulamento \
    n8nio/n8n

  # Aguarda n8n responder (timeout de 30s)
  N8N_OK=0
  for i in $(seq 1 30); do
    curl -sf http://localhost:5678/healthz > /dev/null 2>&1 && N8N_OK=1 && break
    sleep 1
  done
  [ "$N8N_OK" -eq 1 ] && echo "      n8n OK" || echo "      AVISO: n8n pode ainda estar iniciando"
else
  echo "[2/4] n8n já está rodando"
fi

# 4. Webhook Telegram — registra manualmente apontando para o n8n
echo "[3/4] Registrando webhook no Telegram..."
WEBHOOK_RESP=$(curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
  -d "url=$NGROK_URL/webhook/regulamento-esportivo-bot")
echo "$WEBHOOK_RESP" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('ok'):
    print('      Webhook OK:', d.get('description', 'registrado'))
else:
    print('      ERRO no webhook:', d.get('description', d))
    sys.exit(1)
"

# 5. API Python
if ! curl -sf http://localhost:8000/health > /dev/null 2>&1; then
  echo "[4/4] Iniciando API Python..."
  source .venv/bin/activate
  nohup uvicorn src.api:app --host 0.0.0.0 --port 8000 > /tmp/api_regulamento.log 2>&1 &

  # Aguarda a API responder (timeout de 60s — modelo HuggingFace pode demorar)
  API_OK=0
  for i in $(seq 1 60); do
    curl -sf http://localhost:8000/health > /dev/null 2>&1 && API_OK=1 && break
    sleep 1
  done
  [ "$API_OK" -eq 1 ] && echo "      API OK" || echo "      API falhou — verifique /tmp/api_regulamento.log"
else
  echo "[4/4] API já está rodando"
fi

IP=$(hostname -I | awk '{print $1}')
echo ""
echo "=== Tudo no ar ==="
echo "  n8n UI:    http://$IP:5678"
echo "  API:       http://localhost:8000/health"
echo "  Túnel:     $NGROK_URL"
echo "  Webhook:   $NGROK_URL/webhook/regulamento-esportivo-bot"
echo ""
echo "IMPORTANTE: ative o workflow no n8n UI (toggle ON) se ainda não fez."
echo ""
echo "Para parar tudo:"
echo "  docker stop n8n_regulamento && pkill -f 'ngrok http' && pkill -f 'uvicorn src.api'"
