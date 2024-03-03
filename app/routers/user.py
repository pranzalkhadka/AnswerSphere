import schemas
import models
import utils
from sqlalchemy.orm import Session
from database import get_db
from fastapi import status, HTTPException, Depends, APIRouter


router = APIRouter(prefix = "/users", tags = ["users"])


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = utils.hash(user.password)
    # Replace the password with the hashed password
    user.password = hashed_password
    # Unpack the payload dictionary and pass it to the User class
    new_user = models.User(**user.dict())
    # Add the new user to the database
    db.add(new_user)
    # Commit changes to the database
    db.commit()
    # Retrieve the newly created user and store in new_user
    db.refresh(new_user)
    return new_user
    

@router.get("/{id}", response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    # Retrieve the user with the given id
    user = db.query(models.User).filter(models.User.id == id).first()
    # If the user is not found, raise an HTTPException
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    return user