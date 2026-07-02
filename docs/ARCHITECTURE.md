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
Idle → AwaitingDay → ShowingWorkout → AwaitingWeights → AwaitingRPE → Completed
         ↑_______________ cancelar en cualquier estado _______________↓
```

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

Motor de progresión (etapa 8):

```
SI weeks_at_current_weight >= 3
Y avg_session_rpe últimas 3 semanas < 8.0
ENTONCES suggested_weight = current_weight + increment_kg
SINO suggested_weight = current_weight
```

## Escalabilidad futura

Módulos futuros (estadísticas, nutrición, dashboard web) se agregan como servicios independientes reutilizando la capa de repositorios existente.
