from typing import Any, Optional
from pydantic import BaseModel


class RedisModel(BaseModel):
    host: str
    port: int = 6379
    db: Any = 0
    password: Optional[str] = None
    max_connections: Optional[int] = None
    socket_connect_timeout: Optional[int] = None

    class Config:
        orm_mode = True