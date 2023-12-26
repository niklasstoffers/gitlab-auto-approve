from pydantic import BaseModel, StringConstraints, Field
from typing import Annotated

class Uvicorn(BaseModel):
    reload: bool
    host: Annotated[str, StringConstraints(strip_whitespace=True, pattern="^((25[0-5]|(2[0-4]|1\\d|[1-9]|)\\d)\\.?\\b){4}$")]
    port: int = Field(..., min=1, max=65535)
