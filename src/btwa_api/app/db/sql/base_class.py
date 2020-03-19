from sqlalchemy.ext.declarative import declarative_base, declared_attr


# https://github.com/tiangolo/full-stack-fastapi-postgresql
class CustomBase(object):
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)
