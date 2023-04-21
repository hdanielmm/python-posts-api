from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext


SECRET_KEY = "6900d7e78472a2e9e7e24af7852600c79004ec9256d49a74c08e94c20db6672d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password):
    return pwd_context.hash(password)
