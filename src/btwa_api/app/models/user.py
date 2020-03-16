import datetime

from ..db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, String


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    guid = Column(String, unique=True)
    inserted_at = Column('inserted_at', DateTime, default=datetime.datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)
