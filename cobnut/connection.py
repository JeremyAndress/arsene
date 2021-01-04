from json import dumps
from redis import Redis


class RedisConnection():
    def __init__(
        self, *, host: str, port: int = 6379,
        db = 0, password: str = None,
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


    def set(self, *, key: str, data):
        data_convert = self.set_data(data)
        self.client.set(key, data_convert)


    def set_data(self, data):
        data_convert = {
            'type': type(data).__name__,
            'data': None 
        }
        if (
            isinstance(data, list) or isinstance(data, dict) or
            isinstance(data, tuple)
        ):
            data_convert['data'] = dumps(data)
        elif (
            isinstance(data, str) or isinstance(data, int) or 
            isinstance(data, float) or isinstance(data, bytes)
        ):
            data_convert['data'] = data
        return dumps(data_convert)

    def get(self, *, key: str):
        return self.client.get(key)
