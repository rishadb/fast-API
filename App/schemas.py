#a datetime data type like str, int.. has to be imported
from datetime import datetime
from typing import Optional  #for token_data schema
#to assert the schema on calls, #install pip install email-validator for EmailStr
from pydantic import BaseModel, EmailStr 

#user schemas:
class UserCreate(BaseModel):
    email: EmailStr #ensures the value given is of email
    password: str

class UserRes(BaseModel):
    email: str
    created_at: datetime
    class Config:
        orm_mode = True


#call schema defenition: Post schema
class PostBase(BaseModel): # basemodel from pydantic
    #when Post used in post function, it checks for below defenitions presents, else throws an error
    title: str
    content: str
    published: bool = True #default val set to true here , two kind of default vals setting: set here or at the DB
    #rating: Optional[int] = None #optional need to be imported. if no rating given, rating deafault to None

class PostCreate(PostBase):
    pass

class PostRes(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserRes #since owner relationship established with users table for posts table in the model, we can reference any User schema class here 
#to consider the alchemy object in the return to be valid for the pydantic model, pydantic only work with dicts
    class Config:
        orm_mode = True

#for response with vote by join method
class PostVoteRes(BaseModel):
    Post: PostRes #refed above PostRes
    votes: int
#to consider the alchemy object in the return to be valid for the pydantic model, pydantic only work with dicts
    class Config:
        orm_mode = True


#incoming token schema, response_model for login
class Token(BaseModel):
    access_token: str
    token_type: str

#to verify data in token
class TokenData(BaseModel):
    id: Optional[str]


#votes incoming
class Vote(BaseModel):
    post_id: int
    addT_deleteF: bool





    