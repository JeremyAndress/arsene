from json import dumps, loads
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
        if not self.client.get(key): return None
        data_convert = self.client.get(key).decode('utf-8')
        data_json = loads(data_convert)
        if data_json['type'] in ['str','int','float','bytes']:
            return data_json['data']
        elif data_json['type'] in ['list','tuple','dict']:
            return loads(data_json['data'])
