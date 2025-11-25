from fastapi import FastAPI, HTTPException
from db import attach_fastapi_events, get_profiles_collection
from models.mongo_models import ProfileIntro

app = FastAPI()

attach_fastapi_events(app)

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

@app.get("/profiles", response_model=list[ProfileIntro])
def read_profiles():
    coll = get_profiles_collection()
    docs = coll.find()
    return list(docs)
