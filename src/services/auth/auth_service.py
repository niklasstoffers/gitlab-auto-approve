from fastapi import Header, HTTPException, status, Depends
from typing import Annotated
from config.config_manager import get_config
from config.config import Config

GITLAB_TOKEN_HEADER = 'X-Gitlab-Token'

async def require_token(x_gitlab_token: Annotated[str | None, Header(alias = GITLAB_TOKEN_HEADER)] = None, config: Config = Depends(get_config)):
    if x_gitlab_token is None or x_gitlab_token != config.webhook_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)