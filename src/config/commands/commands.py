from pydantic import BaseModel
from config.commands.approval import Approval

class Commands(BaseModel):
    approval: Approval