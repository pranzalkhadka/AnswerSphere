from fastapi import FastAPI
import models
from database import engine, get_db
from routers import post, user, auth, vote

from fastapi.middleware.cors import CORSMiddleware

# Create the tables in the database
models.Base.metadata.create_all(bind = engine)


app = FastAPI()

# Add the middleware to allow CORS
# This is to allow requests from any domain on the internet
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


# Include the routers in the main app        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"Hi, I am Pranjal"}