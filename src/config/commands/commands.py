from pydantic import BaseModel
from config.commands.approval import Approval
from config.commands.disapproval import Disapproval
from config.commands.merge import Merge

class Commands(BaseModel):
    approval: Approval
    disapproval: Disapproval
    merge: Merge