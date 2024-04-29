import React from "react";
import "./ChatQuery.scss";
const ChatQuery = ({ chat, source }) => {
  return (
    <div className="chat-query-container">
      <div className="chat-query">
        <div className="chat-question-container">
          <img className="chat-profile-pic" src={source} alt="logo" />
          <div>
            <p className="chat-question">{chat.question}</p>
            {chat.answer && chat.answer.result.autocorrect && (
              <p className="chat-corrected-question">
                Showing results for: "{chat.answer.result.corrected_str}"
              </p>
            )}
          </div>
        </div>
        <div className="chat-answer">
          <p>{chat.answer.result.response}</p>
        </div>
        <p className="chat-query-time">{chat.answer.result.timestamp}</p>
      </div>
    </div>
  );
};
export default ChatQuery;
