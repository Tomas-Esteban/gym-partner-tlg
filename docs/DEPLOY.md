# Despliegue con Docker

Guía para correr Gym Assistant en otra PC (Windows, macOS o Linux) con Docker y dejarlo funcionando 24/7.

## Requisitos en la PC de producción

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución
- Token del bot de Telegram ([@BotFather](https://t.me/BotFather))
- Conexión a internet (el bot usa polling de Telegram)

## Despliegue desde cero

### 1. Obtener el proyecto

```bash
git clone https://github.com/Tomas-Esteban/gym-partner-tlg.git
cd gym-partner-tlg
git checkout develop
```

O copiá la carpeta del proyecto a la otra PC (USB, red, etc.).

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Editá `.env` y poné tu token real:

```env
BOT_TOKEN=7123456789:AAHtu_token_real_aqui
DATABASE_URL=sqlite:///data/gym_assistant.db
ROUTINES_PATH=data/routines
LOG_LEVEL=INFO
PROGRESSION_WEEKS_THRESHOLD=3
PROGRESSION_RPE_THRESHOLD=8.0
```

**Importante:** nunca subas `.env` a GitHub (ya está en `.gitignore`).

### 3. Levantar el bot

Desde la **raíz del proyecto**:

```bash
docker compose up -d --build
```

Esto:
- Construye la imagen
- Aplica migraciones de DB al arrancar
- Deja el contenedor corriendo en segundo plano
- Reinicia automáticamente si la PC se reinicia (`restart: unless-stopped`)

### 4. Verificar que funciona

```bash
docker compose logs -f bot
```

Deberías ver algo como:

```
Bot starting...
Database migrations applied
Rutina cargada: Rutina Actual v2026-07 (4 días)
Bot ready, polling started
```

Probá en Telegram: `/start` → `gym`

## Comandos útiles

| Acción | Comando |
|--------|---------|
| Ver logs en vivo | `docker compose logs -f bot` |
| Detener el bot | `docker compose down` |
| Reiniciar | `docker compose restart bot` |
| Reconstruir tras cambios | `docker compose up -d --build` |
| Estado del contenedor | `docker compose ps` |

## Datos persistentes

La carpeta `data/` se monta como volumen:

| Ruta | Contenido |
|------|-----------|
| `data/gym_assistant.db` | Base de datos (historial, pesos, usuarios) |
| `data/routines/routine.yaml` | Tu rutina activa |
| `data/routines/warmups/` | Calentamientos |

Si borrás el contenedor, **los datos en `data/` se conservan**.

Para actualizar la rutina: editá los YAML en `data/routines/` y ejecutá `docker compose restart bot`.

## Windows (Docker Desktop)

1. Instalá Docker Desktop y activá WSL2 si te lo pide
2. Abrí PowerShell o CMD en la carpeta del proyecto
3. Los mismos comandos funcionan:

```powershell
copy .env.example .env
# Editar .env con Notepad
docker compose up -d --build
docker compose logs -f bot
```

## Actualizar a una versión nueva

```bash
git pull
docker compose up -d --build
```

Las migraciones de base de datos se aplican solas al reiniciar.

## Solución de problemas

| Problema | Solución |
|----------|----------|
| `BOT_TOKEN no está configurado` | Completá `BOT_TOKEN` en `.env` |
| Error de validación YAML | Revisá formato de `data/routines/routine.yaml` |
| El bot no responde | `docker compose logs -f bot` y verificá que esté `polling started` |
| Puerto / red | No hace falta abrir puertos; el bot sale a internet por polling |

## Arquitectura Docker

```
┌─────────────────────────────────┐
│  PC (Windows / macOS / Linux)   │
│  ┌───────────────────────────┐  │
│  │  gym-assistant-bot        │  │
│  │  (Python 3.12 + aiogram)  │  │
│  └───────────┬───────────────┘  │
│              │ volumen           │
│  ┌───────────▼───────────────┐  │
│  │  ./data/                  │  │
│  │  ├── gym_assistant.db     │  │
│  │  └── routines/            │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
              │
              ▼
        Telegram API
```
