from fastapi import Depends
from services.gitlab.events.comment.comment_event import CommentEvent
from services.gitlab.events.comment.comment_event_type import CommentEventType
from services.gitlab.gitlab_client import get_client, GitlabClient
from config.config_manager import get_config
from config.config import Config
from config.commands.command import Command
from typing import Callable

class CommentEventService():
    gitlab_client: GitlabClient

    def __init__(self, gitlab_client: GitlabClient):
        self.gitlab_client = gitlab_client

    def __is_command_invocation(self, event: CommentEvent, command: Command):
        keyword = command.keyword
        message = event.object_attributes.note
        if command.ignore_case:
            keyword = keyword.lower()
            message = message.lower()
        
        if command.strict_match:
            return keyword in message
        return keyword == message

    def __handle_merge_comment(self, event: CommentEvent):
        if event.merge_request is None:
            raise Exception("Invalid event object")
        config: Config = get_config()
        if self.__is_command_invocation(event, config.commands.approval):
            self.__approve_merge_request(event.project.id, event.merge_request.iid, config.commands.approval.message)


    def handle_comment_event(self, event: CommentEvent):
        if event.type == CommentEventType.MERGE_REQUEST:
            self.__handle_merge_comment(event)

service: CommentEventService | None = None

def get_service(gitlab_client: GitlabClient = Depends(get_client)) -> CommentEventService:
    if service is None:
        service = CommentEventService(gitlab_client)
    return service