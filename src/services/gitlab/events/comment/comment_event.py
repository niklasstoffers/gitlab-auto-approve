from functools import cached_property
from pydantic import BaseModel
from services.gitlab.events.comment.models.merge_request import MergeRequest
from services.gitlab.events.comment.models.object_attributes import ObjectAttributes
from services.gitlab.events.comment.comment_event_type import CommentEventType
from services.gitlab.events.comment.models.user import User
from services.gitlab.events.comment.models.project import Project

class CommentEvent(BaseModel):
    user: User
    project: Project
    object_attributes: ObjectAttributes
    merge_request: MergeRequest | None

    @cached_property
    def type(self) -> CommentEventType:
        for type in CommentEventType:
            if getattr(self, type.value, None) is not None:
                return type
        return CommentEventType.NONE