import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import "./pink.css"

function InterviewChat() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [questions, setQuestions] = useState([])
  const [answer, setAnswer] = useState("")
  const [index, setIndex] = useState(0)
  const [chat, setChat] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/interview/${id}/questions`)
        const data = await res.json()
        if (!Array.isArray(data)) { console.log("NOT ARRAY:", data); return }
        setQuestions(data)
        if (data.length > 0) setChat([{ role: "ai", text: data[0].question }])
      } catch (err) {
        console.log("FETCH ERROR:", err)
      }
    }
    if (id) fetchQuestions()
  }, [id])

  const sendAnswer = async () => {
    if (!answer || loading) return
    setLoading(true)
    const currentQ = questions[index]
    if (!currentQ) { setLoading(false); return }

    setChat(prev => [...prev, { role: "user", text: answer }])

    await fetch(`http://127.0.0.1:8000/question/${currentQ.id}/answer`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answer }),
    })

    const res = await fetch(`http://127.0.0.1:8000/question/${currentQ.id}/evaluate`, { method: "POST" })
    const result = await res.json()

    setChat(prev => [...prev, { role: "score", text: `Score: ${result.score || 0} | ${result.feedback || "No feedback"}` }])
    setAnswer("")

    const next = index + 1
    if (next < questions.length) {
      setIndex(next)
      setChat(prev => [...prev, { role: "ai", text: questions[next].question }])
    } else {
      setChat(prev => [...prev, { role: "ai", text: "🎉 Interview Completed! Redirecting..." }])
      setTimeout(() => navigate(`/interview/${id}/summary`), 2000)
    }
    setLoading(false)
  }

  const progress = questions.length > 0 ? (index / questions.length) * 100 : 0

  return (
    <div className="page-wrapper">
      <div className="chat-header">
        <div className="ai-dot" />
        <h2>Interview in Progress</h2>
      </div>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>
      <div className="chat-messages">
        {chat.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>{m.text}</div>
        ))}
      </div>
      <div className="chat-input-row">
        <input value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Type your answer..." onKeyDown={(e) => e.key === "Enter" && sendAnswer()} />
        <button className="btn-send" onClick={sendAnswer} disabled={loading}>{loading ? "..." : "Send"}</button>
      </div>
    </div>
  )
}

export default InterviewChat