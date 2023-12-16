from pydantic import BaseModel

class User(BaseModel):
    username: str

class Project(BaseModel):
    id: int

class ObjectAttributes(BaseModel):
    note: str

class MergeRequest(BaseModel):
    iid: int

class CommentEvent(BaseModel):
    user: User
    project: Project
    object_attributes: ObjectAttributes
    merge_request: MergeRequest | None