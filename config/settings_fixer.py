from pathlib import Path
from pydantic import (
    Field
)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):

    # validation_alias - это тот ключ, который pydantic будет искать внутри вашего .env файла \
    # чтобы затем присвоить его значение переменной telegram_api_key
    # подробнее https://docs.pydantic.dev/latest/concepts/fields/#field-aliases
    api_key_fixer: str = Field(validation_alias='api_key_fixer')

    _env_path = Path(__file__).resolve().parent / '.env'
    model_config = SettingsConfigDict(env_file=str(_env_path),  # path to your .env
                                      env_file_encoding="utf-8",
                                      extra="ignore"  # extra keys in .env will be ignored
                                      )

fixer_config = Config()
