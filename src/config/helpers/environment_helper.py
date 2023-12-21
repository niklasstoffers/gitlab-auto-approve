from os import environ

def get_bool(env_name: str, default_value: bool) -> bool:
    return environ.get(env_name, str(default_value)).lower() == 'true'

def get_list(env_name: str, default_value: list[str] | None) -> list[str] | None:
    env_value: str | None = environ.get(env_name)
    if env_value is None or len(env_value.strip()) == 0:
        return default_value
    return [s.strip() for s in env_value.strip().split(',')]

def get_string_not_empty(env_name: str, default_value: str | None) -> str | None:
    value = environ.get(env_name, default_value)
    if value is not None:
        value = value.strip()
        if len(value) == 0:
            value = None
    return value