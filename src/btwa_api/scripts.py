import bcrypt
from app.db.session import Session
from app.models.handler import Handler


def add_handler(username, password):
    session = Session()
    handler = Handler(username=username,
                      password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
    session.add(handler)
    session.commit()
    session.close()
