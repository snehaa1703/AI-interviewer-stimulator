import { useState } from "react"
import { useNavigate } from "react-router-dom"
import "./pink.css"

function Home() {
  const [role, setRole] = useState("")
  const [difficulty, setDifficulty] = useState("Medium")
  const [numQuestions, setNumQuestions] = useState(5)
  const navigate = useNavigate()

  const handleStart = async () => {
    if (!role.trim()) { alert("Please enter a role"); return }
    try {
      const res = await fetch("http://127.0.0.1:8000/interview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role, difficulty, num_questions: numQuestions }),
      })
      const data = await res.json()
      if (!res.ok) return console.error(data)
      await fetch(`http://127.0.0.1:8000/interview/${data.id}/generate-questions`, { method: "POST" })
      navigate(`/interview/${data.id}`)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="page-wrapper">
      <div className="home-hero">
        <h1 className="hero-title">AI Interview<br />Simulator</h1>
        <p className="hero-sub">Practice. Improve. Get hired.</p>
      </div>
      <div className="form-card">
        <div className="form-group">
          <label>Role</label>
          <input placeholder="e.g. Frontend Developer" value={role} onChange={(e) => setRole(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Difficulty</label>
          <div className="pill-group">
            {["Easy", "Medium", "Hard"].map((d) => (
              <button key={d} className={`pill ${difficulty === d ? "active" : ""}`} onClick={() => setDifficulty(d)}>{d}</button>
            ))}
          </div>
        </div>
        <div className="form-group">
          <label>Number of Questions</label>
          <input type="number" min={3} max={30} value={numQuestions} onChange={(e) => setNumQuestions(Number(e.target.value))} />
        </div>
        <button className="btn-primary" onClick={handleStart}>Start Interview →</button>
      </div>
    </div>
  )
}

export default Home