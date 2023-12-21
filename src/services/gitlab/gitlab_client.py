from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectMergeRequest, ProjectMergeRequestApproval
from config.config import config

def connect() -> Gitlab:
    gl = Gitlab(config.gitlab_host, private_token=config.access_token)
    try:
        gl.auth()
    except:
        raise Exception("Failed to connect to gitlab server. Please check your gitlab configuration.")
    return gl

gl: Gitlab = connect()

def get_merge_request(project_id: int, merge_request_iid: int) -> ProjectMergeRequest:
    project: Project = gl.projects.get(project_id)
    return project.mergerequests.get(merge_request_iid)

def is_merge_request_approved_by(merge_request: ProjectMergeRequest, username: str) -> bool:
    approvals: ProjectMergeRequestApproval = merge_request.approvals.get()
    for approval in approvals.attributes["approved_by"]:
        if approval.user is not None and approval.user.username == username:
            return True
    return False

def get_current_username() -> str:
    return gl.user.attributes["username"]

def approve_merge_request(project_id: int, merge_request_iid: int, message: str | None = None):
    merge_request: ProjectMergeRequest = get_merge_request(project_id, merge_request_iid)
    if is_merge_request_approved_by(merge_request, get_current_username()):
        raise Exception("Merge request has already been approved by user")
    if message is not None:
        merge_request.notes.create({'body': message})
    merge_request.approve()

def disapprove_merge_request(project_id: int, merge_request_iid: int, message: str | None = None):
    merge_request: ProjectMergeRequest = get_merge_request(project_id, merge_request_iid)
    if not is_merge_request_approved_by(merge_request, get_current_username()):
        raise Exception("Merge request is not approved by user")
    if message is not None:
        merge_request.notes.create({'body': message})
    merge_request.unapprove()

def merge(project_id: int, merge_request_iid: int, only_when_pipeline_succeeds: bool = True, remove_source_branch: bool = True, message: str | None = None):
    merge_request: ProjectMergeRequest = get_merge_request(project_id, merge_request_iid)
    if message is not None:
        merge_request.notes.create({'body': message})
    merge_request.merge(should_remove_source_branch=remove_source_branch, merge_when_pipeline_succeeds=only_when_pipeline_succeeds)

def cancel_merge(project_id: int, merge_request_iid: int, message: str | None = None):
    merge_request: ProjectMergeRequest = get_merge_request()
    if message is not None:
        merge_request.notes.create({'body', message})
    merge_request.cancel_merge_when_pipeline_succeeds()