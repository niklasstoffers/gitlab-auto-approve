from fastapi import Header, HTTPException, status, Depends
from typing import Annotated
from config.config_manager import get_config
from config.config import Config
from logging import Logger
from helpers.logging.dependencies import resolve_logger

GITLAB_TOKEN_HEADER = 'X-Gitlab-Token'


async def require_token(x_gitlab_token: Annotated[str | None, Header(alias=GITLAB_TOKEN_HEADER)] = None, config: Config = Depends(get_config), logger: Logger = Depends(resolve_logger(__name__))):
    if x_gitlab_token is None or x_gitlab_token != config.gitlab.webhook_token:
        logger.debug("Authorization error")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    logger.debug("Authorization successfull")
