from .. import schemas,models
from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from ..database import get_db
from .. import oauth2

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:str=""):
    stmt = (
    select(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    )
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    .group_by(models.Post.id)
    .where(models.Post.title.contains(search))
    .limit(limit)
    .offset(skip)
    )
    posts = db.execute(stmt).all()
    return posts

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,response:Response,db:Session=Depends(get_db),current_user:schemas.UserOut =Depends(oauth2.get_current_user)):
    stmt = (
    select(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    )
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    .group_by(models.Post.id)
    .where(models.Post.id==id))
    one_post=db.execute(stmt).first()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with ID : {id} not found")
    return one_post


#one_post=db.execute(select(models.Post).where(models.Post.id==id)).scalar_one_or_none()
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):

    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    
    del_post = db.execute(select(models.Post).where(models.Post.id==id)).scalar_one_or_none()
    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found")
    if del_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    db.delete(del_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    post_db = db.execute(select(models.Post).where(models.Post.id == id)).scalar_one_or_none()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    if post_db.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    for key, value in post.model_dump().items():
        if key != 'id':
            setattr(post_db, key, value)
    db.commit()
    db.refresh(post_db)
    return post_db