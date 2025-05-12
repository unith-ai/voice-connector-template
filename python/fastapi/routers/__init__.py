from fastapi import APIRouter

from .health_check.health_handler import health_router
from .voice.voice_handler import voice_router

router = APIRouter()
router.include_router(health_router, prefix="", tags=["Health"])
router.include_router(voice_router, prefix="", tags=["Voice"])

__all__ = ["router"]
