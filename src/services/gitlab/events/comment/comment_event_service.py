from fastapi import Depends
from services.gitlab.events.comment.comment_event import CommentEvent
from services.gitlab.events.comment.comment_event_type import CommentEventType
from services.gitlab.gitlab_client import get_client, GitlabClient
from config.config_manager import get_config
from config.config import Config
from config.commands.command import Command

class CommentEventService():
    gitlab_client: GitlabClient
    config: Config

    def __init__(self, gitlab_client: GitlabClient, config: Config):
        self.gitlab_client = gitlab_client
        self.config = config

    def __is_command_invocation(self, event: CommentEvent, command: Command):
        keyword = command.keyword
        message = event.object_attributes.note
        if command.ignore_case:
            keyword = keyword.lower()
            message = message.lower()
        
        if command.strict_match:
            return keyword == message
        return keyword in message

    def __handle_merge_comment(self, event: CommentEvent):
        if event.merge_request is None:
            raise Exception("Invalid event object")
        if self.__is_command_invocation(event, self.config.commands.approval):
            self.gitlab_client.approve_merge_request(event.project.id, event.merge_request.iid, self.config.commands.approval.message)
        elif self.__is_command_invocation(event, self.config.commands.disapproval):
            self.gitlab_client.disapprove_merge_request(event.project.id, event.merge_request.iid, self.config.commands.disapproval.message)
        elif self.__is_command_invocation(event, self.config.commands.merge):
            self.gitlab_client.merge(event.project.id, event.merge_request.iid, message=self.config.commands.merge.message)


    def handle_comment_event(self, event: CommentEvent):
        if event.type == CommentEventType.MERGE_REQUEST:
            self.__handle_merge_comment(event)

service: CommentEventService | None = None

def get_service(gitlab_client: GitlabClient = Depends(get_client), config: Config = Depends(get_config)) -> CommentEventService:
    global service
    if service is None:
        service = CommentEventService(gitlab_client, config)
    return service