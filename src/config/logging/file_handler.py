from pydantic import model_validator, ValidationError
from pathlib import Path
from config.logging.handler import Handler

class FileHandler(Handler):
    logfile: Path | None = None

    @model_validator(mode='after')
    def _validate(self) -> 'FileHandler':
        if self.enable and self.logfile is None:
            raise ValidationError("Log file must be specified when enabling file handler")
        return self