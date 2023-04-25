from jose import JWTError, jwt
from datetime import datetime, timedelta


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "6900d7e78472a2e9e7e24af7852600c79004ec9256d49a74c08e94c20db6672d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt