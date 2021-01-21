from cobnut import __version__, Cobnut, RedisModel


def test_version():
    assert __version__ == '0.1.1'

def test_client():
    cobnut = Cobnut(redis_connection=RedisModel(host="localhost"))
    cobnut.set(key='test', data='test')
    cobnut.get(key='test')
    cobnut.delete(key='test')
    cobnut.get(key='test')
