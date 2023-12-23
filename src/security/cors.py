from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def enable_cors(app: FastAPI, origins: list[str]):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )