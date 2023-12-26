from pydantic import BaseModel


class MergeRequest(BaseModel):
    iid: int
