from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials

from ..db.database import Database
from ..db.utils import get_db
from ..security import check_handler_auth, security

router = APIRouter()


@router.get("/register/{guid}")
def register(guid: str,
             credentials: HTTPBasicCredentials = Depends(security),
             db: Database = Depends(get_db)):
    check_handler_auth(db, credentials)
    if db.add_user(guid):
        return True
    else:
        raise HTTPException(status_code=400, detail="GUID already exists")
