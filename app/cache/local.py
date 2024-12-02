import pickle
from datetime import datetime, timedelta
from typing import TypedDict, Any, Optional

from .base import AbstractCache


class _ValueType(TypedDict):
    data: Any
    expires: datetime


class InMemoryCache(AbstractCache):
    """Кэш данных в памяти."""

    def __init__(self) -> None:
        self._cache: dict[str, _ValueType] = {}

    async def get(self, key: str) -> Optional[Any]:
        if value := self._cache.get(key, None):
            if value["expires"] is None or value["expires"] > datetime.now():
                return pickle.loads(value["data"])
            else:
                await self.delete(key)
        return None

    async def set(self, key: str, value: Any, expire: int) -> None:
        self._cache[key] = {
            "data": pickle.dumps(value),
            "expires": (datetime.now() + timedelta(seconds=expire)) if expire > 0 else None,
        }

    async def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    async def delete_namespace(self, prefix: str) -> None:
        for key in list(self._cache.keys()):
            if key.startswith(prefix):
                self._cache.pop(key, None)
