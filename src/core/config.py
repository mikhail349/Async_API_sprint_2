import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
"""Корень проекта."""


class BaseConfig(BaseSettings):
    """Базовый класс для конфигураций, получающих значений из .env файла."""

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")


class ProjectSettings(BaseConfig):
    """Настройки проекта."""

    PROJECT_NAME: str = "Read-only API для онлайн-кинотеатра"
    """Название проекта."""
    PROJECT_DESC: str = (
        "Информация о фильмах, жанрах и людях, "
        "участвовавших в создании произведения"
    )
    """Описание проекта."""
    PROJECT_VER: str = "1.0.0"
    """Версия проекта."""


class RedisSettings(BaseConfig):
    """Настройки Redis."""

    REDIS_HOST: str = "127.0.0.1"
    """HOST для подклчючения к Redis."""
    REDIS_PORT: int = 6379
    """PORT для подклчючения к Redis."""
    CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
    """Кэширование кинопроизведений в секундах."""


class ElasticSettings(BaseConfig):
    """Настройки ElasticSearch."""

    ELASTIC_HOST: str = "127.0.0.1"
    """HOST для подклчючения к ElasticSearch."""
    ELASTIC_PORT: int = 9200
    """PORT для подклчючения к ElasticSearch."""
    ELASTIC_DEFAULT_PAGE_SIZE: int = 10
    """Размер ES-страницы по умолчанию."""


project_settings = ProjectSettings()
redis_settings = RedisSettings()
elastic_settings = ElasticSettings()
