import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.config import DATABASE_URI

engine = create_engine(DATABASE_URI, pool_pre_ping=True,
                       connect_args={'check_same_thread': False}  # TODO: check if OK with SQLite
                       )
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
