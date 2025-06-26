from fastapi import FastAPI
from src.routes import user_router


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

    return server


# Application entrypoint
app = create_app()