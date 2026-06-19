# AI Interview Simulator API

An AI-powered interview preparation platform built with FastAPI, PostgreSQL, SQLAlchemy, and Google Gemini. The application allows users to create interviews, generate AI-based interview questions, submit answers, receive AI-generated feedback and scores, and view a complete interview performance summary.

## Features

### Interview Management

* Create a new interview
* View all interviews
* View a single interview
* Delete an interview

### AI Question Generation

* Generate interview questions using Google Gemini
* Customize questions by:

  * Role
  * Difficulty level
  * Number of questions
* Store generated questions in PostgreSQL

### Answer Submission

* Submit answers for generated questions
* Persist answers in the database

### AI Evaluation

* Evaluate answers using Google Gemini
* Generate:

  * Score (0–100)
  * Personalized feedback
* Store evaluation results

### Interview Summary

* Calculate:

  * Total questions
  * Answered questions
  * Average score
* Generate AI-powered performance summaries
* Highlight strengths and improvement areas

## Tech Stack

### Backend

* FastAPI
* Python

### Database

* PostgreSQL
* SQLAlchemy ORM

### AI Integration

* Google Gemini API

### Validation

* Pydantic

## Project Structure

```text
backend/
│
├── main.py
├── models.py
├── schema.py
├── database.py
├── gemini_service.py
├── .env
├── requirements.txt
│
└── venv/
```

## Database Schema

### Interview

| Field         | Type     |
| ------------- | -------- |
| id            | Integer  |
| role          | String   |
| difficulty    | String   |
| num_questions | Integer  |
| score         | Integer  |
| created_at    | DateTime |

### Question

| Field        | Type    |
| ------------ | ------- |
| id           | Integer |
| interview_id | Integer |
| question     | String  |
| answer       | String  |
| feedback     | String  |
| score        | Integer |

## API Endpoints

### Interview Routes

#### Create Interview

```http
POST /interview
```

#### Get All Interviews

```http
GET /interviews
```

#### Get Single Interview

```http
GET /interview/{interview_id}
```

#### Delete Interview

```http
DELETE /interview/{interview_id}
```

---

### Question Routes

#### Generate Questions

```http
POST /interview/{interview_id}/generate-questions
```

#### Get Interview Questions

```http
GET /interview/{interview_id}/questions
```

#### Submit Answer

```http
PATCH /question/{question_id}/answer
```

#### Evaluate Answer

```http
POST /question/{question_id}/evaluate
```

---

### Summary Route

#### Interview Summary

```http
GET /interview/{interview_id}/summary
```

## How It Works

### 1. Create Interview

User creates an interview by providing:

* Role
* Difficulty
* Number of questions

### 2. Generate Questions

Google Gemini generates interview questions based on the selected role and difficulty.

### 3. Submit Answers

User submits answers for generated questions.

### 4. Evaluate Answers

Google Gemini evaluates answers and returns:

* Score
* Feedback

### 5. Generate Summary

The system calculates interview statistics and generates an AI-powered overall performance report.

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
```

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd ai-interview-simulator
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn main:app --reload
```

## Future Improvements

* JWT Authentication
* User Accounts
* Interview History
* Bulk Evaluation
* Resume Upload
* AI Follow-up Questions
* Frontend Dashboard
* Analytics and Performance Tracking

## Learning Outcomes

This project demonstrates:

* REST API Development
* FastAPI Fundamentals
* SQLAlchemy ORM
* PostgreSQL Integration
* Database Relationships
* Pydantic Validation
* CRUD Operations
* AI Integration with Gemini
* Prompt Engineering
* Backend System Design

## Author

Sneha Agrawal
