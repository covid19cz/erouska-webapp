from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials

from .config import logger
from .db.session import Session
from .db.utils import get_db
from .models.user import User
from .security import check_basic_auth, security

router = APIRouter()


def add_user(db: Session, guid: str):
    try:
        user = User(guid=guid)
        db.add(user)
        db.commit()
        return True
    except Exception as e:
        logger.error(e)
        return False


@router.get("/register/{guid}")
def register(guid: str,
             credentials: HTTPBasicCredentials = Depends(security),
             db: Session = Depends(get_db)):
    check_basic_auth(credentials)
    if add_user(db, guid):
        return True
    else:
        raise HTTPException(status_code=400, detail="GUID already exists")
