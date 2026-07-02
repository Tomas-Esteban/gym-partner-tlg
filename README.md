# Gym Assistant

Asistente personal de gimnasio via bot de Telegram. Registra entrenamientos, recuerda pesos anteriores y sugiere progresiones futuras.

## Características

- Bot de Telegram con flujo conversacional
- Rutinas configurables via archivos YAML
- Historial de entrenamientos en SQLite
- Progresión de pesos basada en RPE semanal
- Multi-usuario (cada chat de Telegram es independiente)
- Docker para despliegue multiplataforma

## Inicio rápido

```bash
cp .env.example .env
# Editar .env con tu BOT_TOKEN

docker compose -f docker/docker-compose.yml up --build
```

## Documentación

- [Setup](docs/SETUP.md) — instalación y configuración
- [Desarrollo](docs/DEVELOPMENT.md) — guía para desarrolladores
- [Despliegue](docs/DEPLOY.md) — producción en Docker
- [Arquitectura](docs/ARCHITECTURE.md) — diseño del sistema
- [Base de datos](docs/DATABASE.md) — esquema y migraciones
- [Roadmap](docs/ROADMAP.md) — plan de desarrollo
- [Changelog](docs/CHANGELOG.md) — historial de cambios

## Stack

- Python 3.12
- aiogram 3
- SQLAlchemy 2 + Alembic
- SQLite
- Docker / Docker Compose
- YAML para rutinas

## Licencia

Uso personal.
