from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.orm_config import get_db
from models import schemas, ormpost
from .orm_posts import Error404, error_404
from utils import verify_password
from oauth2 import create_access_token

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(ormpost.User).filter(ormpost.User.email == user_credentials.username).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
            # raise Error404()
        
        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    except Exception as e:
        print("Error: %s" % e)

    # Create token
    # This is the data to put in the payload
    access_token = create_access_token(data = {"user_id": user.id})
    # Return token
    return {"access_token": access_token, "token_type": "bearer"}
