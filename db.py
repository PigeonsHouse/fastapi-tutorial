import os
from sqlalchemy import DateTime, ForeignKey, String, create_engine, Column
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any
from uuid import uuid4
from sqlalchemy.sql.functions import func

def generate_uuid():
    return str(uuid4())

@as_declarative()
class Base:
    id: Any
    __name__: Any

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

try:
    os.environ['DATABASE_URL']
except Exception:
    print("DEBUG: using sqlite")

os.environ.setdefault('DATABASE_URL', 'sqlite:///db.sqlite3?check_same_thread=false')
DATABASE_URL = os.environ['DATABASE_URL']

engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(bind=engine)

SessionClass = sessionmaker(engine)
def get_db() -> Session:
    db = SessionClass()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True)
    name = Column(String)
    password_hash = Column(String)

    contents = relationship('Content', foreign_keys='Content.user_id', back_populates='user')

class Content(Base):
    __tablename__ = 'contents'
    id = Column(String, primary_key=True, default=generate_uuid)
    content = Column(String)
    user_id = Column(String(), ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())

    user = relationship('User', back_populates='contents')
