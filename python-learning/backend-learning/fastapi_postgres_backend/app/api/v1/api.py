from fastapi import APIRouter
from app.api.v1.endpoints import users, http_methods

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(http_methods.router)
