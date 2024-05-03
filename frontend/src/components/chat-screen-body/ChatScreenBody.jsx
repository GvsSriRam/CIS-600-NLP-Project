import React from "react";
import "./ChatScreenBody.scss";
import ChatQuery from "./../chat-query/ChatQuery.jsx";

// Render the ChatScreenBody component
const ChatScreenBody = ({ chatLog, source }) => {
  return (
    <div className="chat-screen-body">
      {/* Map through the chatLog array and render a ChatQuery component for each chat */}
      {chatLog.map((chat, index) => (
        <ChatQuery chat={chat} source={source} key={index} />
      ))}
    </div>
  );
};

export default ChatScreenBody;
