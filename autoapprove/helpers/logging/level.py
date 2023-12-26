from logging import getLevelNamesMapping


def get_level_from_name(name: str) -> int | None:
    mappings = getLevelNamesMapping()
    if name in mappings:
        return mappings[name]
    return None
