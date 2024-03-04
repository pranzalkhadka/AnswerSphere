import schemas
import models
import oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import func
from fastapi import Response, status, HTTPException, Depends, APIRouter


router = APIRouter(prefix = "/posts", tags = ["posts"])

# limit helps to limit the number of posts
# skip helps to skip the number of posts
# search helps to search for a specific post
@router.get("/", response_model = List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # Retrieve all the posts from the database
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()   -> to retrieve only the posts created by the current user
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts



@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def make_post(payload: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.id)
    # Unpack the payload dictionary and pass it to the Post class
    new_post = models.Post(owner_id = current_user.id, **payload.dict())
    # Add the new post to the database
    db.add(new_post)
    # Commit changes to the database
    db.commit()
    # Retrieve the newly created post and store in new_post
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model = schemas.PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Retrieve the post with the given id
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # If the post is not found, raise an HTTPException
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # If the user can only view his/her own posts
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You don't have permission to delete this post")
    
    return post



@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Retrieve the post with the given id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # If the post is not found, raise an HTTPException
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You don't have permission to delete this post")
    
    # Delete the retrieved post
    post_query.delete(synchronize_session = False)
    # Commit changes to the database
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code = status.HTTP_202_ACCEPTED, response_model = schemas.PostResponse)
def update_post(id: int, payload: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Retrieve the post with the given id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # If the post is not found, raise an HTTPException
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You don't have permission to delete this post")
    
    post_query.update(payload.dict(), synchronize_session = False)
    # Commit changes to the database
    db.commit()
    # Return the updated post
    return post_query.first()
    