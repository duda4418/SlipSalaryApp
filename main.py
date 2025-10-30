import fastapi, uvicorn

from routers.health import health_router

app = fastapi.FastAPI()

app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)