from .. import schemas,models
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostResponse])
def get_posts(db:Session=Depends(get_db)):
    posts = db.execute(select(models.Post)).scalars().all()
    return posts

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id:int,response:Response,db:Session=Depends(get_db)):
    one_post=db.execute(select(models.Post).where(models.Post.id==id)).scalar_one_or_none()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with ID : {id} not found")
    return one_post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db)):
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    del_post = db.execute(select(models.Post).where(models.Post.id==id)).scalar_one_or_none()
    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found")
    db.delete(del_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_db = db.execute(select(models.Post).where(models.Post.id == id)).scalar_one_or_none()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    for key, value in post.model_dump().items():
        if key != 'id':
            setattr(post_db, key, value)
    db.commit()
    db.refresh(post_db)
    return post_db