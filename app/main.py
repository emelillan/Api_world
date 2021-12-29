from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from starlette.status import HTTP_404_NOT_FOUND


app = FastAPI()

#create Post class Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None


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

#ALL POST GET
@app.get("/posts")
def get_posts():

    cursor.execute("""SELECT * from public."Posts";""")
    posts = cursor.fetchall()
    print(posts)
    return {"data":posts}

# CREATE POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):

    cursor.execute(""" INSERT into public."Posts" (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    created_post = cursor.fetchone()
    conn.commit()

    return {"new_post": created_post}

#GET ONE POST BY ID
@app.get('/posts/{id}')
def get_posts(id: int, response: Response):

    cursor.execute(""" SELECT *  from public."Posts" WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail=f"Post with ID: {id} was not found")                                
    return {"post_detail" : post}

# DELETE ONE POST BY ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # deleting post
    cursor.execute(""" DELETE FROM  public."Posts" WHERE id = %s returning * """, (id,))
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Post ID: {id} does not Exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE ONE POST BY ID
@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    
    cursor.execute(""" UPDATE  public."Posts" SET title= %s, content = %s, published= %s WHERE id = %s returning * """, (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Post ID: {id} does not Exist")

    return {"data" : updated_post}


#Post Schema
#title str
#content str