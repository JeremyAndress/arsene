from logging import Logger
from functools import wraps
from typing import (
    Dict, List, Tuple, Optional, Union,
    Callable, Any
)

from arsene.logger import logger
from arsene.schemas.redis import RedisModel
from arsene.key_builder import generate_key
from arsene.exceptions import ValidationBroker
from arsene.data_convert import (
    set_data, resolve_data,
    object_hook, date_serial
)


class Arsene:
    def __init__(
        self, *, redis_connection: Optional[RedisModel] = None,
        global_expire: Optional[int] = None,
        set_data: Callable[[Any], Any] = set_data,
        resolve_data: Callable[[Any], Any] = resolve_data,
        object_hook: Callable[[Any], Any] = object_hook,
        json_serial: Callable[[Any], Any] = date_serial,
        catch_errors: bool = False, logger: Logger = logger
    ) -> None:
        self.logger = logger
        self.set_data = set_data
        self.object_hook = object_hook
        self.json_serial = json_serial
        self.catch_errors = catch_errors
        self.resolve_data = resolve_data
        self.global_expire = global_expire
        self.redis_connection = redis_connection
        self.store = self.create_store()

    def create_store(self) -> Any:
        if self.redis_connection:
            store = self.redis_conn()
        else:
            raise ValidationBroker
        return store

    def redis_conn(self) -> Any:
        from arsene.connection.redis_client import RedisConnection
        r = RedisConnection(
            schema=self.redis_connection,
            resolve_data=self.resolve_data,
            object_hook=self.object_hook,
            json_serial=self.json_serial,
            set_data=self.set_data
        )
        r.test_connection()
        return r

    def set(self, *, key: str, expire: Optional[int] = None, data: Union[
        str, int, Dict, List, float,
        bytes, Tuple
    ]) -> None:
        ex = expire if expire else self.global_expire
        try:
            self.store.set(key=key, expire=ex, data=data)
        except Exception as e:
            self.logger.error(f'Arsene error {e}')
            if not self.catch_errors:
                raise

    def get(self, *, key: str) -> Union[
        str, int, Dict, List, float,
        bytes, Tuple, None
    ]:
        try:
            return self.store.get(key=key)
        except Exception as e:
            self.logger.error(f'Arsene error {e}')
            if not self.catch_errors:
                raise

    def delete(self, *, key: str) -> None:
        try:
            self.store.delete(key=key)
        except Exception as e:
            self.logger.error(f'Arsene error {e}')
            if not self.catch_errors:
                raise

    def clean_key(self, *, key: str) -> Any:
        self.delete(key=key)

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def cache(
        self, *, key: str, expire: Optional[int] = None,
        check_params: bool = False, kwargs_list: Optional[List] = None,
        check_args_params: bool = False, check_kwargs_params: bool = False
    ) -> Any:
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                name = generate_key(
                    key=key, deeper_args=args, deeper_kwargs=kwargs,
                    kwargs_list=kwargs_list, check_params=check_params,
                    check_args_params=check_args_params,
                    check_kwargs_params=check_kwargs_params
                )
                key_data = self.get(key=name)
                if key_data:
                    self.logger.info(f'Find key: {name} data: {key_data}')
                    return key_data
                elif key_data is None:
                    ex = expire if expire else self.global_expire
                    response = func(*args, **kwargs)
                    self.logger.info(f'Save key: {name} data: {key_data} expire: {ex}')
                    self.set(key=name, data=response, expire=ex)
                    return response
            return wrapper
        return decorator
