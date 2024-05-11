from fastapi import APIRouter

import src.api.v1.user_endpoints

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_endpoints.router, tags=["users"])
