from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from typing import Annotated
from comment_event import CommentEvent
from config import config
from gitlab_client import gl
from gitlab.v4.objects import Project, ProjectMergeRequest
from urllib.parse import urlparse
import uvicorn

async def verify_token(x_gitlab_token: Annotated[str | None, Header(alias = 'X-Gitlab-Token')] = None):
    if x_gitlab_token is None or x_gitlab_token != config.webhook_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

def check_comment(event: CommentEvent):
    comment: str = event.object_attributes.note
    if config.approval.ignore_case:
        comment = comment.lower()
    if config.approval.strict_match:
        return config.approval.keyword == comment
    return config.approval.keyword in comment

def check_author(event: CommentEvent):
    return config.approval.only_for_members == None or event.user.username in config.approval.only_for_members

def approve(event: CommentEvent):
    project: Project = gl.projects.get(event.project.id)
    merge_request: ProjectMergeRequest = project.mergerequests.get(event.merge_request.iid)
    if config.approval.message is not None:
        merge_request.notes.create({'body': config.approval.message})
    merge_request.approve()

app = None
if config.ssl.enable:
    app = FastAPI(ssl_keyfile=config.ssl.key_file, ssl_certfile=config.ssl.cert_file)
    app.add_middleware(HTTPSRedirectMiddleware)
else:
    app = FastAPI()

if config.trusted_hosts_only:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=[urlparse(config.gitlab_host).netloc])

origins = [config.gitlab_host]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/approve-merge", dependencies = [Depends(verify_token)])
async def approve_merge(event: CommentEvent):
    if check_author(event) and check_comment(event):
        try:
            approve(event)
        except:
            raise Exception("Failed to approve merge request")
        
if __name__ == "__main__":
    if config.ssl.enable:
        uvicorn.run("main:app", host="0.0.0.0", port=80, ssl_keyfile=config.ssl.key_file, ssl_certfile=config.ssl.cert_file)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=80)