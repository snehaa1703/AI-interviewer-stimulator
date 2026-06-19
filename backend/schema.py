from enum import Enum
from pydantic import BaseModel,Field


class Difficulty(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"

class InterviewCreate(BaseModel):
    role:str
    difficulty:Difficulty
    num_questions:int =Field (
        ge=3,
        le=30
    )

class InterviewResponse(BaseModel):
    id: int
    role: str
    difficulty: str
    num_questions: int
    score: int | None = None
    class Config:
        from_attributes = True
    status: str


class ScoreUpdate(BaseModel):
    score: int = Field(ge=0, le=100)

class AnswerUpdate(BaseModel):
    answer:str


class EvaluationResponse(BaseModel):
    score: int
    feedback: str

class QuestionResponse(BaseModel):
    id: int
    interview_id: int
    question: str
    answer: str | None
    feedback: str | None
    score: int | None

    class Config:
        from_attributes = True   
        
class InterviewSummaryResponse(BaseModel):
    total_questions: int
    answered_questions: int
    average_score: float
    ai_summary: str