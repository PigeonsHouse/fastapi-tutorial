from datetime import datetime, timedelta
import os
from typing import Optional
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
import jwt

SECRET = os.environ.get('SECRET', 'jwt_secret')

def generate_token(user_id: str) -> str:
    exp_datetime = datetime.now() + timedelta(10)

    jwt_payload = {
        'exp': exp_datetime.timestamp(),
        'user_id': user_id
    }

    encoded_jwt = jwt.encode(jwt_payload, SECRET, algorithm='HS256')

    return encoded_jwt

def decode_token(token: str) -> str:
    user_dict = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = user_dict['user_id']
    return user_id

security = HTTPBearer()
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Optional[str]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if credentials.scheme != 'Bearer':
            raise credentials_exception

        user_id = decode_token(credentials.credentials)
    except Exception:
        raise credentials_exception
    return user_id
