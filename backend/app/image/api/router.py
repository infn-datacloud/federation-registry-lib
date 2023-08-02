from fastapi import APIRouter
from app.image.api.v1.endpoints import router as v1_router
from app.config import get_settings

settings = get_settings()

router = APIRouter()
router.include_router(v1_router)
router.include_router(v1_router, prefix=settings.API_V1_STR)
