from fastapi import FastAPI
from bootstrapping.bootstrapper import configure_app
from routes.comment import router as comment_router
from config.config_manager import get_config
from logging import Logger, getLogger

logger: Logger = getLogger(__name__)

logger.info("Creating app")
app = FastAPI()
logger.info("Configuring app")
configure_app(app, get_config())

app.include_router(comment_router)