import React, { useEffect } from "react";
import "./ChatQuery.scss";

const ChatQuery = ({ chat, source }) => {
  useEffect(() => {
    console.log("here", chat);
  }, [chat]);
  return (
    <div className="chat-query-container">
      <div className="chat-query">
        <div className="chat-question-container">
          <img className="chat-profile-pic" src={source} alt="logo" />
          <div>
            <p className="chat-question">{chat.question}</p>
            {chat.answer && chat.answer.result.autocorrect && (
              <p className="chat-corrected-question">
                {chat.answer.result.corrected_str}
              </p>
            )}
          </div>
        </div>
        <div className="chat-answer">
          <p>{chat.answer.result.response}</p>
        </div>
        <p className="chat-query-time">now</p>
      </div>
      {/* <p className="chat-query-time">now</p> */}
    </div>
  );
};
export default ChatQuery;
