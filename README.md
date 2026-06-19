# 🎤 AI Interview Simulator

A full-stack web application that simulates technical job interviews using AI. Users configure a personalized interview session, answer questions in a chat-style interface, and receive AI-generated scores and feedback at the end.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, React Router, CSS |
| Backend | FastAPI, SQLAlchemy, SQLite |
| AI | Google Gemini API |
| Server | Uvicorn |

---

## 📁 Project Structure

```
ai-interview-simulator/
├── backend/
│   ├── main.py          # FastAPI routes
│   ├── models.py        # SQLAlchemy DB models
│   ├── schema.py        # Pydantic schemas
│   ├── database.py      # DB connection
│   ├── ai_service.py    # Gemini AI functions
│   ├── .env             # API keys (never commit this)
│   └── venv/            # Python virtual environment
│
└── frontend/
    └── src/
        ├── App.jsx
        ├── main.jsx
        └── pages/
            ├── home.jsx
            ├── interviewer.jsx
            ├── summary.jsx
            └── pink.css
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ai-interview-simulator
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv google-genai
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend/` folder:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://aistudio.google.com/apikey

### 4. Start the Backend

```bash
uvicorn main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend runs at: `http://localhost:5174`

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/interview` | Create a new interview |
| GET | `/interview/{id}` | Get interview details |
| GET | `/interviews` | Get all interviews |
| DELETE | `/interview/{id}` | Delete an interview |
| POST | `/interview/{id}/generate-questions` | Generate AI questions |
| GET | `/interview/{id}/questions` | Get all questions |
| PATCH | `/question/{id}/answer` | Submit an answer |
| POST | `/question/{id}/evaluate` | Evaluate answer with AI |
| GET | `/interview/{id}/summary` | Get interview summary |

---

## 🖥️ Pages

### `/` — Home
- Enter the job role (e.g. Frontend Developer)
- Select difficulty: Easy / Medium / Hard
- Choose number of questions (3–30)
- Click **Start Interview** to begin

### `/interview/:id` — Interview Chat
- Chat-style interface with AI asking questions one by one
- Type your answer and hit **Send** or press **Enter**
- Each answer is scored (0–100) with instant AI feedback
- Progress bar tracks completion
- Auto-redirects to summary after the last question

### `/interview/:id/summary` — Summary
- Circular score ring showing average score
- Stats: total questions, answered, average score
- Full AI-generated feedback with strengths and improvements
- Button to start a new interview

---

## 🤖 AI Features

All AI is powered by the **Google Gemini API**:

- **Question Generation** — Generates role-specific interview questions based on difficulty
- **Answer Evaluation** — Scores each answer 0–100 with detailed feedback
- **Summary Report** — Produces an overall performance summary with strengths and areas to improve

---

## 🎨 Design

- Dark pink theme (`#1a0a10` background, `#e91e8c` accent)
- Playfair Display for headings, Inter for body text
- Fully responsive layout
- Animated AI status dot, smooth progress bar, circular score ring

---

## 🐛 Known Issues

- Google Gemini free tier has a limit of 20 requests/day per model. If you hit the limit, create a new API key at https://aistudio.google.com/apikey
- Make sure to use `"Create API key in new project"` to get full free quota

---

## 📝 Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key |

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

---

## 🙌 Author

Built by Sneha Agrawal as part of a Python internship project.