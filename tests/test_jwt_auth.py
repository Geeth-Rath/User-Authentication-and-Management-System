import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.utils.jwt_auth import create_access_token

import os

os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["EXPIRE_MINUTES"] = "15"
os.environ["ALGORITHUM"] = "HS256"

def test_create_access_token():

    user_id = 1
    username = "testuser"

    token = create_access_token(id=user_id, username=username)

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHUM")])
        assert payload["sub"] == username
        assert payload["id"] == user_id
        exp = datetime.utcfromtimestamp(payload["exp"])
        assert exp > datetime.utcnow()
        assert exp <= datetime.utcnow() + timedelta(minutes=int(os.getenv("EXPIRE_MINUTES")))
    except jwt.JWTError:
        pytest.fail("Token verification failed")

