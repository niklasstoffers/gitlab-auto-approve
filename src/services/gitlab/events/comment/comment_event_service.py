from services.gitlab.events.comment.comment_event import CommentEvent
from services.gitlab.events.comment.comment_event_type import CommentEventType
from services.gitlab.gitlab_client import approve_merge_request
from config.config_manager import get_config
from config.config import Config
from config.commands.command import Command
from typing import Callable


def _is_command_invocation(event: CommentEvent, command: Command):
    keyword = command.keyword
    message = event.object_attributes.note
    if command.ignore_case:
        keyword = keyword.lower()
        message = message.lower()
    
    if command.strict_match:
        return keyword in message
    return keyword == message

def _handle_merge_comment(event: CommentEvent):
    if event.merge_request is None:
        raise Exception("Invalid event object")
    config: Config = get_config()
    if _is_command_invocation(event, config.commands.approval):
        approve_merge_request(event.project.id, event.merge_request.iid, config.commands.approval.message)


def handle_comment_event(event: CommentEvent):
    if event.type == CommentEventType.MERGE_REQUEST:
        _handle_merge_comment(event)

def get_handler() -> Callable[[CommentEvent]]:
    return handle_comment_event