from pydantic import BaseModel, StringConstraints
from typing import Annotated

class ObjectAttributes(BaseModel):
    note: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]