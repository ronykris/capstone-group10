from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_routes import router as api_router
from app.utils.logger import get_logger
from app.utils.config import config
import os

logger = get_logger(__name__)

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    :return: Configured FastAPI application
    """
    # Initialize FastAPI app
    app = FastAPI(
        title="Food Recognition API",
        description="API for food recognition and segmentation",
        version="1.0.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.get("api", "allowed_origins"),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(
        api_router,
        prefix=config.get("api", "prefix")
    )

    # Startup event
    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up the application...")
        # Verify environment variables
        if not config.get("fal", "api_key"):
            logger.warning("FAL API key is not configured!")

    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down the application...")

    return app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    # Run the application using uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.get("app", "host"),
        port=config.get("app", "port"),
        reload=config.get("app", "debug"),
        log_level=config.get("logging", "level").lower()
    )
