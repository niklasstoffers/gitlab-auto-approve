from services.gitlab.events.comment.comment_event import CommentEvent
from services.gitlab.events.comment.comment_event_type import CommentEventType
from services.gitlab.gitlab_client import approve_merge_request
from config.config_manager import get_config
from config.config import Config

def _handle_merge_comment(event: CommentEvent):
    if event.merge_request is None:
        raise Exception("Invalid event object")
    config: Config = get_config()
    approve_merge_request(event.project.id, event.merge_request.iid, config.commands.approval.message)


def handle_comment_event(event: CommentEvent):
    if event.type == CommentEventType.MERGE_REQUEST:
        _handle_merge_comment(event)