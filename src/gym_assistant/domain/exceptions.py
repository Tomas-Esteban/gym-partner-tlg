"""Excepciones de dominio."""


class GymAssistantError(Exception):
    """Error base de la aplicación."""


class UserNotFoundError(GymAssistantError):
    """Usuario no encontrado."""


class RoutineNotFoundError(GymAssistantError):
    """Rutina o día no encontrado en YAML."""


class SessionNotFoundError(GymAssistantError):
    """Sesión de entrenamiento no encontrada."""


class InvalidWeightCountError(GymAssistantError):
    """Cantidad de pesos no coincide con ejercicios."""


class InvalidRPEError(GymAssistantError):
    """RPE fuera del rango válido (1-10)."""
