#To login the user and send the token
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session # for Session used in path func
router = APIRouter(tags=["Authentication"])
from .. import database, models, utils, oauth2, schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm # to use for user_credentials, this makes user credentials come in a username, password form; when sending the request, send in a form-data


#Check and retrieve the user from login credentials
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): #user_credentials come in a form with email as username and password as password
    
    #verifying email & extracting user from DB
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #the email is stored in username field of the form
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    #verifying the password
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    #creating the token
    access_token = oauth2.create_access_token(data = {"user_id": user.id}) #data is the payload here that we want to put in
    
    return {"access_token": access_token, "token_type": "bearer"} #bearer is for the frontend



