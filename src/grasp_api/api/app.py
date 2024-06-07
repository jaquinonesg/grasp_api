from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from grasp_api.api import settings
from grasp_api.api.v1.provision.base.serializers import HealthCheck
from grasp_api.api.v1.provision.example import views as v1_views_example
from grasp_api.api.v1.provision.middleware.log_middleware import log_middleware
from grasp_api.config.logger import logger
from grasp_api.config.main import filter_settings
from grasp_api.db.database import (
    ReadOnlySession,
    Session,
    configure_db_session,
)


def uvicorn_entry() -> FastAPI:
    return create_app()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        debug=settings.debug,
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
    logger.info("Starting API...")
    _setup_routes(app)
    _on_startup(app)
    return app


def _setup_routes(app):
    app.include_router(
        v1_views_example.router,
        prefix="/grasp_api/v1",
        tags=["example"],
    )

    @app.get("/", response_model=HealthCheck, tags=["status"])
    async def health_check():
        return {
            "name": settings.project_name,
            "version": settings.version,
            "description": settings.description,
        }


def _on_startup(app: FastAPI):
    @app.on_event("startup")
    async def configure_db():
        configure_db_session(Session, filter_settings("grasp_api_db_"))
        configure_db_session(
            ReadOnlySession, filter_settings("grasp_api_db_ro_")
        )
