from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel

from .utils import get_or_404
from ..db.database import Database
from ..db.firebase import Firebase, get_firebase
from ..db.utils import get_db
from ..security import check_handler_auth, security

router = APIRouter()


class User(BaseModel):
    fuid: str
    infected: bool


@router.get("/get-user/{phone}", response_model=User)
def get_user(phone: str,
             credentials: HTTPBasicCredentials = Depends(security),
             firebase: Firebase = Depends(get_firebase),
             db: Database = Depends(get_db)):
    """Find user by his phone number."""
    check_handler_auth(db, credentials)
    user = get_or_404(firebase.get_user_by_phone(phone))
    return User(fuid=user["fuid"], infected=user["infected"])


class ProximityRecord(BaseModel):
    buid: str
    start: int
    end: int
    infected: bool
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
        infected=r["user"]["infected"],
        phone=r["user"]["phone"]
    ) for r in records]


class InfectedStatus(BaseModel):
    infected: bool


@router.post("/mark-infected/{fuid}")
def mark_infected(fuid: str,
                  status: InfectedStatus,
                  credentials: HTTPBasicCredentials = Depends(security),
                  firebase: Firebase = Depends(get_firebase),
                  db: Database = Depends(get_db)):
    """Change the infected status of a user"""
    check_handler_auth(db, credentials)
    if not firebase.mark_as_infected(fuid, status.infected):
        raise HTTPException(status_code=404)
