import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";
import lionLogo from "./assets/lion-logo.png";
import logo from "./assets/unswlogo.jpeg";
import loadingGif from "./assets/typing.gif";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input) return;

    const timestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    const newUserMessage = { text: input, sender: "user", time: timestamp };
    setMessages((messages) => [...messages, newUserMessage]);

    setIsLoading(true); // Start loading

    try {
      const response = await axios.post("http://localhost:5000/chat", {
        prompt: input,
      });
      const botMessage = {
        text: response.data.response,
        sender: "bot",
        time: timestamp,
      };
      setMessages((messages) => [...messages, botMessage]);
    } catch (error) {
      const errorMessage = {
        text: "Failed to get response from the server.",
        sender: "bot",
        time: timestamp,
      };
      setMessages((messages) => [...messages, errorMessage]);
    }

    setInput(""); // Clear input after sending
    setIsLoading(false); // Stop loading
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
            <img
              src={logo}
              alt="UNSW Logo"
              style={{ height: "100px", width: "80%" }}
            />
            <h2 style={{ color: "black", textAlign: "center" }}>
              Chat with UNSW Bot
            </h2>
            <button style={{color:"red"}} onClick={toggleChat} className="close-button">
              X
            </button>
          </div>
          <div className="messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                {msg.text} <span className="timestamp">{msg.time}</span>
              </div>
            ))}
            {isLoading && (
              <img
                src={loadingGif}
                id="loader"
                alt="Loading..."
                className="loading-gif"
              />
            )}
            <div ref={messagesEndRef} />  {/* Invisible element at the end of messages */}
          </div>
          <form onSubmit={handleSubmit} className="chat-input-controls">
            <input
              type="text"
              style={{
                marginRight: "5px",
                padding: "15px",
                borderRadius: "15px",
              }}
              value={input}
              onChange={handleInputChange}
              placeholder="Ask me anything..."
            />
            <button
              type="submit"
              style={{
                background: "yellow",
                color: "black",
                boxShadow: "2px 2px 10px rgba(0,0,0,0.2)",
              }}
            >
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;
