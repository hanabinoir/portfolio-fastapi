from fastapi import FastAPI, HTTPException
from db import connect, close, get_profiles_collection
from models.mongo_models import ProfileIntro
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect() 
    
    yield  # The application runs here
    
    close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/profile", response_model=ProfileIntro)
async def read_profile():
    coll = get_profiles_collection()
    doc = coll.find_one({"type": "INTRO"})
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc

