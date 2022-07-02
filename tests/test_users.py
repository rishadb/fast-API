#pytest -v -s <testFilePath>
import pytest
from app import schemas
from .database import client, session #session is needed coz client calls for session
#test funcs for path ops

def test_root(client):
    res = client.get("/") #sends a request to api and store response in res
    assert res.json().get('message') == 'Hello World' #if assert fails, test fails
    assert res.status_code == 200


def test_create_user(client):
    #be sure to add the '/' in the users path since test wont reditrect to correct path like fastapi
    res = client.post("/users/", json = {"email": "hello2@gmail.com", "password": "pass2"}) # second param json in func is data in the body as json; refer schema for body content
    new_user = schemas.UserRes(**res.json()) #checks if the schema of response is same as userres schema
    assert res.status_code == 201
    assert new_user.email == "hello2@gmail.com" #refer response schema fot get params

def test_login(client):
    res = client.post("/login", data= {"username":"hello2@gmail.com", "password":"pass2"}) #load is passed as data since login sends form data
    print(res.json()) #for debugging here
    assert res.status_code == 200