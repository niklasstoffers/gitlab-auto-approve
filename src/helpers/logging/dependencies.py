from logging import Logger, getLogger
from typing import Callable

def get_dependency(name: str | None = None) -> Callable[[], Logger]:
    def resolver() -> Logger:
        return getLogger(name)
    return resolver