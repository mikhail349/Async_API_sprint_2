from pydantic import BaseSettings


class TestSettings(BaseSettings):
    ELASTIC_HOST: str = "127.0.0.1"
    """HOST для подклчючения к ElasticSearch."""
    ELASTIC_PORT: int = 9200
    """PORT для подклчючения к ElasticSearch."""

    REDIS_HOST: str = "127.0.0.1"
    """HOST для подклчючения к Redis."""
    REDIS_PORT: int = 6379
    """PORT для подклчючения к Redis."""

    API: str = "http://localhost:8000/api/v1/"


test_settings = TestSettings()
