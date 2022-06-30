#depends for alchemy session , status for http error status code, APIRouter for routing
from fastapi import FastAPI
from . import models #import table models we created
from .database import engine
from .routers import post, user, auth, votes # importing the API files
from fastapi.middleware.cors import CORSMiddleware #CORS


#to create all the tables from models; not needed now since we use alembic to create and update the tables
#models.Base.metadata.create_all(bind = engine) #copied from fast api/alchemy

#define app
app = FastAPI()

#CORS setup: add middleware
origins = ["*"] #["https://www.google.com", "https://fastapi.tiangolo.com", "https://www.youtube.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#include router files to route from App
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

#APIs

@app.get("/") #decorator+app+httpmethod(path)
async def root():
    return {"message": "Hello World"}

