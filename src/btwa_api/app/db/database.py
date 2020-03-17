from sqlalchemy.orm import Session

from ..models.handler import Handler


class Database:
    def __init__(self, session: Session):
        self.session = session

    def get_handler_hashed_password(self, username):
        handler = self.session.query(Handler).filter_by(username=username).first()
        if handler is not None:
            return handler.password
        return None
