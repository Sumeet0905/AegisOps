from fastapi import FastAPI

from app.api import routes_health
from app.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="AI Ops Suite", debug=settings.app_env == "dev")
    app.include_router(routes_health.router)
    return app


app = create_app()