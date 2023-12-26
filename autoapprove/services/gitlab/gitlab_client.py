from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectMergeRequest, ProjectMergeRequestApproval, ProjectMember
from fastapi import Depends
from logging import Logger
from helpers.logging.dependencies import resolve_logger
from config.config_manager import get_config
from config.config import Config
from services.gitlab.gitlab_role import GitlabRole
from services.gitlab.merge_request_status import MergeRequestStatus


class GitlabClient():
    client: Gitlab
    logger: Logger

    def __init__(self, client: Gitlab, logger: Logger):
        self.client = client
        self.logger = logger

    def connect(self):
        self.client.auth()

    def get_project(self, project_id: int) -> Project | None:
        return self.client.projects.get(project_id)

    def get_merge_request(self, project: Project, merge_request_iid: int) -> ProjectMergeRequest | None:
        return project.mergerequests.get(merge_request_iid)

    def is_merge_request_approved_by(self, merge_request: ProjectMergeRequest, username: str) -> bool:
        approvals: ProjectMergeRequestApproval = merge_request.approvals.get()
        self.logger.debug(f'Checking approvals for merge request {merge_request.get_id()} with approvals "{approvals.attributes["approved_by"]}"')
        for approval in approvals.attributes["approved_by"]:
            if approval['user']['username'] == username:
                return True
        return False

    def get_current_username(self) -> str:
        return self.client.user.attributes["username"]

    def get_project_member(self, project: Project, user_id: int) -> ProjectMember | None:
        return project.members.get(user_id)

    def get_role_for_member(self, project_member: ProjectMember) -> GitlabRole:
        return GitlabRole(project_member.attributes['access_level'])

    def member_has_role(self, project_member: ProjectMember, role: GitlabRole, exact_rule: bool = False) -> bool:
        access_level: int = project_member.attributes['access_level']
        self.logger.debug(f'Checking access level for project member {project_member.get_id()} with access level "{access_level}"')
        if exact_rule:
            return access_level == role
        return GitlabRole(access_level).is_higher_than(role)

    def approved_merge_request(self, merge_request: ProjectMergeRequest) -> bool:
        return self.is_merge_request_approved_by(merge_request, self.get_current_username())

    def approve_merge_request(self, merge_request: ProjectMergeRequest, message: str | None = None):
        if message is not None:
            merge_request.notes.create({'body': message})
        merge_request.approve()

    def disapprove_merge_request(self, merge_request: ProjectMergeRequest, message: str | None = None):
        if message is not None:
            merge_request.notes.create({'body': message})
        merge_request.unapprove()

    def is_mergeable_or_future_mergeable(self, merge_request: ProjectMergeRequest) -> bool:
        merge_status: str = merge_request.attributes['detailed_merge_status']
        self.logger.debug(f'Checking merge status for merge request {merge_request.get_id()} with merge status "{merge_status}"')
        return merge_status in [MergeRequestStatus.MERGEABLE, MergeRequestStatus.CI_MUST_PASS, MergeRequestStatus.CI_STILL_RUNNING]

    def can_merge(self, merge_request: ProjectMergeRequest) -> bool:
        return self.is_mergeable_or_future_mergeable(merge_request) and not merge_request.attributes['merge_when_pipeline_succeeds']

    def can_cancel_merge(self, merge_request: ProjectMergeRequest) -> bool:
        return self.is_mergeable_or_future_mergeable(merge_request) and merge_request.attributes['merge_when_pipeline_succeeds']

    def merge(self, merge_request: ProjectMergeRequest, only_when_pipeline_succeeds: bool = True, remove_source_branch: bool = True, message: str | None = None):
        if message is not None:
            merge_request.notes.create({'body': message})
        merge_request.merge(should_remove_source_branch=remove_source_branch, merge_when_pipeline_succeeds=only_when_pipeline_succeeds)

    def cancel_merge(self, merge_request: ProjectMergeRequest, message: str | None = None):
        if message is not None:
            merge_request.notes.create({'body', message})
        merge_request.cancel_merge_when_pipeline_succeeds()


client: GitlabClient = None


def get_client(logger: Logger = Depends(resolve_logger(__name__)), config: Config = Depends(get_config)) -> GitlabClient:
    global client
    if client is None:
        logger.info('Creating gitlab client')
        gl = Gitlab(str(config.gitlab.host), private_token=config.gitlab.access_token)
        client = GitlabClient(gl, logger)
        try:
            logger.info('Connecting to gitlab')
            client.connect()
        except Exception as e:
            logger.error('Failed to connect to gitlab', exc_info=e)
            raise Exception("Failed to connect to gitlab")
    return client
