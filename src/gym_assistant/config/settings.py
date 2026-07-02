"""Configuración de la aplicación desde variables de entorno."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración centralizada cargada desde .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bot_token: str = Field(default="", description="Token del bot de Telegram")
    database_url: str = Field(
        default="sqlite:///data/gym_assistant.db",
        description="URL de conexión a la base de datos",
    )
    routines_path: Path = Field(
        default=Path("data/routines"),
        description="Ruta al directorio de rutinas YAML",
    )
    log_level: str = Field(default="INFO", description="Nivel de logging")
    progression_weeks_threshold: int = Field(
        default=3,
        description="Semanas mínimas antes de considerar incremento de peso",
    )
    progression_rpe_threshold: float = Field(
        default=8.0,
        description="RPE promedio máximo para permitir incremento de peso",
    )


def get_settings() -> Settings:
    """Retorna la instancia de configuración."""
    return Settings()
