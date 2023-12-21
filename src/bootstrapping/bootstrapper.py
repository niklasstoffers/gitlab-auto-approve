from fastapi import FastAPI
from security.cors import enable_cors
from security.https import enable_https_redirection
from security.trusted_hosts import enable_trusted_hosts_only
from logging import Logger, getLogger, FileHandler, StreamHandler
from uvicorn.logging import DefaultFormatter
from config.config import Config
import sys

def configure_logging(config: Config, logger: Logger):
    logger.info('Configuring logging')
    rootLogger: Logger = getLogger(None)

    if config.logging.enable:
        logger.info('Enabling logging')
        rootLogger.setLevel(config.logging.getLogLevel())
        handlers = config.logging.handlers

        if handlers is not None:
            formatter = DefaultFormatter(fmt="%(levelprefix)s [%(name)s] %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            if handlers.console is not None and handlers.console.enable:
                logger.info('Using console handler')
                console_handler: StreamHandler = StreamHandler(stream=sys.stdout)
                console_handler.setFormatter(formatter)
                rootLogger.addHandler(console_handler)
            if handlers.file is not None and handlers.file.enable:
                logger.info('Using file handler with file "%s"', handlers.file.logfile)
                file_handler: FileHandler = FileHandler(filename=handlers.file.logfile)
                file_handler.setFormatter(formatter)
                rootLogger.addHandler(file_handler)

def configure_app(app: FastAPI, config: Config):
    logger: Logger = getLogger(__name__)
    if config.trusted_hosts_only:
        host = config.gitlab.host.host
        logger.info('Enabling trusted host middleware with allowed host "%s"', host)
        enable_trusted_hosts_only(app, allowed_hosts=host)
    if config.ssl.enable:
        logger.info("Enabling HTTPS redirection")
        enable_https_redirection(app)
    
    origin = str(config.gitlab.host)
    logger.info('Enabling CORS with allowed origin set to "%s"', origin)
    enable_cors(app, origins=[origin])