from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from oauth2 import get_current_user
from models.schemas import Vote
from models import ormpost as models

from database.orm_config import get_db


router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(
    vote: Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    post = db.query(models.OrmPost).filter(models.OrmPost.id == vote.post_id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {vote.post_id} does not exist",
        )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()
        # db.refresh(new_vote)

        return {"message": "Successfully added vote"}
    else:
        if found_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}
