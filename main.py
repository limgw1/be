from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.routes import todo

app = FastAPI()

app.include_router(todo.router)

@app.get("/")
async def root():
    return {"message": "Health Check! App seems to be running"}