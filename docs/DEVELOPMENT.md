# Desarrollo

## Estructura del proyecto

Ver [ARCHITECTURE.md](ARCHITECTURE.md) para el diseño completo.

```
src/gym_assistant/
├── bot/           # Handlers, FSM, keyboards, middlewares
├── config/        # Settings desde .env
├── domain/        # Entidades y excepciones
├── services/      # Lógica de negocio
├── infrastructure/# DB, YAML, repos
└── utils/         # Logging y utilidades
```

## Entorno de desarrollo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Ejecutar en desarrollo

```bash
# Con logging debug
LOG_LEVEL=DEBUG gym-assistant
```

## Tests

```bash
pytest
```

## Migraciones

Crear una nueva migración tras cambiar modelos:

```bash
alembic revision --autogenerate -m "descripcion del cambio"
alembic upgrade head
```

## Estrategia de ramas

```
main          ← producción
develop       ← integración
feature/*     ← desarrollo por etapa
```

## Convenciones

- Conventional Commits para mensajes de commit
- Tipado en todo el código Python
- Handlers no acceden directamente a DB ni YAML
- Configuración solo via `.env`

## Agregar un handler

1. Crear módulo en `bot/handlers/`
2. Registrar router en `bot/dispatcher.py`
3. Delegar lógica a servicios en `services/`
