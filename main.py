from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL Connection
db = mysql.connector.connect(
    host="shinkansen.proxy.rlwy.net",
    user="root",
    password="dmwOEZmAatrlfrrAtzvUhudFNomgBUpf",
    database="railway",
    port=58616
)

cursor = db.cursor(dictionary=True)

# Model structure
class Todo(BaseModel):
    heading: str
    content: str
    date: str

# GET all todos
@app.get("/todos")
def get_todos():
    cursor.execute("SELECT * FROM todos ORDER BY id DESC")
    return cursor.fetchall()

# GET single todo
@app.get("/todos/{todo_id}")
def get_single(todo_id: int):
    cursor.execute("SELECT * FROM todos WHERE id=%s", (todo_id,))
    todo = cursor.fetchone()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# CREATE todo
@app.post("/todos")
def create(todo: Todo):
    query = """
    INSERT INTO todos (heading, content, date)
    VALUES (%s,%s,%s)
    """
    cursor.execute(query, (todo.heading, todo.content, todo.date))
    db.commit()
    return {"message": "Todo created successfully"}

# UPDATE todo
@app.put("/todos/{todo_id}")
def update(todo_id: int, todo: Todo):
    query = """
    UPDATE todos
    SET heading=%s, content=%s, date=%s
    WHERE id=%s
    """
    cursor.execute(query, (todo.heading, todo.content, todo.date, todo_id))
    db.commit()
    return {"message": "Todo updated successfully"}

# DELETE todo
@app.delete("/todos/{todo_id}")
def delete(todo_id: int):
    cursor.execute("DELETE FROM todos WHERE id=%s", (todo_id,))
    db.commit()
    return {"message": "Todo deleted successfully"}