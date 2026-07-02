# Arquitectura

## Visión general

Gym Assistant sigue una arquitectura por capas:

| Capa | Responsabilidad |
|------|-----------------|
| **Presentación** (`bot/`) | Handlers Telegram, FSM, keyboards |
| **Aplicación** (`services/`) | Lógica de negocio |
| **Dominio** (`domain/`) | Entidades y excepciones |
| **Infraestructura** (`infrastructure/`) | DB, YAML, repositorios |

Los handlers **no acceden** directamente a la base de datos ni leen archivos YAML.

## Flujo de datos

```
Telegram → Handler → Service → Repository → SQLite
                         ↓
                    YamlLoader → routine.yaml
```

## FSM del entrenamiento

```
Idle → AwaitingDay → AwaitingWeights → AwaitingRPE → Completed
         ↑_______________ cancelar en cualquier estado _______________↓
```

### Etapa 4 (implementado)

- Comando `gym` detecta el próximo día sugerido según historial
- Teclado inline para elegir cualquier día de la rutina
- Muestra calentamiento (`upper` / `lower`) según el día
- Envía la hoja completa de ejercicios en un mensaje

### Etapa 5 (implementado)

- Sesión `in_progress` creada al elegir día, con `exercise_logs` vacíos
- Parseo de pesos multilínea (uno por línea, en orden)
- Validación de cantidad y formato; reintento sin perder estado
- `/cancelar` descarta sesión en DB y limpia FSM

### Etapa 6 (implementado)

- Solicitud de RPE (1–10) tras registrar pesos
- Sesión marcada como `completed` con `session_rpe` y `completed_at`
- Resumen final con ejercicios, pesos y esfuerzo
- FSM vuelve a `Idle` al completar

### Etapa 7 (implementado)

- Consulta del último `weight_kg` por `exercise_key` al mostrar la hoja
- Peso sugerido igual al último registrado (hasta etapa 8)
- `suggested_weight_kg` persistido en `exercise_logs` al iniciar sesión

### Etapa 8 (implementado)

- `ProgressionService` con regla de 3 semanas y RPE promedio semanal
- `progression_tracking` actualizado al completar sesión
- Incremento por ejercicio desde `progression.increment_kg` en YAML

## Rutinas YAML

Las rutinas viven en `data/routines/` como archivos YAML validados con Pydantic al inicio. La base de datos solo almacena claves de referencia (`day_key`, `exercise_key`, `routine_version`).

### Archivos

| Archivo | Contenido |
|---------|-----------|
| `routine.yaml` | Rutina activa con 4 días y ejercicios |
| `warmups/upper.yaml` | Calentamiento tren superior |
| `warmups/lower.yaml` | Calentamiento tren inferior |

### Claves estables

Cada ejercicio tiene un `key` independiente del nombre visible. Esto permite cambiar rutinas cada 4 meses sin perder continuidad del historial.

### Validación

El bot valida el YAML al arrancar. Si hay errores de formato, no inicia y registra el error en logs.

## Progresión de pesos

Motor de progresión (etapa 8, implementado):

```
SI weeks_at_current_weight >= PROGRESSION_WEEKS_THRESHOLD (default: 3)
Y avg_session_rpe últimas N semanas activas < PROGRESSION_RPE_THRESHOLD (default: 8.0)
Y increment_kg > 0 (definido en YAML por ejercicio)
ENTONCES suggested_weight = last_weight + increment_kg
SINO suggested_weight = last_weight
```

- `progression_tracking` se actualiza al completar cada sesión
- El RPE de sesión alimenta el promedio semanal
- Solo cuentan semanas con al menos una sesión completada

## Escalabilidad futura

Módulos futuros (estadísticas, nutrición, dashboard web) se agregan como servicios independientes reutilizando la capa de repositorios existente.
