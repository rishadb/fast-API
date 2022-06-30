from App import database
from .. import models, schemas, oauth2, database #import table models we created
from sqlalchemy.orm import Session # for Session used in path func
#depends for alchemy session , status for http error status code, APIrouter for routing
from fastapi import status, HTTPException, Depends, APIRouter


#initialize router and @app replaces by @router, put prefix for the urls, tag to group apis in the docs
router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

#to add or delete vote for a post by a user
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    
    found_vote = vote_query.first()

    if (vote.addT_deleteF): #to add the vote/ clicking the first time
        if found_vote: # means vote exist already
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                    detail= f"user {current_user.id} has already voted on post: {vote.post_id}")
        else: #vote dont exist = need to put the vote
            try:# if post_id doesn't exists, 
                new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
                db.add(new_vote)
                db.commit()
                return {"message": "successfully voted"}
            except:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the post id is not correct")    
            
            
            
    else:#to delte the vote/ second tap
        if not found_vote: #vote doesn't exist = cant delete = raise exception
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the vote dosn't exist")
        else: # vote exists = need to delete it
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "successfully deleted the vote"}