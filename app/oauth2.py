import schemas
from database import get_db
import models
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import settings

# Create an instance of OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict, expires_delta: int = None):
    # Create a copy of the data
    to_encode = data.copy()
    # If expires_delta is provided, create an expiration time
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add the expiration time to the data
    to_encode.update({"exp": expire})
    # Encode the data and return the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        # print(payload)
        id: str = payload.get('user_id')
        # print(id)
        # print(type(id))
        # If the id is not found, raise an HTTPException
        if id is None:
            raise credentials_exception
        # Create a TokenData instance
        token_data = schemas.TokenData(id = str(id))
        # print(token_data)

    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Create an instance of HTTPException
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = "Invalid Credentials", headers = {"WWW-Authenticate" : "Bearer"})
    # Verify the token
    token = verify_access_token(token, credentials_exception)
    # Retrieve the user with the given id
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user