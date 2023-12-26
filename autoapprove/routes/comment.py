from fastapi import APIRouter, Depends
from services.gitlab.events.comment.comment_event import CommentEvent
from services.auth.auth_service import require_token
from helpers.logging.dependencies import resolve_logger
from services.gitlab.events.comment.comment_event_service import CommentEventService, get_service
from logging import Logger


router = APIRouter(prefix="/comment", tags=["comment"])


@router.post('/')
def comment_webhook(event: CommentEvent, comment_event_service: CommentEventService = Depends(get_service), logger: Logger = Depends(resolve_logger(__name__)), authorized=Depends(require_token)):
    try:
        comment_event_service.handle_comment_event(event)
    except Exception as e:
        logger.error("Failed to handle comment", exc_info=e)
        raise Exception("Failed to handle comment event")
