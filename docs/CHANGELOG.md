# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added

- Scaffolding inicial del proyecto con Docker y documentación
- Base de datos SQLite con SQLAlchemy y Alembic
- Cargador de rutinas YAML con validación Pydantic
- Bot skeleton de Telegram con registro automático de usuarios
- Flujo `gym`: selección de día, calentamiento y hoja de ejercicios
- Registro de pesos multilínea con validación y persistencia en SQLite
- Captura de RPE de sesión y cierre de entrenamiento con resumen final
- Hoja de entrenamiento con último peso y peso sugerido por ejercicio
- Motor de progresión basado en RPE semanal e incrementos configurables en YAML

### Changed

- Docker: compose en raíz, entrypoint con validación de token y rutinas por defecto
- Fix: middleware de usuario en callback_query para selección de día
