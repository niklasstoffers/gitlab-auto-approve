from fastapi import Depends
from services.gitlab.events.comment.comment_event import CommentEvent
from services.gitlab.events.comment.comment_event_type import CommentEventType
from services.gitlab.gitlab_client import get_client, GitlabClient
from gitlab.v4.objects import ProjectMergeRequest, Project, ProjectMember
from config.config_manager import get_config
from config.config import Config
from config.commands.command import Command
from logging import Logger, DEBUG
from helpers.logging.dependencies import resolve_logger
from helpers.dump.json_dump import dump as json_dump
from services.gitlab.gitlab_role import GitlabRole

class CommentEventService():
    gitlab_client: GitlabClient
    config: Config
    logger: Logger

    def __init__(self, gitlab_client: GitlabClient, config: Config, logger: Logger):
        self.gitlab_client = gitlab_client
        self.config = config
        self.logger = logger

    def __is_command_invocation(self, event: CommentEvent, command: Command) -> bool:
        keyword: str = command.keyword
        message: str = event.object_attributes.note

        if command.ignore_case:
            self.logger.debug('Performing ignore case match for command invocation')
            keyword = keyword.lower()
            message = message.lower()
        
        is_match: bool = False
        if command.strict_match:
            is_match = keyword == message
            self.logger.debug(f'Performing strict match comparison of message "{message}" with result {is_match}')
        else:
            is_match = keyword in message
            self.logger.debug(f'Performing match comparison of message "{message}" with result {is_match}')
        
        if is_match:
            self.logger.info(f'Invocation matches command signature for command "{type(command).__name__}"')
        return is_match
    
    def __can_invoke_command(self, event: CommentEvent, command: Command) -> bool:
        can_invoke: bool = True

        if command.requires_role is not None:
            self.logger.info('Performing role check')

            project: Project = self.gitlab_client.get_project(event.project.id)
            if project is None:
                raise Exception(f"Unknown project with id {event.project.id}")
            
            project_member: ProjectMember = self.gitlab_client.get_project_member(project, event.user.id)
            if project_member is None:
                raise Exception(f"Unknown project member with id {event.user.id} for project with id {event.project.id}")
            
            can_invoke = self.gitlab_client.member_has_role(project_member, command.requires_role.get_role())
            member_role: GitlabRole = self.gitlab_client.get_role_for_member(project_member)
            if can_invoke:
                self.logger.info(f'User passed role restrictions with user role "{member_role}"')
            else:
                self.logger.info(f'Cannot invoke command due to role restriction with user role "{member_role}"')
        else:
            self.logger.info('Skipping role check because no role restrictions have been specified')

        if command.only_for_members is not None:
            self.logger.info('Performing member check')

            can_invoke = can_invoke and event.user.username in command.only_for_members
            if can_invoke:
                self.logger.info(f'User "{event.user.username}" passed member restrictions')
            else:
                self.logger.info(f'Cannot invoke command due to member restrictions for user "{event.user.username}"')
        else:
            self.logger.info('Skipping member check because no member restrictions have been specified')

        return can_invoke

    def __handle_merge_comment(self, event: CommentEvent):
        project: Project = self.gitlab_client.get_project(event.project.id)
        if project is None:
            raise Exception(f"Project with id {event.project.id} not found")
        
        merge_request: ProjectMergeRequest = self.gitlab_client.get_merge_request(project, event.merge_request.iid)
        if merge_request is None:
            raise Exception(f"Merge request with iid {event.merge_request.iid} not found for project {event.project.id}")

        if self.__is_command_invocation(event, self.config.commands.approval) and self.__can_invoke_command(event, self.config.commands.approval) and not self.gitlab_client.approved_merge_request(merge_request):
            self.logger.info('Approving merge request')
            self.gitlab_client.approve_merge_request(merge_request, self.config.commands.approval.message)
        elif self.__is_command_invocation(event, self.config.commands.disapproval) and self.__can_invoke_command(event, self.config.commands.disapproval) and self.gitlab_client.approved_merge_request(merge_request):
            self.logger.info('Disapproving merge request')
            self.gitlab_client.disapprove_merge_request(merge_request, self.config.commands.disapproval.message)
        elif self.__is_command_invocation(event, self.config.commands.merge) and self.__can_invoke_command(event, self.config.commands.merge) and self.gitlab_client.can_merge(merge_request):
            self.logger.info('Merging merge request')
            self.gitlab_client.merge(event.project.id, event.merge_request.iid, message=self.config.commands.merge.message)


    def handle_comment_event(self, event: CommentEvent):
        if self.logger.isEnabledFor(DEBUG):
            self.logger.debug(f'Got comment event with data\n{json_dump(event)}')

        if event.type == CommentEventType.MERGE_REQUEST:
            self.logger.info('Got merge request comment event')
            self.__handle_merge_comment(event)
        else:
            self.logger.info(f'Got comment event for unhandled type "{event.type}"')

service: CommentEventService | None = None

def get_service(gitlab_client: GitlabClient = Depends(get_client), config: Config = Depends(get_config), logger: Logger = Depends(resolve_logger(__name__))) -> CommentEventService:
    global service
    if service is None:
        logger.debug('Initializing comment event service')
        service = CommentEventService(gitlab_client, config, logger)
    return service