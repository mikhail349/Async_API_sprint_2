import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """Декодировать в unicode."""
    return orjson.dumps(v, default=default).decode()


class OrjsonMixin(BaseModel):
    """Миксин для замены стандартной работы с json на более быструю."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
