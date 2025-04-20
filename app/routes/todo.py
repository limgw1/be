from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()
router = APIRouter()

class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool = False

todos: List[TodoItem] = []

@router.get("/todos", response_model=List[TodoItem])
async def get_todos():
    return todos

@router.post("/todos", response_model=TodoItem)
async def create_todo(item: TodoItem):
    todos.append(item)
    return item

@router.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, updated: TodoItem):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[index]
            return {"detail": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")

app.include_router(router)