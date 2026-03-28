import os

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # API — PORT is set automatically by Render; API_PORT is used locally
    API_HOST: str = "0.0.0.0"
    API_PORT: int = int(os.environ.get("PORT", 8000))
    API_RELOAD: bool = False

    # CORS — comma-separated string in .env, e.g. http://localhost:4200,http://localhost:3000
    CORS_ORIGINS: str = "http://localhost:4200"

    # Simulation limits
    MAX_EVENTS: int = 1_000_000
    MAX_PHOTONS: int = 1_000_000
    MAX_SIMULATIONS: int = 1_000_000

    @computed_field
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
