import { useState } from 'react'
import './App.css'
import LiveKitModal from './components/LiveKitModal';

function App() {
  const [showSupport, setShowSupport] = useState(false);

  const handleSupportClick = () => {
    setShowSupport(true)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">TutorAgent</div>
      </header>

      <main>
        <section className="hero">
          <h1>Welcome to Your Voice Tutor</h1>
          <p>Ask questions and learn in real-time.</p>
          <div className="search-bar">
            <input type="text" placeholder='Enter your question or topic'></input>
            <button>Ask</button>
          </div>
        </section>

        <button className="support-button" onClick={handleSupportClick}>
          Start Tutoring Session
        </button>
      </main>

      {showSupport && <LiveKitModal setShowSupport={setShowSupport}/>}
    </div>
  )
}

export default App
