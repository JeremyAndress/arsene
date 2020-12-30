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


    def ping(self):
        self.client.ping()


    def set(self, *, key, data):
        self.client.set(key, data)