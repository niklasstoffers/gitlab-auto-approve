from logging import Logger, DEBUG
from config.config import Config
from config.config_manager import get_config, init as init_config_manager
from helpers.dump.json_dump import dump
from helpers.logging.factory import create_logger
import uvicorn

class StartupLoggerConfig():
    enable: bool
    enable_file_logs: bool
    file: str

    def __init__(self, disable: bool, disable_file_logs: bool, file: str):
        self.enable = disable
        self.enable_file_logs = disable_file_logs
        self.file = file

class Startup():
    config_file: str
    startup_logger_config: StartupLoggerConfig

    def with_startup_logger(self, loggerConfig: StartupLoggerConfig) -> 'Startup':
        self.startup_logger_config = loggerConfig
        return self
    
    def with_config(self, config_file: str) -> 'Startup':
        self.config_file = config_file
        return self
    
    def __run_app(self, config: Config, logger: Logger):
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
        config = self.startup_logger_config
        startup_logger: Logger = Logger('$startup')
        startup_logger = create_logger(startup_logger, 
                                       DEBUG, 
                                       config.enable, 
                                       config.enable and config.enable_file_logs, 
                                       config.file)
        return startup_logger
        

    def run(self):
        logger = self.__get_startup_logger()
        logger.info("Performing startup")
        init_config_manager(self.config_file, logger)
        config = get_config()

        if logger.isEnabledFor(DEBUG):
            logger.debug("Running with configuration:\n%s", dump(config))

        self.__run_app(config, logger)