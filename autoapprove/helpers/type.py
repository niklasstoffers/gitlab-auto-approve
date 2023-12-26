from typing import Union, cast, Any, get_origin, get_args
from types import UnionType


def is_of_type_or_generic_of_type(type: type, of_type: type):
    return type is of_type or get_origin(type) is of_type


def is_optional(t: type) -> bool:
    return type(t) is UnionType or get_origin(t) is Union and len(get_args(t)) == 2 and type(None) in get_args(t)


def unpack_optional(t: Any | None):
    args = cast(list, list(t.__args__))
    args.remove(type(None))
    return args[0]
