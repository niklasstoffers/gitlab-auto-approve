from pydantic import BaseModel, StringConstraints
from typing import Annotated


class User(BaseModel):
    id: int
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
