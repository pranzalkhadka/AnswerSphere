import schemas
import models
import oauth2
from sqlalchemy.orm import Session
from database import get_db


from fastapi import status, HTTPException, Depends, APIRouter


router = APIRouter(prefix = "/vote", tags = ["vote"])

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Post not found")

    # Check if the vote is valid
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    # If the vote is 1, then the user has already voted
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "You have already voted")
        # Create a new vote
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"detail": "Voted successfully"}
    else:
        # If the vote is 0, then the user has not voted
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Vote does not exist")
        # Remove the vote
        vote_query.delete(synchronize_session = False)
        db.commit()
        return {"detail": "Vote removed"}