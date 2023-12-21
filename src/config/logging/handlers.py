from pydantic import BaseModel
from config.logging.file_handler import FileHandler
from config.logging.console_handler import ConsoleHandler

class Handlers(BaseModel):
    console: ConsoleHandler | None
    file: FileHandler | None