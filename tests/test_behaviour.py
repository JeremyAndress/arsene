import time
import inspect
from datetime import datetime
from unittest import TestCase
from arsene import Arsene, RedisModel


class ArseneTestCase(TestCase):

    def setUp(self):
        self.arsene = Arsene(redis_connection=RedisModel(host='localhost'))

    def test_set(self):
        self.arsene.set(key='test', data='test')
        assert self.arsene.get(key='test') == 'test'
        self.arsene.delete(key='test')
        assert self.arsene.get(key='test') is None

    def test_set_expire(self):
        self.arsene.set(key='test', data='test_expire', expire=1)
        assert self.arsene.get(key='test') == 'test_expire'
        time.sleep(1)
        assert self.arsene.get(key='test') is None

    def test_decorator_params(self):
        def without_decorator(data):
            pass
        data = list(inspect.signature(without_decorator).parameters.keys())

        @self.arsene.clean_key(key='test')
        def get_decorator(data):
            pass
        assert list(
            inspect.signature(get_decorator).parameters.keys()
        ) == data

    def test_decorator_return(self):
        @self.arsene.cache(
            key='test_cache', check_kwargs_params=True,
            check_args_params=True, kwargs_list=['data'],
            expire=2
        )
        def cache(pk, data='data', extra='extra_data'):
            return {'now': datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}
        response = cache(1, data=[1, 4, 5], extra='extra_data')

        assert cache(
            1, data=[1, 4, 5], extra='extra_data'
        ) == response

        time.sleep(2)

        assert cache(
            1, data=[1, 4, 5], extra='extra_data'
        ) != response

    def test_complex_data(self):
        data = [
            {
                'id': 580,
                'encrypt': 'zOzdQcztWnDgb1A2UjfeQw==',
                'status': None,
                'date': datetime.now()
            },
            {
                'id': 581,
                'encrypt': 'nAo3CnQE2S2YqQUdc77kvA==',
                'status': True,
                'date': datetime(1999, 2, 3)
            }
        ]
        self.arsene.set(key='complex_data', data=data, expire=3)
        time.sleep(2)
        assert self.arsene.get(key='complex_data') is not None
