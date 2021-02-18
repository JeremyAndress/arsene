from json import loads
from typing import Optional
from redis import Redis
from .data_convert import set_data, object_hook


class RedisConnection():
    def __init__(
        self, *, host: str, port: int = 6379,
        db=0, password: str = None,
        socket_connect_timeout: int = 1
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.status = False
        self.socket_connect_timeout = socket_connect_timeout
        self.client = self.create_client()

    def create_client(self):
        return Redis(
            host=self.host, port=self.port, db=self.db, password=self.password,
            socket_connect_timeout=self.socket_connect_timeout
        )

    def test_connection(self):
        self.client.ping()
        self.status = True

    def set(self, *, key: str, expire: Optional[int] = None, data):
        data_convert = set_data(data)
        self.client.set(key, data_convert, ex=expire)

    def get(self, *, key: str):
        if not self.client.get(key):
            return None

        data_convert = self.client.get(key).decode('utf-8')
        data_json = loads(data_convert)

        if data_json['type'] in ['str', 'int', 'float', 'bytes']:
            return data_json['data']

        elif data_json['type'] in ['list', 'tuple', 'dict']:
            return loads(data_json['data'], object_hook=object_hook)

    def delete(self, *, key: str):
        self.client.delete(key)
