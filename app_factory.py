"""Application factory for creating FastAPI app instances.

Using a factory avoids side effects (like starting logging or importing heavy modules)
when tests import the application. Tests can call `create_app()` to get an
isolated instance and override dependencies.
"""
import fastapi
from fastapi.middleware.cors import CORSMiddleware

from core.logging import configure_logging, RequestLoggingMiddleware
from api.routers.employees import employees_router
from api.routers.health import health_router
from api.routers.idempotency_keys import idempotency_router
from api.routers.months import months_router
from api.routers.reports import reports_router
from api.routers.report_generation import report_generation_router
from api.routers.salary_components import salary_components_router
from api.routers.vacations import vacations_router
from api.routers.auth import auth_router


def create_app() -> fastapi.FastAPI:
    configure_logging()
    app = fastapi.FastAPI()
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[],
    )
    # Routers
    app.include_router(health_router, prefix="/api")
    app.include_router(idempotency_router, prefix="/api")
    app.include_router(salary_components_router, prefix="/api")
    app.include_router(months_router, prefix="/api")
    app.include_router(vacations_router, prefix="/api")
    app.include_router(reports_router, prefix="/api")
    app.include_router(employees_router, prefix="/api")
    app.include_router(report_generation_router, prefix="/api")
    app.include_router(auth_router, prefix="/api")
    return app
