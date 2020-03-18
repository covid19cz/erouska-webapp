from fastapi import APIRouter

from ..config import statsd

router = APIRouter()


@router.get("/status")
async def healthcheck():
    """Health check"""
    statsd.incr("healthchecked")
    return {"healthy": True}
