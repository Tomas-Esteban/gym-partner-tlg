#!/bin/sh
set -e

mkdir -p /app/data/routines/warmups

# Sembrar rutinas por defecto si el volumen está vacío (primer arranque)
if [ ! -f /app/data/routines/routine.yaml ]; then
  echo "Inicializando rutinas en /app/data/routines ..."
  cp -r /app/default-routines/. /app/data/routines/
fi

if [ -z "$BOT_TOKEN" ] || [ "$BOT_TOKEN" = "your_telegram_bot_token" ]; then
  echo "ERROR: BOT_TOKEN no está configurado. Editá el archivo .env antes de arrancar."
  exit 1
fi

exec "$@"
