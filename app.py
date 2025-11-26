from fastapi import FastAPI, HTTPException, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session as DBSession

from models.pg_models import User
from db import mongodb, pg_db
from db.mongodb import get_profiles_collection
from models.mongo_models import ProfileIntro
from contextlib import asynccontextmanager
from passlib.context import CryptContext
from utils.auth import create_session, require_admin
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb.connect() 
    pg_db.connect()
    
    yield  # The application runs here
    
    mongodb.close()
    pg_db.close()
app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"hint": "Try it under /docs."}

# Register feature routers
from routers import auth as auth_router
from routers import profile as profile_router

app.include_router(auth_router.router)
app.include_router(profile_router.router)
