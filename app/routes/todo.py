import os
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from datetime import datetime

#Instantiate environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

#DB functionality
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

#ORM Models
class Task(Base):
  __tablename__ = "tasks"
  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String, nullable=False)
  description = Column(Text, nullable=True)
  due_date = Column(TIMESTAMP, nullable=True)
  is_completed = Column(Boolean, default=False)
  created_at = Column(TIMESTAMP, default=datetime.utcnow)

# Schemas
class TaskCreate(BaseModel):
  title: str
  description: Optional[str]
  due_date: Optional[datetime]

class TaskOut(TaskCreate):
  id: int
  is_completed: bool
  created_at: datetime

  model_config = {
    "from_attributes": True
  }


#Start FastAPI Instance
app = FastAPI()
router = APIRouter()

#Routes
@router.post("/tasks/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
  db_task = Task(**task.dict())
  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  return db_task

@router.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
  task = db.query(Task).filter(Task.id == task_id).first()
  if not task:
    raise HTTPException(status_code=404, detail="Task not found")
  return task

@router.get("/tasks/", response_model=List[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
  return db.query(Task).all()

# Projects
# @router.post("/projects/", response_model=ProjectOut)
# def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
#   db_project = Project(**project.dict())
#   db.add(db_project)
#   db.commit()
#   db.refresh(db_project)
#   return db_project

# @router.get("/projects/{project_id}", response_model=ProjectOut)
# def read_project(project_id: int, db: Session = Depends(get_db)):
#   project = db.query(Project).filter(Project.id == project_id).first()
#   if not project:
#     raise HTTPException(status_code=404, detail="Project not found")
#   return project

# @router.get("/projects/", response_model=List[ProjectOut])
# def list_projects(db: Session = Depends(get_db)):
#   return db.query(Project).all()

app.include_router(router)