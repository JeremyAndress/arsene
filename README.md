<p align="center">
  <img width="320" height="320" src="docs/arsene.png" alt='Arsene'>
</p>

<p align="center">
<em>Simple cache management to make your life easy.</em>
</p>

<p align="center">
<a href="https://github.com/JeremyAndress/arsene/actions/workflows/python-app.yml" target="_blank">
    <img src="https://github.com/JeremyAndress/arsene/actions/workflows/python-app.yml/badge.svg" alt="Test">
</a>

<a href="LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/peaceiris/actions-gh-pages.svg" alt="MIT">
</a>

<a href="https://pypi.python.org/pypi/arsene" target="_blank">
    <img src="https://badge.fury.io/py/arsene.svg" alt="pypy">
</a>
</p>

---

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