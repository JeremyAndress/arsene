from typing import Callable


class Base:
    def __init__(
        self, *, set_data: Callable, resolve_data: Callable,
        object_hook: Callable, json_serial: Callable
    ) -> None:
        self.set_data = set_data
        self.object_hook = object_hook
        self.json_serial = json_serial
        self.resolve_data = resolve_data
