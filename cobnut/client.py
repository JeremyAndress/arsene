from typing import Union, Dict, List, Optional
from connection import RedisConnection
from schemas.redis import RedisModel

class Cobnut():
    def __init__(
        self, *, redis_connection: Union[RedisModel, None] = None
    ):
        self.redis_connection = redis_connection
        self.store = self.create_store()


    def create_store(self):
        if self.redis_connection:
            store = self.redis_conn
            return store


    def redis_conn(self):
        r = RedisConnection(
            host=self.redis_connection.host
        )
        r.ping()
        return r


    def set(self, *, key: str, data: Union[str, int, Dict, List]):
        self.store().set(key=key, data=data)

cobnut = Cobnut(redis_connection=RedisModel(host="localhost"))
cobnut.set(key='la', data='lala')