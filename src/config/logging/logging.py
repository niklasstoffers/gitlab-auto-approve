from pydantic import BaseModel, model_validator, ValidationError
from config.logging.handlers import Handlers
from logging import getLevelNamesMapping
from helpers.logging.level import get_level_from_name

class Logging(BaseModel):
    enable: bool
    level: str | None
    handlers: Handlers | None
    _level: int | None
            

    @model_validator(mode='after')
    def _validate(self) -> 'Logging':
        if self.enable:
            if self.level is None:
                raise ValidationError("Log level must be specified when enabling logging")
            else:
                level = get_level_from_name(self.level)
                if level is None:
                    raise ValidationError("Invalid log level")
                self._level = level
        
        return self

    
    def getLogLevel(self) -> int:
        return self._level