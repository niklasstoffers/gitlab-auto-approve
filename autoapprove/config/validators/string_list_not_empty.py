from pydantic import ValidationError


def string_list_not_empty(value: list[str] | None) -> list[str] | None:
    for i, entry in enumerate(value or []):
        value[i] = entry.strip()
        if len(entry) == 0:
            raise ValidationError("string cannot be empty")
    return value
