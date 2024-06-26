import React, { useState } from "react";
import "./App.css";
import logo from "./cred-icon.svg";
import downArrowIcon from "./assets/icons/down-arrow.svg";
import chatIcon from "./assets/icons/dark.svg";
import infoIcon from "./assets/icons/info.svg";
import settingsIcon from "./assets/icons/settings.svg";
import FAQIcon from "./assets/icons/faq-2.svg";
import defaultImg from "./assets/img/default-pic.jpeg";
import voiceIcon from "./assets/icons/voice.svg";
import addImageIcon from "./assets/icons/add-img.svg";
import MenuItem from "./components/menu-item/MenuItem.jsx";
import ChatScreenBody from "./components/chat-screen-body/ChatScreenBody.jsx";
import { useEffect } from "react";

const App = () => {
  // State for tracking if the app is focused
  const [isFocused, setIsFocused] = useState(false);
  // State for tracking the user's input
  const [input, setInput] = useState("");
  // State for tracking the chat log
  const [chatLog, setChatLog] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // fetch response to the api combining the chatlog array of messages and sending it as a message to http://0.0.0.0:8000/nlp/chat as a post request
    const response = await fetch("http://localhost:8000/nlp/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input,
      }),
    });
    const reply = await response.json();
    setChatLog([...chatLog, { question: input, answer: reply }]);
    setInput("");
  };
  useEffect(() => {
    console.log(chatLog);
  });

  return (
    <div className="main-container">
      <div className="side-nav">
        <div className="top-nav">
          <div className="logo-container">
            <img className="logo" src={logo} alt="logo" />
          </div>
          <div className="main-menu-group">
            <div className="main-menu-container">
              <img className="down-arrow" src={downArrowIcon} alt="logo" /> Main
              Menu
            </div>
            <MenuItem source={chatIcon} name={"Chatbot"} isSelected={true} />
            <MenuItem source={infoIcon} name={"More Info"} isSelected={false} />
          </div>
        </div>

        <div className="bottom-nav">
          <hr
            style={{
              backgroundColor: "#1D1D1D",
              height: "1px",
              border: "none",
            }}
          />
          <div className="setting-faq-group">
            <MenuItem source={FAQIcon} name={"FAQ"} isSelected={false} />
            <MenuItem
              source={settingsIcon}
              name={"Settings"}
              isSelected={false}
            />
          </div>
          <div className="upgrade-logout-group">
            <div className="profile-container">
              <img className="profile-pic" src={defaultImg} alt="logo" />
              <div>
                <p className="profile-name">Prabas</p>
                <p className="profile-email">mahendrabahubali@gmail.com</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="main-body-container">
        <div className="main-body">
          <h2 className="main-body-heading">Credit Card Management Chatbot</h2>
          <div className="chat-screen-container">
            <ChatScreenBody chatLog={chatLog} source={defaultImg} />
          </div>
          <form onSubmit={handleSubmit}>
            <div
              className={`input-box-container ${isFocused ? "focused" : ""}`}
            >
              <img className="voice-icon" src={addImageIcon} alt="logo" />
              <input
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="text-input"
                placeholder="Start typing here..."
                type="text"
                accept=".txt"
              />
              <img className="voice-icon" src={voiceIcon} alt="logo" />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default App;
