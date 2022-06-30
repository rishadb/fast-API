#CREATE TOKEN, VERIFY TOKEN, PATH OPS DEPENDANCY FUNC
from fastapi import Depends, status, HTTPException #for get_user func
from jose import JWTError, jwt # jose has to be installed with pip install python-jose[cryptography];
from datetime import datetime, timedelta  # to include the formatted time for token
from requests import Session
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer # dependancy func for the token in get_current_user
from .config import settings #import the initiated setting here to import secret vals


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #dependancy func for token scheme;url of the login added


#access token will have a header, payload and signature()
#igredients: secret key, algo for encrypting signature HS256, expiration time
SECRET_KEY = settings.secret_key #just type long string
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRES_MINUTES = settings.access_token_expires_minutes

#func to create access token
def create_access_token(data: dict):
    
    #Add expire time to the data
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire}) #add the expire time to the dict

    #make the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

#decode, extract payload, extract info from payload, verify the token 
def verify_access_token(token: str, credentials_exception): #cred_exception error to be raised if creds dont match
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM]) # to decode the token with key and extract payload
        id: str = payload.get("user_id") #refer to the auth page and see what we put as payload when making token
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id) # to check and ensure that all data we passed into the token are acutally there, come in handy when there were lot of items in payload
    except JWTError: #from jose library
        raise credentials_exception
    
    return token_data #data to be used at where the get_current_user is called
    
#to be passed as a dependancy to path ops; takes token from requests, extract id, verify token, fetch user from DB and add as a param to path ops func
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)): #oauth2scheme ties this func to login url
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", 
                            headers={"WWW-Authenticate": "Bearer"})#just put the headers as is here
    
    token = verify_access_token(token ,credentials_exception) # gives the payload_data returned from verify
    current_user = db.query(models.User).filter(models.User.id == token.id).first() #extract logged in userdata from database to be used in other logics
    
    return current_user


    

    
