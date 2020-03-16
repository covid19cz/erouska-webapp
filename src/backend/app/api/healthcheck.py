from app.config import statsd
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def healthcheck():
    statsd.incr("healthchecked")
    return {"app": "", "healthy": True}
