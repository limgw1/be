from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
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