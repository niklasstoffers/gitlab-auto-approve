from fastapi import FastAPI, Depends, Request, Header, HTTPException, status
from typing import Annotated
from comment_event import CommentEvent
from config import config
from gitlab_client import gl
from gitlab.v4.objects import Project, ProjectMergeRequest

async def verify_token(x_gitlab_token: Annotated[str | None, Header()] = None):
    if x_gitlab_token is None or x_gitlab_token != config.webhook_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

async def check_comment(event: CommentEvent):
    comment: str = event.object_attributes.note
    if config.approval.ignore_case:
        comment = comment.lower()
    if config.approval.strict_match:
        return config.approval.keyword == comment
    return config.approval.keyword in comment

async def check_author(event: CommentEvent):
    return config.approval.only_for_members == None or event.user.username in config.approval.only_for_members

async def approve(event: CommentEvent):
    project: Project = gl.projects.get(event.project.id)
    merge_request: ProjectMergeRequest = project.mergerequests.get(event.merge_request.id)
    if config.approval.message is not None:
        merge_request.notes.create({'body': config.approval.message})
    merge_request.approve()

app = FastAPI()

@app.post("/approve-merge", dependencies = [Depends(verify_token)])
async def root(event: CommentEvent):
    if check_author(event) and check_comment(event):
        try:
            approve(event)
        except:
            raise Exception("Failed to approve merge request")