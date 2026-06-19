import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import "./pink.css"

function Summary() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/interview/${id}/summary`)
        const data = await res.json()
        setSummary(data)
      } catch (err) {
        setError("Failed to load summary")
      } finally {
        setLoading(false)
      }
    }
    if (id) fetchSummary()
  }, [id])

  if (loading) return <div className="page-wrapper"><p className="loading-text">Generating your summary...</p></div>
  if (error) return <div className="page-wrapper"><p className="error-text">{error}</p></div>

  const scorePercent = Math.round(summary.average_score)

  return (
    <div className="page-wrapper">
      <div className="summary-hero">
        <h1 className="hero-title" style={{ fontSize: "38px" }}>Interview Complete</h1>
        <p className="hero-sub">Here's how you performed</p>
        <div className="score-ring" style={{ background: `conic-gradient(#e91e8c 0% ${scorePercent}%, #2d1020 ${scorePercent}% 100%)` }}>
          <span>{scorePercent}</span>
        </div>
      </div>
      <div className="stats-row">
        <div className="stat-card"><div className="val">{summary.total_questions}</div><div className="lbl">Total</div></div>
        <div className="stat-card"><div className="val">{summary.answered_questions}</div><div className="lbl">Answered</div></div>
        <div className="stat-card"><div className="val">{summary.average_score.toFixed(1)}</div><div className="lbl">Avg Score</div></div>
      </div>
      <div className="ai-feedback">
        <h3>AI Feedback</h3>
        <p>{summary.ai_summary}</p>
      </div>
      <button className="btn-primary" onClick={() => navigate("/")}>Start New Interview →</button>
    </div>
  )
}

export default Summary