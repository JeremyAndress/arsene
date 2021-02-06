import time
import inspect
from unittest import TestCase
from cobnut import __version__, Cobnut, RedisModel


class CobnutTestCase(TestCase):

    def setUp(self):
        self.cobnut = Cobnut(redis_connection=RedisModel(host="localhost"))

    def test_version(self):
        assert __version__ == '0.1.2'

    def test_set(self):
        self.cobnut.set(key='test', data='test')
        assert self.cobnut.get(key='test') == 'test'
        self.cobnut.delete(key='test')
        assert self.cobnut.get(key='test') is None

    def test_set_expire(self):
        self.cobnut.set(key='test', data='test_expire', expire=1)
        assert self.cobnut.get(key='test') == 'test_expire'
        time.sleep(1)
        assert self.cobnut.get(key='test') == None

    def test_decorator_params(self):
        def without_decorator(data):
            pass
        data = list(inspect.signature(without_decorator).parameters.keys())

        @self.cobnut.clean_key(key='test')
        def get_decorator(data):
            pass
        assert list(
            inspect.signature(get_decorator).parameters.keys()
        ) == data
