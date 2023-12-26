import json
from typing import Any


def dump(obj: Any):
    return json.dumps(obj, default=lambda x: x.__dict__ if hasattr(x, "__dict__") else str(x), indent=4)
