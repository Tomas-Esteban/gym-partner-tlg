# Despliegue

## Requisitos en producción

- Docker Desktop (Windows o macOS)
- Archivo `.env` con `BOT_TOKEN` válido
- Acceso a internet (polling de Telegram)

## Despliegue con Docker Compose

```bash
# Desde la raíz del proyecto
cp .env.example .env
# Editar .env

docker compose -f docker/docker-compose.yml up -d --build
```

## Volúmenes

El directorio `data/` se monta como volumen:

- `data/gym_assistant.db` — base de datos SQLite
- `data/routines/` — archivos YAML de rutinas

Para actualizar la rutina, reemplazar los YAML en `data/routines/` y reiniciar el contenedor.

## Logs

```bash
docker compose -f docker/docker-compose.yml logs -f bot
```

## Reiniciar

```bash
docker compose -f docker/docker-compose.yml restart bot
```

## Actualizar

```bash
git pull
docker compose -f docker/docker-compose.yml up -d --build
```

## Migraciones en Docker

```bash
docker compose -f docker/docker-compose.yml exec bot alembic upgrade head
```

## Multiplataforma

El proyecto usa rutas relativas y volúmenes Docker. Funciona igual en:

- macOS (desarrollo)
- Windows (producción con Docker Desktop)

No usar paths absolutos en configuración.
