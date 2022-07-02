#copied from database.py
#TO CONNECT TO THE DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings #import the initiated setting here to import secret vals
from app.database import get_db
import pytest
from app.main import app
from fastapi.testclient import TestClient #testing tool from fastapi
from app.models import Base

#put a _test at the end of the sqlDBURL
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

#engine to connect alchemy to postgres for queries
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#session for talking to DB for qieries
#changed seeionLocal to TestingLocal
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)


@pytest.fixture(scope="function") #the scope here is default val, but can change to module, session, class,.. so fixture runs for each specified scope only
def session(): #this session func which stores db as a session var gets passed to client below, so this func runs before client
    Base.metadata.drop_all(bind = engine) #drop all the tables
    Base.metadata.create_all(bind = engine) #make all the tables
    
    db = TestingSessionLocal() #create dependancy, this func get a connection/session to DB when we get a request, sends a sql statement to it, closes after the request is done.
    try:
        yield db
    finally:
        db.close()

#with fixture decorator, func store the return value in a variable_name same as the function name. pass this func as params to the tests so it runs before them
@pytest.fixture()
def client(session): #var client = testclient made when this func is run when passed onto the tests
    #command.upgrade("head"); command.downgrade("head"); from alembic import command ;# for creating table thru alembic
    
    #create dependancy, this func get a connection/session to DB when we get a request, sends a sql statement to it, closes after the request is done.
    #changes: get_dg to override_get_db
    def override_get_db(): #copied from fast api/alchemy
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    #To override get_db with pverride_get_db:
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app) #yield makes codes in func after the yield run; testclient starts the testing process on app
