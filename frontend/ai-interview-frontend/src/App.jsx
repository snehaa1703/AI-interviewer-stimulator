import { BrowserRouter, Routes, Route } from "react-router-dom"
import Home from "./pages/home"
import InterviewChat from "./pages/interviewer"
import Summary from "./pages/summary"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/interview/:id" element={<InterviewChat />} />
        <Route path="/interview/:id/summary" element={<Summary />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App