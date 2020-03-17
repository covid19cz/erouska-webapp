from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.handler import Handler
from ..models.user import User


class Database:
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, guid: str) -> bool:
        """Returns true if user was added successfully"""
        try:
            user = User(guid=guid)
            self.session.add(user)
            self.session.commit()
            return True
        except IntegrityError:
            return False

    def get_handler_hashed_password(self, username):
        handler = self.session.query(Handler).filter_by(username=username).first()
        if handler is not None:
            return handler.password
        return None

    def get_user_by_guid(self, guid: str):
        return self.session.query(User).filter_by(guid=guid).first()
