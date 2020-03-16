from ..config import statsd
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def healthcheck():
    statsd.incr("healthchecked")
    return {"app": "", "healthy": True}
