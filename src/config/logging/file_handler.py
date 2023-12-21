from pydantic import FilePath, model_validator, ValidationError
from config.logging.handler import Handler

class FileHandler(Handler):
    logfile: FilePath | None

    @model_validator(mode='after')
    def _validate(self) -> 'FileHandler':
        if self.enable and self.logfile is None:
            raise ValidationError("Log file must be specified when enabling file handler")
        return self