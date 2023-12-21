from abc import ABC
from pydantic import StringConstraints
from typing import Annotated
from config.commands.command import Command

class RespondableCommand(Command, ABC):
    message: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1)]