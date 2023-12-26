from pydantic import BaseModel
from os import environ
from typing import Any, cast
from config.config import Config
from helpers.type import is_of_type_or_generic_of_type, is_optional, unpack_optional

def _parse_as_list(value: str) -> list[str]:
    value = value.strip("[]")
    return [x.strip() for x in value.split(',') if len(x.strip()) > 0]

def _load_environment_variable(section: dict[str, Any], env_var_name: str, attribute: str, type: type) -> bool:
    value: str = environ.get(env_var_name, None)
    if value is None or len(value.strip()) == 0:
        return False
    
    value = value.strip()
    if is_optional(type):
        type = unpack_optional(type)

    if is_of_type_or_generic_of_type(type, list):
        section[attribute] = _parse_as_list(value)
    else:
        section[attribute] = value
    return True

def _is_model(t: type) -> (bool, type):
    model_type: type = t
    if is_optional(t):
        model_type = unpack_optional(t)
    if isinstance(model_type, type) and issubclass(model_type, BaseModel):
        return True, model_type
    return False, None

def _load_environment_helper(section: dict[str, Any], section_type: BaseModel, separator: str, prefix: str = "") -> bool:
    loaded_field = False
    for field_name, field_info in section_type.model_fields.items():
        field_type = field_info.annotation
        is_model, model_type = _is_model(field_type)
        if is_model:
            field_was_none = not field_name in section
            if field_was_none:
                section[field_name] = dict()
            loaded_sub_field = _load_environment_helper(section[field_name], cast(BaseModel, model_type), separator, f"{prefix}{field_name}{separator}")
            if not loaded_sub_field and field_was_none:
                del section[field_name]
        else:
            loaded_field = _load_environment_variable(section, (prefix + field_name).upper(), field_name, field_type) or loaded_field
    return loaded_field


def load_environment(config: dict[str, Any], separator: str = "__"):
    _load_environment_helper(config, Config, separator)