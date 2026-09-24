from fastapi import APIRouter

from src.presentation.api.v1.users.routes import router as users_router

router = APIRouter(prefix='/v1')
router.include_router(users_router)

__all__ = ['router']
