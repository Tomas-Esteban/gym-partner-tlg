# Setup

## Requisitos

- Python 3.12+
- Docker y Docker Compose (para despliegue)
- Token de bot de Telegram (via [@BotFather](https://t.me/BotFather))

## Instalación local

```bash
# Clonar repositorio
git clone <repo-url>
cd gym-partner-tlg

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -e ".[dev]"

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu BOT_TOKEN
```

## Configuración

Copiar `.env.example` a `.env` y completar:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Token del bot de Telegram | (requerido) |
| `DATABASE_URL` | URL de SQLite | `sqlite:///data/gym_assistant.db` |
| `ROUTINES_PATH` | Ruta a rutinas YAML | `data/routines` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |
| `PROGRESSION_WEEKS_THRESHOLD` | Semanas para incremento | `3` |
| `PROGRESSION_RPE_THRESHOLD` | RPE máximo para incremento | `8.0` |

## Migraciones

Las migraciones se aplican automáticamente al iniciar el bot. También podés ejecutarlas manualmente:

```bash
alembic upgrade head
```

## Ejecutar

```bash
gym-assistant
```

## Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```

El volumen `data/` persiste la base de datos y las rutinas YAML entre reinicios.
