from pydantic import BaseModel

class Handler(BaseModel):
    enable: bool