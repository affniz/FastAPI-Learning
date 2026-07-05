from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import schemas,database,models,oauth2

router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote_on_post(vote_data:schemas.Vote,db:Session = Depends(database.get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    post=db.scalar((select(models.Post).where(models.Post.id==vote_data.post_id)))
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote_data.post_id} does not exist")
    vote_query=select(models.Vote).where(models.Vote.post_id == vote_data.post_id, models.Vote.user_id == current_user.id)
    found_vote=db.scalar(vote_query)
    if vote_data.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {current_user.id} has already voted on post {vote_data.post_id}")
        new_vote = models.Vote(post_id=vote_data.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message":"Successfully added a vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote not found")
        db.delete(found_vote)
        db.commit()
        return {"Message":"Successfully deleted vote"}