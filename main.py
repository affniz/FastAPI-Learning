from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating: int | None = None

my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},
          {"title":"title of post 2","content":"content of post 2","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return -1

@app.get("/")
def root():
    return {"message":"hello world"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    res=find_post(id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with ID : {id} not found")
    return res 

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    ind = find_index_post(id)
    if ind==-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found")
    my_posts.pop(ind)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int,post:Post):
    ind = find_index_post(id)
    if ind==-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found")
    upd_post = post.model_dump()
    upd_post['id'] = id
    my_posts[ind] = upd_post
    return {"message":"Post updated successfully"}