from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel

from .utils import get_or_404
from ..db.firebase.firebase import Firebase, get_firebase
from ..db.sql.database import Database
from ..db.utils import get_db
from ..security import check_handler_auth, security

router = APIRouter()


class UserLookup(BaseModel):
    phone: str


class User(BaseModel):
    fuid: str
    status: str


@router.post("/get-user", response_model=User)
def get_user(lookup: UserLookup,
             credentials: HTTPBasicCredentials = Depends(security),
             firebase: Firebase = Depends(get_firebase),
             db: Database = Depends(get_db)):
    """Find user by his phone number."""
    check_handler_auth(db, credentials)
    user = get_or_404(firebase.get_user_by_phone(lookup.phone))
    return User(fuid=user["fuid"], status=user["status"])


class ProximityRecord(BaseModel):
    buid: str
    start: int
    end: int
    status: str
    phone: str


@router.get("/proximity/{fuid}", response_model=List[ProximityRecord])
def get_proximity(fuid: str,
                  credentials: HTTPBasicCredentials = Depends(security),
                  firebase: Firebase = Depends(get_firebase),
                  db: Database = Depends(get_db)):
    """Return information about proximity of the given user"""
    check_handler_auth(db, credentials)
    records = get_or_404(firebase.get_proximity(fuid))
    return [ProximityRecord(
        buid=r["buid"],
        start=r["timestampStart"],
        end=r["timestampEnd"],
        status=r["user"]["status"],
        phone=r["user"]["phoneNumber"]
    ) for r in records]


class UserStatus(BaseModel):
    status: str


@router.post("/change-user-status/{fuid}")
def change_user_status(fuid: str,
                       status: UserStatus,
                       credentials: HTTPBasicCredentials = Depends(security),
                       firebase: Firebase = Depends(get_firebase),
                       db: Database = Depends(get_db)):
    """Change the infected status of a user"""
    check_handler_auth(db, credentials)
    if not firebase.change_user_status(fuid, status.status):
        raise HTTPException(status_code=404)
