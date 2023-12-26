from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


def enable_https_redirection(app: FastAPI):
    app.add_middleware(HTTPSRedirectMiddleware)
