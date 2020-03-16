from ..models.user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


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
