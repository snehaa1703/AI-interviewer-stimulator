from sqlalchemy import Column, Integer, String,ForeignKey,Text
from database import Base
from sqlalchemy import DateTime
from datetime import datetime

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String,nullable=False)
    difficulty = Column(String,nullable=False)
    num_questions=Column(Integer,nullable=False)
    score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String,nullable=False,default="created")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(
        Integer,
        ForeignKey("interviews.id"),
        nullable=False
    )
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)
