# Base de datos

## Motor

SQLite via SQLAlchemy 2.0. Migraciones gestionadas con Alembic.

## Tablas

### users

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER PK | ID interno |
| telegram_id | BIGINT UNIQUE | ID de Telegram |
| username | VARCHAR | Username de Telegram |
| display_name | VARCHAR | Nombre visible |
| created_at | DATETIME | Fecha de registro |

### user_settings

Pares clave-valor por usuario (ej: `last_completed_day_key`).

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER PK | |
| user_id | INTEGER FK → users | |
| key | VARCHAR | Clave de configuración |
| value | VARCHAR | Valor |

### training_sessions

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER PK | |
| user_id | INTEGER FK → users | |
| routine_name | VARCHAR | Nombre de la rutina YAML |
| routine_version | VARCHAR | Versión de la rutina |
| day_key | VARCHAR | Clave del día (day_1, day_2...) |
| warmup_type | VARCHAR | upper / lower |
| session_rpe | INTEGER NULL | RPE de sesión (1-10) |
| status | VARCHAR | in_progress / completed / cancelled |
| started_at | DATETIME | Inicio de sesión |
| completed_at | DATETIME NULL | Fin de sesión |

### exercise_logs

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER PK | |
| session_id | INTEGER FK → training_sessions | |
| exercise_key | VARCHAR | Clave estable del ejercicio |
| exercise_name | VARCHAR | Nombre desnormalizado |
| order_index | INTEGER | Orden en la rutina |
| sets_planned | INTEGER | Series planificadas |
| reps_planned | VARCHAR | Repeticiones planificadas |
| suggested_weight_kg | FLOAT | Peso sugerido al inicio |
| weight_kg | FLOAT NULL | Peso registrado |

### progression_tracking

Motor de progresión (etapa 8). Se actualiza al completar cada sesión:

- `week_start`: lunes de la semana de la sesión
- `avg_session_rpe`: promedio de RPE de sesiones completadas esa semana
- `weeks_at_current_weight`: semanas consecutivas (con actividad) en el mismo peso
- Usado para calcular `suggested_weight` en la hoja de entrenamiento

## Migraciones

```bash
# Aplicar todas
alembic upgrade head

# Crear nueva
alembic revision --autogenerate -m "descripcion"
```

## Nota

La base de datos **no almacena rutinas**. Solo historial, entrenamientos, pesos y configuraciones.
