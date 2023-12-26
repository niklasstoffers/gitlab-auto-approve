from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from logging import Logger, getLogger

class ExceptionLoggerMiddleware(BaseHTTPMiddleware):
    logger: Logger

    def __init__(self, app):
        super().__init__(app)
        self.logger = getLogger(__name__)
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            self.logger.error("Exception occured during request handling", exc_info=e)
            return Response("Internal server error", status_code=500)