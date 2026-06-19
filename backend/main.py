from fastapi import FastAPI, Depends, HTTPException
from database import engine, get_db
from models import Base, Interview, Question
from schema import InterviewCreate, InterviewResponse, ScoreUpdate, AnswerUpdate, QuestionResponse, InterviewSummaryResponse
from sqlalchemy.orm import Session
from ai_service import generate_questions, evaluate_answer, generate_ai_summary
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Interview Simulator API"}


@app.post("/interview")
def create_interview(data: InterviewCreate, db: Session = Depends(get_db)):
    new_interview = Interview(
        role=data.role,
        difficulty=data.difficulty.value,
        num_questions=data.num_questions,
    )
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    return {
        "id": new_interview.id,
        "role": new_interview.role,
        "difficulty": new_interview.difficulty,
        "num_questions": new_interview.num_questions,
        "score": new_interview.score
    }


@app.get("/interviews", response_model=list[InterviewResponse])
def get_interviews(db: Session = Depends(get_db)):
    interviews = db.query(Interview).all()
    return interviews


@app.get("/interview/{interview_id}")
def get_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")

    return {
        "id": interview.id,
        "role": interview.role,
        "difficulty": interview.difficulty,
        "num_questions": interview.num_questions,
        "score": interview.score
    }


@app.patch("/interview/{interview_id}/score")
def update_score(interview_id: int, data: ScoreUpdate, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")

    interview.score = data.score
    db.commit()
    db.refresh(interview)

    return {
        "message": "Score updated successfully",
        "id": interview.id,
        "score": interview.score
    }


@app.delete("/interview/{interview_id}")
def delete_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()

    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")

    db.delete(interview)
    db.commit()
    return {"message": "Interview deleted successfully"}


@app.post("/interview/{interview_id}/generate-questions")
def generate_interview_questions(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")

    questions = generate_questions(
        role=interview.role,
        difficulty=interview.difficulty,
        num_questions=interview.num_questions
    )

    for question in questions:
        new_question = Question(
            interview_id=interview.id,
            question=question
        )
        db.add(new_question)

    interview.status = "questions_generated"
    db.commit()

    return {
        "interview_id": interview.id,
        "questions": questions
    }


@app.get("/interview/{interview_id}/questions", response_model=list[QuestionResponse])
def get_questions(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")

    questions = db.query(Question).filter(
        Question.interview_id == interview_id
    ).all()

    return questions


@app.patch("/question/{question_id}/answer")
def submit_answer(question_id: int, data: AnswerUpdate, db: Session = Depends(get_db)):
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    question.answer = data.answer
    db.commit()
    db.refresh(question)

    return {"message": "Answer submitted successfully"}


@app.post("/question/{question_id}/evaluate")
def evaluate_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(404, "Question not found")

    if not question.answer:
        return {
            "score": 0,
            "feedback": "No answer provided"
        }

    try:
        result = evaluate_answer(question.question, question.answer)

        question.score = result["score"]
        question.feedback = result["feedback"]

        # ✅ Recalculate interview average score
        questions = db.query(Question).filter(
            Question.interview_id == question.interview_id
        ).all()

        scored = [q.score for q in questions if q.score is not None]

        if scored:
            interview = db.query(Interview).filter(
                Interview.id == question.interview_id
            ).first()
            interview.score = sum(scored) / len(scored)

        db.commit()
        db.refresh(question)

        return result

    except Exception as e:
        print("EVALUATE ENDPOINT ERROR:", e)
        db.rollback()

        return {
            "score": 0,
            "feedback": "Server evaluation failed"
        }


@app.get("/interview/{interview_id}/summary", response_model=InterviewSummaryResponse)
def get_summary(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")

    questions = db.query(Question).filter(
        Question.interview_id == interview_id
    ).all()

    total_questions = len(questions)
    answered_questions = 0
    total_score = 0
    interview.status = "completed"

    for q in questions:
        if q.answer is not None:
            answered_questions += 1
        if q.score is not None:
            total_score += q.score

    average_score = total_score / answered_questions if answered_questions > 0 else 0

    feedback_list = [q.feedback for q in questions if q.feedback is not None]
    feedback_text = "\n".join(feedback_list)

    ai_summary = generate_ai_summary(
        role=interview.role,
        difficulty=interview.difficulty,
        total_questions=total_questions,
        answered_questions=answered_questions,
        average_score=average_score,
        feedback_text=feedback_text
    )

    db.commit()

    return {
        "total_questions": total_questions,
        "answered_questions": answered_questions,
        "average_score": average_score,
        "ai_summary": ai_summary
    }