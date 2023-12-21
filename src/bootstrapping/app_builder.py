from fastapi import FastAPI
from security.cors import enable_cors
from security.https import enable_https_redirection
from security.trusted_hosts import enable_trusted_hosts_only
from logging import Logger, getLogger
from helpers.logging.factory import create_logger
from config.config import Config

class AppBuilder():
    config: Config
    logger: Logger

    def with_config(self, config: Config) -> 'AppBuilder':
        self.config = config
        return self
    
    def __configure_logging(self):
        rootLogger: Logger = getLogger(None)
        config = self.config.logging
        if config.enable and config.handlers is not None:
            handlers = config.handlers
            rootLogger = create_logger(rootLogger, 
                                    config.getLogLevel(),
                                    handlers.console is not None and handlers.console.enable,
                                    handlers.file is not None and handlers.file.enable,
                                    handlers.file.logfile if handlers.file is not None else "")
    
    def __configure_app(self, app: FastAPI):
        if self.config.trusted_hosts_only:
            host = self.config.gitlab.host.host
            self.logger.info('Enabling trusted host middleware with allowed host "%s"', host)
            enable_trusted_hosts_only(app, allowed_hosts=host)
        if self.config.ssl.enable:
            self.logger.info("Enabling HTTPS redirection")
            enable_https_redirection(app)
        
        origin = str(self.config.gitlab.host)
        self.logger.info('Enabling CORS with allowed origin set to "%s"', origin)
        enable_cors(app, origins=[origin])

    def build(self) -> FastAPI:
        self.__configure_logging()
        self.logger = getLogger(__name__)

        self.logger.info("Building app")
        app = FastAPI()

        self.logger.info("Configuring app")
        self.__configure_app(app)

        return app