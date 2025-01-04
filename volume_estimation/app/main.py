from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .api.api_routes import router
from .utils.logger import setup_logger
from .utils.config import settings

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    # Initialize FastAPI app with configuration
    app = FastAPI(
        title=settings.app.name,
        description=settings.app.description,
        version=settings.app.version,
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )

    # Setup CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup routes
    app.include_router(router, prefix=settings.api.prefix)

    # Setup logging
    setup_logger()

    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting {settings.app.name} v{settings.app.version}")
        logger.info(f"Debug mode: {settings.app.debug}")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info(f"Shutting down {settings.app.name}")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.debug
    )