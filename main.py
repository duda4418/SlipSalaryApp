import uvicorn
from app_factory import create_app

# Single app instance for production run; tests should import create_app directly.
app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)