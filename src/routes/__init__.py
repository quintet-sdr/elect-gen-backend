from fastapi import APIRouter

from . import api


def meta() -> APIRouter:
    meta_router = APIRouter()

    meta_router.include_router(api.router)

    return meta_router
