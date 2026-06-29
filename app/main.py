from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import time
import psycopg
from psycopg.rows import dict_row
from random import randrange

app = FastAPI()
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
while True:
    try:
        conn = psycopg.connect(host=DB_HOST,
                            dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            row_factory=dict_row) # type: ignore[arg-type]
        cursor = conn.cursor()
        print("Database connection succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ",error)
        time.sleep(2)

my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},
          {"title":"title of post 2","content":"content of post 2","id":2}]


@app.get("/")
def root():
    return {"message":"hello world"}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    cursor.execute("SELECT * FROM posts WHERE id=%s",(id,))
    one_post=cursor.fetchone()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with ID : {id} not found")
    return one_post

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute(
    "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    (post.title, post.content, post.published)
    )
    new_post = cursor.fetchall()
    conn.commit()
    return {"data":new_post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *",(id,))
    del_post=cursor.fetchone()
    conn.commit()
    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int,post:Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s , published = %s WHERE id=%s RETURNING *",(post.title,post.content,post.published,id))
    upd_post = cursor.fetchone()
    conn.commit()
    if upd_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found")
    return {"data":upd_post}