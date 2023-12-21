from fastapi import APIRouter, Depends
from services.gitlab.events.comment.comment_event import CommentEvent
from services.auth.auth_service import require_token
from helpers.logging.dependencies import get_dependency
from logging import Logger


router = APIRouter(prefix="/comment", tags=["comment"])

@router.post('/')
def comment_webhook(event: CommentEvent, logger: Logger = Depends(get_dependency(__name__)), dependencies = [Depends(require_token)]):
    return "test"