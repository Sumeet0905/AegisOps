from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import routes_health, routes_triage
from app.db.session import close_pool
from app.settings import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    close_pool()


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title="AI Ops Suite",
        version="0.1.0",
        debug=settings.app_env == "dev",
        lifespan=lifespan,
    )
    application.include_router(routes_health.router)
    application.include_router(routes_triage.router, prefix="/api/v1")
    return application


app = create_app()
