from fastapi import FastAPI

from db import mongodb, pg_db
from contextlib import asynccontextmanager

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
from routers import projects as project_router

app.include_router(auth_router.router)
app.include_router(profile_router.router)
app.include_router(project_router.router)