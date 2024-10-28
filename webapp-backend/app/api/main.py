from fastapi import APIRouter

from app.api.routes import auth, account, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
