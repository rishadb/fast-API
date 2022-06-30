from sqlalchemy import func #for the join table vote count function
from .. import models, schemas, oauth2 #import table models we created
from sqlalchemy.orm import Session # for Session used in path func
#depends for alchemy session , status for http error status code, APIrouter for routing
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import List, Optional #list: if the response schema need to be a list

#initialize router and @app replaces by @router, put prefix for the urls, tag to group apis in the docs
router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/", response_model=List[schemas.PostVoteRes]) #since response is a list, schemas also has to be listd; also the schema updated to include the vote from join table
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
    ,limit: int= 10, skip: int= 0, search: Optional[str] = "" ):# limit, skip, search,.. are query parameters

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.owner_id == current_user.id, models.Post.title.contains(
                search)).limit(limit).offset(skip).all() #only returns the posts of the user, with the query parametes filtered and applied
    #Also, returns the vote count from the join table of posts and votes
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRes) # changed the default 200 status code
#def create_post(payload: dict = Body(...) ):  # uses Body here which does not assert the incoming call; so pydantic used below
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #return {"message": payload["name"]}  

    new_post = models.Post(owner_id = current_user.id, **post.dict()) #extracts post data and make a Post column, here foreign_key - owner_id is added to colum, which is user.id from token
    db.add(new_post) #adds the above col to the DB
    db.commit() #commit the changes
    db.refresh(new_post) #like RETURNING in sql
    return new_post


@router.get("/{id}", response_model=schemas.PostVoteRes)
def get_a_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    a_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    if not a_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with {id} is not found")

    if a_post.Post.owner_id != current_user.id: #check the post_owner_id same as  user.id; check schema always
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to view the post")
    return a_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) # this is just query
    post = post_query.first() #needto be this way to perform post.owner_id

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")

    if post.owner_id != current_user.id: #check the post_owner_id same as  user.id
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to delete the post")

    post_query.delete(synchronize_session = False)
    db.commit()
    return status.HTTP_204_NO_CONTENT
    

@router.put("/{id}", response_model=schemas.PostRes)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) #
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {id} is not found")
    print(current_user)
    if post.owner_id != current_user.id: #check the post_owner_id same as token user_id
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to update the post")
    
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()
    
    return post_query.first() # putting the_post here only gives the object, cant be transformed to a dict too