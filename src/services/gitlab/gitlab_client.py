from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectMergeRequest, ProjectMergeRequestApproval
from fastapi import Depends
from logging import Logger
from helpers.logging.dependencies import resolve_logger
from config.config import config

class GitlabClient():
    client: Gitlab

    def __init__(self, client: Gitlab):
        self.client = client

    def connect(self):
        self.client.auth()

    def get_merge_request(self, project_id: int, merge_request_iid: int) -> ProjectMergeRequest:
        project: Project = self.client.projects.get(project_id)
        return project.mergerequests.get(merge_request_iid)

    def is_merge_request_approved_by(self, merge_request: ProjectMergeRequest, username: str) -> bool:
        approvals: ProjectMergeRequestApproval = merge_request.approvals.get()
        for approval in approvals.attributes["approved_by"]:
            if approval.user is not None and approval.user.username == username:
                return True
        return False

    def get_current_username(self, ) -> str:
        return self.client.user.attributes["username"]

    def approve_merge_request(self, project_id: int, merge_request_iid: int, message: str | None = None):
        merge_request: ProjectMergeRequest = self.get_merge_request(project_id, merge_request_iid)
        if self.is_merge_request_approved_by(merge_request, self.get_current_username()):
            raise Exception("Merge request has already been approved by user")
        if message is not None:
            merge_request.notes.create({'body': message})
        merge_request.approve()

    def disapprove_merge_request(self, project_id: int, merge_request_iid: int, message: str | None = None):
        merge_request: ProjectMergeRequest = self.get_merge_request(project_id, merge_request_iid)
        if not self.is_merge_request_approved_by(merge_request, self.get_current_username()):
            raise Exception("Merge request is not approved by user")
        if message is not None:
            merge_request.notes.create({'body': message})
        merge_request.unapprove()

    def merge(self, project_id: int, merge_request_iid: int, only_when_pipeline_succeeds: bool = True, remove_source_branch: bool = True, message: str | None = None):
        merge_request: ProjectMergeRequest = self.get_merge_request(project_id, merge_request_iid)
        if message is not None:
            merge_request.notes.create({'body': message})
        merge_request.merge(should_remove_source_branch=remove_source_branch, merge_when_pipeline_succeeds=only_when_pipeline_succeeds)

    def cancel_merge(self, project_id: int, merge_request_iid: int, message: str | None = None):
        merge_request: ProjectMergeRequest = self.get_merge_request(project_id, merge_request_iid)
        if message is not None:
            merge_request.notes.create({'body', message})
        merge_request.cancel_merge_when_pipeline_succeeds()


client: GitlabClient = None

def get_client(logger: Logger = Depends(resolve_logger(__name__))) -> GitlabClient:
    if client is None:
        logger.info('Creating gitlab client')
        gl = Gitlab(config.gitlab_host, private_token=config.access_token)
        client = GitlabClient(gl)
        try:
            logger.info('Connecting to gitlab')
            client.connect()
        except Exception as e:
            logger.error('Failed to connect to gitlab', exc_info=e)
            raise Exception("Failed to connect to gitlab")
    return client