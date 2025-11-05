from fastapi import APIRouter, Depends
from auth.deps import require_manager

health_router = APIRouter(prefix="/health", dependencies=[Depends(require_manager)])

@health_router.get("")
async def health_check():
    return {"status": "ok"}