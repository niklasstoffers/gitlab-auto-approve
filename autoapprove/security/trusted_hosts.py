from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware


def enable_trusted_hosts_only(app: FastAPI, allowed_hosts: list[str]):
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
