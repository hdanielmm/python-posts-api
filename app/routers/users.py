from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.orm_config import get_db
from models import ormpost as models

from models.schemas import User, UserCreate
from routers.orm_posts import Error404, error_404
from utils import get_password_hash
from oauth2 import get_current_user


router = APIRouter(prefix="/users", tags=["user"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[User])
def get_user(db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):
    users = db.query(models.User).all()

    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=User)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    return user


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=User)
def update_user(id: int, new_user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == id)
        print("user", user)
        print("user.first", user.first())
        if user.first() is None:
            Error404()

        hashed_password = get_password_hash(new_user.password)
        new_user.password = hashed_password
        user.update(new_user.dict(), synchronize_session=False)

        db.commit()

        return user.first()
    except Error404:
        raise error_404(id)
    except Exception as e:
        print("Error: %s" % e)
