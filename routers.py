from fastapi import APIRouter, Depends
from typing import List
from utils import generate_token, get_current_user
from db import get_db
import cruds
from sqlalchemy.orm.session import Session
from schemas import ContentPayload, ContentSchema, ReturnToken, SignInPayload, SignUpPayload, UserSchema

user_router = APIRouter(prefix='/users', tags=['users'])
content_router = APIRouter(prefix='/contents', tags=['contents'])

@user_router.post('/signup', response_model=UserSchema)
def signup(payload: SignUpPayload, db: Session = Depends(get_db)):
    user = cruds.add_user(db, payload.email, payload.name, payload.password)
    return user

@user_router.post('/signin', response_model=ReturnToken)
def signin(payload: SignInPayload, db: Session = Depends(get_db)):
    user_id = cruds.get_user_id(db, payload.email, payload.password)
    token = generate_token(user_id)
    return {'token': token}

@user_router.get('/me', response_model=UserSchema)
def get_my_info(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = cruds.get_user_by_id(db, user_id)
    return user

@content_router.get('', response_model=List[ContentSchema], dependencies=[Depends(get_current_user)])
def fetch_contents(db: Session = Depends(get_db)):
    contents = cruds.get_contents(db)
    return contents

@content_router.post('', response_model=ContentSchema)
def post_content(payload: ContentPayload, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    content = cruds.add_content(db, payload.content, user_id)
    return content
