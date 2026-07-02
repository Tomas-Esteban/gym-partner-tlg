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

    def __init__(self, received: int, expected: int) -> None:
        self.received = received
        self.expected = expected
        super().__init__(f"Se recibieron {received} pesos, se esperaban {expected}")


class InvalidWeightFormatError(GymAssistantError):
    """Formato de peso inválido en el mensaje."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"Peso inválido: {value}")


class InvalidRPEError(GymAssistantError):
    """RPE fuera del rango válido (1-10)."""
