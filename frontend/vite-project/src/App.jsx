import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import lionLogo from './assets/lion-logo.png';
import logo from './assets/unswlogo.jpeg';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input) return;

    const timestamp = new Date().toLocaleTimeString();
    const newUserMessage = { text: input, sender: 'user', time: timestamp };
    setMessages(messages => [...messages, newUserMessage]);
    
    try {
      const response = await axios.post('http://localhost:5000/chat', { prompt: input });
      const botMessage = { text: response.data.response, sender: 'bot', time: timestamp };
      setMessages(messages => [...messages, botMessage]);
    } catch (error) {
      const errorMessage = { text: "Failed to get response from the server.", sender: 'bot', time: timestamp };
      setMessages(messages => [...messages, errorMessage]);
    }

    setInput('');
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="App">
      {!isOpen && (
        <div className="chat-icon" onClick={toggleChat}>
          <img src={lionLogo} alt="Chat with UNSW Bot" />
        </div>
      )}

      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <img src={logo} alt="UNSW Logo" style={{ height: '80%', width: "30%" }} />
            <h2 style={{ color: "black",textAlign:"center" }}>Chat with UNSW Bot</h2>
            <button onClick={toggleChat} style={{color:"red",alignSelf:"baseline"}} id="close-button">X</button>
          </div>
          <div className="messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                {msg.text} <span className="timestamp">{msg.time}</span>
              </div>
            ))}
          </div>
          <form onSubmit={handleSubmit} id='chat-input-controls'>
            <input type="text" style={{ marginRight: "5px", padding: "15px", borderRadius: "15px" }} value={input} onChange={handleInputChange} placeholder="Ask me anything..." />
            <button type="submit" style={{ background: "yellow", color: "black", boxShadow: "2px 2px 10px rgba(0,0,0,0.2)" }}>Send</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;
