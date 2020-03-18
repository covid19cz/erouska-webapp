import bcrypt
from app.db.sql.models.handler import Handler
from app.db.sql.session import Session


def add_handler(username, password):
    session = Session()
    handler = Handler(username=username,
                      password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
    session.add(handler)
    session.commit()
    session.close()
