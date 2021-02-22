# Arsene
[![Test](https://github.com/JeremyAndress/arsene/actions/workflows/python-app.yml/badge.svg)](https://github.com/JeremyAndress/arsene/actions/workflows/python-app.yml) [![license](https://img.shields.io/github/license/peaceiris/actions-gh-pages.svg)](LICENSE)

Simple cache management to make your life easy.

### Requirements 
- Python 3.6+ 

### Installation
```sh
pip install arsene
```

### Quick Start
For the tutorial, you must install redis as dependency

```sh
pip install arsene[redis]
```


The simplest Arsene setup looks like this:

```python
from arsene import Arsene, RedisModel

arsene = Arsene(redis_connection=RedisModel(host="localhost"))
arsene.set(key='mykey', data='mydata')
arsene.get(key='mykey')
# Response: mydata

arsene.delete(key='mykey')
arsene.get(key='mykey')
# Response: None

```