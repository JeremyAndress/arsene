from typing import Optional
from pydantic import BaseModel


class RedisModel(BaseModel):
    host: str
    db: int = 0
    port: int = 6379
    ssl: bool = False
    encoding: str = 'utf-8'
    health_check_interval: int = 0
    username: Optional[str] = None
    password: Optional[str] = None
    ssl_check_hostname: bool = False
    ssl_ca_certs: Optional[str] = None
    max_connections: Optional[int] = None
    ssl_cert_reqs: Optional[str] = 'required'
    socket_connect_timeout: Optional[int] = None

    class Config:
        orm_mode = True
