import os
import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from schemas import UserSchema
from db import User

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

# 作る関数1
# DBからcontentsのテーブルにある情報全部持ってきて，返す用のschemaにフォーマットして，フォーマットしたものの配列を返す
# fetch_contents関数で使用したい．

# 作る関数2
# Contentの作成に必要な情報を引数に受け取り，DBに追加して，追加した情報を更新した後にフォーマットして返す．
# post_content関数で使用したい．
