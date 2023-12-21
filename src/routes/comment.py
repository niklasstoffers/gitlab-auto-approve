from fastapi import APIRouter, Depends
from services.gitlab.events.comment.comment_event import CommentEvent
from services.auth.auth_service import require_token
from helpers.logging.dependencies import resolve_logger
from logging import Logger


router = APIRouter(prefix="/comment", tags=["comment"])

@router.post('/')
def comment_webhook(event: CommentEvent, logger: Logger = Depends(resolve_logger(__name__)), authorized = Depends(require_token)):
    return "test"