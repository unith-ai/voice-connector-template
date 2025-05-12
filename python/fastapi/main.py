import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(router)


def create_app() -> FastAPI:
    logger.info("Initializing FastAPI app")

    app = FastAPI(
        title="Fast Api Template Api Gateway",
        description="Fast Api Template Api Gateway",
        version="0.0.1",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    init_routers(app=app)
    init_cors(app=app)
    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        workers=0,
        factory=True,
    )
