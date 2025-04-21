from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
Base = declarative_base()

#ORM Models
class Task(Base):
  __tablename__ = "tasks"
  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String, nullable=False)
  description = Column(Text, nullable=True)
  due_date = Column(TIMESTAMP, nullable=True)
  is_completed = Column(Boolean, default=False)
  created_at = Column(TIMESTAMP, default=datetime.utcnow)