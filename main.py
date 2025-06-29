from fastapi import FastAPI
from loguru import logger

from src.routes import user_router, secure_endpoint_router
from src.config import env_vars


def create_app() -> FastAPI:
    """Create and configure an instance of the FastAPI application."""
    server = FastAPI(
        title="Wiredcraft Users API",
        description="Wiredcraft Users API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        contact={
            "name": "George Mwangi",
            "email": "mwangigeorge648@gmail.com"
        },
        license_info={
            "name": "License",
            "url": "https://opensource.org/licenses/MIT"
        }
    )

    # include routers to the app instance
    server.include_router(user_router())
    server.include_router(secure_endpoint_router())

    return server


logger.debug(f"Running in production mode: {env_vars.running_in_production}")

app = create_app()  # Application entrypoint