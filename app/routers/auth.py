import utils
import oauth2
import models
import schemas
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import status, HTTPException, Depends, APIRouter


# Create a new APIRouter
router = APIRouter(tags = ["authentication"])


@router.post("/login", status_code = status.HTTP_200_OK, response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Retrieve the user with the given email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # If the user email is not found, raise an HTTPException
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid credentials")
    
    # If the password is incorrect, raise an HTTPException
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid credentials")

    # Create an access token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}