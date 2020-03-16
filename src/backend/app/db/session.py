from app.config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

args = {}
if DATABASE_URI.startswith("sqlite:///"):
    args["check_same_thread"] = False  # TODO: check if OK with SQLite

engine = create_engine(DATABASE_URI, pool_pre_ping=True, connect_args=args)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
