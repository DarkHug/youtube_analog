import json

from pydantic import validator, AnyUrl, model_validator
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    @validator("CORS_ORIGINS", "ALLOWED_HOSTS", pre=True)
    def _parse_str_list(cls, v):
        # 1. Если v is None — вернуть пустой список [].
        if v is None:
            return []

        if isinstance(v, (list, tuple)):
            return [str(x).strip() for x in v if str(x).strip()]

        if isinstance(v, str):
            s = v.strip()

            if s == "" or s in ("[]", "None"):
                return []

            if s.startswith("["):
                try:
                    parsed = json.loads(s)
                except Exception:
                    raise ValueError("Invalid JSON format for list field")

                # Если parsed — список/кортеж — нормализуем и возвращаем.
                if isinstance(parsed, (list, tuple)):
                    return [str(x).strip() for x in parsed if str(x).strip()]

                raise ValueError("JSON did not produce a list")

            return [p for p in [p.strip() for p in s.split(",")] if p]

        raise ValueError("Unsupported type for list field")

    @model_validator(mode="after")
    def _check_required_fields_in_production(self):
        """
        Выполняется после валидации модели. Проверяем, что в production:
         - SECRET_KEY задан и не равен dev-значению,
         - DATABASE_URL реально настроен (простая проверка).
        Если условие не выполнено — поднимаем ValueError, который превратится в ValidationError при создании Settings().
        """
        if getattr(self, "APP_ENV", None) == "production":
            secret_key = getattr(self, "SECRET_KEY", None)
            db_url = getattr(self, "DATABASE_URL", None)

            if not secret_key or secret_key == "very_secret_key":
                raise ValueError("SECRET_KEY must be set to a secure value in production")

            # Простая проверка — можно усложнить (длина, схема, и т.д.)
            if not db_url or db_url.startswith("postgres://postgres:postgres@localhost"):
                raise ValueError("DATABASE_URL must be set correctly in production")

        return self

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    APP_ENV: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 200
    REFRESH_TOKEN_EXPIRE_DAYS: int = 10
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    STORAGE_BACKEND: str = "local"
    LOG_LEVEL: str = "INFO"
    MAX_UPLOAD_SIZE_MB: int = 100

    ALLOWED_HOSTS: list[str] = []
    CORS_ORIGINS: list[str] = []


settings = Settings()
