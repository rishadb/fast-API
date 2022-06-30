from typing import Optional #for optional col name in pydantic model
from fastapi import Body, FastAPI, status, HTTPException
import fastapi #Body to extract the body of the incoming call, status for http error status code
from pydantic import BaseModel #to assert the schema on calls
from requests import Response 
import psycopg2
from psycopg2.extras import RealDictCursor # to get the col names while querying
import time 

#define app
app = FastAPI()

#connect to the DB & setup cursor
while True:#to stop starting server without connecting to the DB
    try:
        conn = psycopg2.connect(host = "localhost", database="fastapi", 
            user="postgres", password = "admin", cursor_factory=RealDictCursor )# cursor_factory to give the col name while querying)
        cursor = conn.cursor() #curson used to execute sql statements
        print("Database connection was successfull")
        break
    except Exception as error:
        print(f"Database connection was unsuccessfull, Error: {error}")
        time.sleep(2)



#call schema defenition
class Post(BaseModel): # basemodel from pydantic
    #when Post used in post function, it checks for below defenitions presents, else throws an error
    title: str
    content: str
    published: bool = True #default val set to true here
    #rating: Optional[int] = None #optional need to be imported. if no rating given, rating deafault to None


#APIs

@app.get("/") #decorator+app+httpmethod(path)
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_post():
    cursor.execute(""" SELECT * FROM posts """)
    post = cursor.fetchall()
    return {"post":post}

@app.post("/posts", status_code=status.HTTP_201_CREATED) # changed the default 200 status code
#def create_post(payload: dict = Body(...) ):  # uses Body here which does not assert the incoming call; so pydantic used below
def create_post(post: Post):
    #return {"message": payload["name"]} 
    cursor.execute(""" INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *  """, (post.title, post.content, post.published))#use the %s to prevent sql injection
    new_post = cursor.fetchone() # returning will be stored in new_post
    conn.commit() # to commit to the DB
    return {"data": new_post}


@app.get("/posts/{id}")
def get_apost(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))#need to convert id to string and put a comma
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with {id} is not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING id""", (str(id),))
    index = cursor.fetchone()   
    conn.commit()
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
    return status.HTTP_204_NO_CONTENT

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING * """, 
    (post.title,post.content, post.published, str(id),))    
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {id} is not found")
    return f" the post with id {id} has been updated as: {dict(updated_post)} "
