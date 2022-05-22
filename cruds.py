import os
from typing import List
import bcrypt
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm.session import Session
from schemas import ContentSchema, UserSchema
from db import Content, User

salt = os.environ.get('PASSWORD_HASH_SALT', '$2a$10$ThXfVCPWwXYx69U8vuxSUu').encode()

def get_password_hash(password: str) -> str:
    hash = bcrypt.hashpw(password.encode(), salt)
    return hash.decode()

def add_user(db: Session, email: str, name: str, password: str) -> UserSchema:
    users_orm = db.query(User).filter(User.email == email).all()
    if users_orm:
        raise HTTPException(status_code=400, detail='this email is already exist')

    user_orm = User(
        email=email,
        name=name,
        password_hash=get_password_hash(password)
    )

    db.add(user_orm)
    db.commit()
    db.refresh(user_orm)
    user_info = UserSchema.from_orm(user_orm)
    return user_info

def get_user_id(db: Session, email: str, password: str) -> str:
    user: User = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    password_hash = get_password_hash(password)
    if user.password_hash != password_hash:
        raise HTTPException(status_code=401, detail='authentication failed')

    return user.id

def get_user_by_id(db: Session, user_id: str) -> UserSchema:
    user_orm = db.query(User).filter(User.id == user_id).first()
    if user_orm is None:
        raise HTTPException(status_code=404, detail='this user is not found')
    user = UserSchema.from_orm(user_orm)
    return user

def get_contents(db: Session, user_id: str) -> List[ContentSchema]:
    contents_orm = db.query(Content).order_by(desc(Content.created_at)).all()
    contents = list(map(ContentSchema.from_orm, contents_orm))
    if not contents:
        raise HTTPException(status_code=404, detail='content is not found')
    return contents

def add_content(db: Session, content: str, user_id: str) -> ContentSchema:
    content_orm = Content(
        content=content,
        user_id=user_id
    )

    db.add(content_orm)
    db.commit()
    db.refresh(content_orm)

    content_data = ContentSchema.from_orm(content_orm)
    return content_data
