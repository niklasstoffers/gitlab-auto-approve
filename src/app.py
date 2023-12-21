from bootstrapping.app_builder import AppBuilder
from routes.comment import router as comment_router
from config.config_manager import get_config
from logging import Logger, getLogger


app = AppBuilder()              \
    .with_config(get_config())  \
    .build()
app.include_router(comment_router)

logger: Logger = getLogger(__name__)
logger.info("Application startup complete")