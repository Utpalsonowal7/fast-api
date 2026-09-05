"""
Simple FastAPI CRUD app for a To-Do list.
Great for learning: no database needed, just an in-memory list.

Run with:
    uvicorn main:app --reload

Then open:
    http://127.0.0.1:8000/docs   <- interactive Swagger UI (try it here!)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="To-Do List API")

# ---------------------------------------------------------
# "Database" — just a Python list living in memory.
# Data resets every time you restart the server.
# ---------------------------------------------------------
todos = []
next_id = 1


# ---------------------------------------------------------
# Pydantic models define the shape of data going in/out.
# ---------------------------------------------------------
class TodoCreate(BaseModel):
    title: str
    done: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


class Todo(BaseModel):
    id: int
    title: str
    done: bool


# ---------------------------------------------------------
# CREATE — add a new to-do
# ---------------------------------------------------------
@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = {"id": next_id, "title": todo.title, "done": todo.done}
    todos.append(new_todo)
    next_id += 1
    return new_todo


# ---------------------------------------------------------
# READ — list all to-dos
# ---------------------------------------------------------
@app.get("/todos", response_model=list[Todo])
def list_todos():
    return todos


# ---------------------------------------------------------
# READ — get a single to-do by id
# ---------------------------------------------------------
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# ---------------------------------------------------------
# UPDATE — change title and/or done status
# ---------------------------------------------------------
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, update: TodoUpdate):
    for todo in todos:
        if todo["id"] == todo_id:
            if update.title is not None:
                todo["title"] = update.title
            if update.done is not None:
                todo["done"] = update.done
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# ---------------------------------------------------------
# DELETE — remove a to-do
# ---------------------------------------------------------
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return
    raise HTTPException(status_code=404, detail="Todo not found")