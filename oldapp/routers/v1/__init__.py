from fastapi import APIRouter
from . import providers, services

router = APIRouter()
router.include_router(providers.router)
router.include_router(services.router)


