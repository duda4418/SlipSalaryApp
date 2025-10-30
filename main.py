import fastapi, uvicorn

from api.routers.employees import employees_router
from api.routers.health import health_router
from api.routers.idempotency_keys import idempotency_router
from api.routers.months import months_router
from api.routers.reports import reports_router
from api.routers.salary_components import salary_components_router
from api.routers.users import users_router
from api.routers.vacations import vacations_router

app = fastapi.FastAPI()

app.include_router(health_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(idempotency_router, prefix="/api")
app.include_router(salary_components_router, prefix="/api")
app.include_router(months_router, prefix="/api")
app.include_router(vacations_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(employees_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)