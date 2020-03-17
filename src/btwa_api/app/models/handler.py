from sqlalchemy import Binary, Column, Integer, String

from ..db.base_class import Base


class Handler(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=128), unique=True)
    password = Column(Binary(length=80))
