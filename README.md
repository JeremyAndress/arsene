# Cobnut

Simple cache to make your life easy

### Installation
```sh
pip install cobnut
```

### Quick Start
For the tutorial, you must install redis as dependency

```sh
pip install cobnut[redis]
```


The simplest Cobnut setup looks like this:

```python
from cobnut import Cobnut, RedisModel

cobnut = Cobnut(redis_connection=RedisModel(host="localhost"))
cobnut.set(key='mykey', data='mydata')
cobnut.get(key='mykey')
#Response: mydata
cobnut.delete(key='test')
cobnut.get(key='test')
#Response : None
```