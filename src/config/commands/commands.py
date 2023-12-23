from pydantic import BaseModel
from config.commands.approval import Approval
from config.commands.disapproval import Disapproval

class Commands(BaseModel):
    approval: Approval
    disapproval: Disapproval