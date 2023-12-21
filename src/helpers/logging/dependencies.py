from logging import Logger, getLogger
from typing import Callable

def resolve_logger(name: str | None = None) -> Callable[[], Logger]:
    def resolver() -> Logger:
        return getLogger(name)
    return resolver