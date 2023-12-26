from pydantic import BaseModel, StringConstraints, HttpUrl
from typing import Annotated


class Gitlab(BaseModel):
    host: HttpUrl
    access_token: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    webhook_token: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
