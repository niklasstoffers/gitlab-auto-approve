from config.config import Config
import yaml
from pydantic import ValidationError
from logging import Logger


_config: Config | None = None

def _load_config(filename: str, logger: Logger) -> Config:
    try:
        logger.info('Loading configuration from file "%s"', filename)
        with open(filename) as config_file:
            yaml_config = yaml.safe_load(config_file.read())
            config: Config = Config(**yaml_config)
            return config
    except ValidationError as e:
        logger.error('Failed to load configuration', exc_info=e)
        raise Exception("Failed to load configuration file. Please check your settings")

def init(filename: str, logger: Logger):
    global _config
    _config = _load_config(filename, logger)

def get_config() -> Config:
    if _config is None:
        raise Exception("Configuration has not been loaded")
    return _config