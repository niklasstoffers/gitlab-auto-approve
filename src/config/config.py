from pydantic import BaseModel
from config.gitlab import Gitlab
from config.environment import Environment
from config.ssl import SSL
from config.commands.commands import Commands
from config.uvicorn import Uvicorn
from config.logging.logging import Logging

class Config(BaseModel):
    gitlab: Gitlab
    trusted_hosts_only: bool
    environment: Environment
    ssl: SSL
    commands: Commands
    uvicorn: Uvicorn
    logging: Logging