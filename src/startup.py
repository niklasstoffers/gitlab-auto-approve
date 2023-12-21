from logging import Logger, getLogger, NullHandler, getHandlerByName, DEBUG
from config.config import Config
from config.config_manager import get_config, init as init_config_manager
from bootstrapping.bootstrapper import configure_logging
from helpers.dump.json_dump import dump
import uvicorn

class StartupLoggerConfig():
    disable: bool
    disable_file_logs: bool

    def __init__(self, disable: bool, disable_file_logs: bool):
        self.disable = disable
        self.disable_file_logs = disable_file_logs

class Startup():
    config_file: str
    startup_logger_config: StartupLoggerConfig

    def with_startup_logger(self, loggerConfig: StartupLoggerConfig) -> 'Startup':
        self.startup_logger_config = loggerConfig
        return self
    
    def with_config(self, config_file: str) -> 'Startup':
        self.config_file = config_file
        return self
    
    def __run_app(self, config: Config):
        logger: Logger = getLogger(__name__)
        cert_file: str | None = None
        key_file: str | None = None

        if config.ssl.enable:
            logger.info("Launching uvicorn with SSL")
            cert_file = config.ssl.cert_file
            key_file = config.ssl.key_file
        else:
            logger.info("Launching uvicorn")
        
        uvicorn.run("app:app", 
                    host=config.uvicorn.host, 
                    port=config.uvicorn.port,
                    ssl_certfile=cert_file,
                    ssl_keyfile=key_file,
                    reload=config.uvicorn.reload,
                    log_config="log_config.yaml"
        )

    def __get_startup_logger(self) -> Logger:
        startup_logger: Logger = getLogger('$startup')
        if self.startup_logger_config.disable_file_logs:
            print("disabling file")
            startup_file_handler = getHandlerByName('startup_file')
            startup_logger.removeHandler(startup_file_handler)
        if self.startup_logger_config.disable:
            print("disabling")
            for handler in startup_logger.handlers:
                startup_logger.removeHandler(handler)
            startup_logger.addHandler(NullHandler())
        return startup_logger

    def run(self):
        startup_logger = self.__get_startup_logger()
        init_config_manager(self.config_file, startup_logger)
        config = get_config()
        
        configure_logging(config, startup_logger)
        logger: Logger = getLogger(__name__)

        if logger.isEnabledFor(DEBUG):
            logger.debug("Running with configuration:\n%s", dump(config))

        self.__run_app(config)