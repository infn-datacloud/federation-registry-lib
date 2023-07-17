from fastapi import APIRouter
from app.user_group.api.v1.endpoints import router as v1_router

router = APIRouter()
router.include_router(v1_router)
router.include_router(v1_router, prefix="/v1")
