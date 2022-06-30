
from .. import models, schemas, utils #import table models we created
#depends for alchemy session , status for http error status code, APIrouter for routing
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session # for Session used in path func
from ..database import get_db



#initialize router and @app replaces by @router, put prefix for the urls, tag to group apis in the docs
router = APIRouter(
    prefix="/users",
    tags=["users"]

)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserRes)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #to hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        #raise http error for unique error 
        return new_user
    except:#raise http error for unique error 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the {user.email} is already enrolled")

@router.get("/{id}", response_model=schemas.UserRes)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with {id} not found")
    return user