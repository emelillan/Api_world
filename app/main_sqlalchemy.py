from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from starlette.status import HTTP_404_NOT_FOUND
import models
from sqlalchemy.orm import Session
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()




#create Post class Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True



my_posts = [{"title":"title1", "content":"content of post 1", "id": 1},
            {"title":"title2", "content":"content of post 2", "id": 2}]

while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='Fastapi_1',
                                user='ezequielmelillan',
                                password='new_password',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was Succesfull")
        break
    except Exception as error:
        print("Connecting to database fail")
        print("Error: ", error)
        time.sleep(5)



#MAIN ENDPOINT
@app.get("/") 
def root():
    return {"message": "Welcome to my API"}

#testin sqlalchemy
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}


#ALL POST GET
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}

# CREATE POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post, db: Session = Depends(get_db)):
    created_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return {"new_post": created_post}

#GET ONE POST BY ID
@app.get('/posts/{id}')
def get_posts(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail=f"Post with ID: {id} was not found")                                
    return {"post_detail" : post}

# DELETE ONE POST BY ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    # deleting post

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Post ID: {id} does not Exist")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE ONE POST BY ID
@app.put("/posts/{id}")
def update_post(id: int, updated_post:Post, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Post ID: {id} does not Exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data" : post_query.first()}
