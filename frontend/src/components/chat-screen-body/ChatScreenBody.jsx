import React from "react";
import "./ChatScreenBody.scss";
import ChatQuery from "./../chat-query/ChatQuery.jsx";
const ChatScreenBody = ({ source }) => {
  return (
    <div className="chat-screen-body">
      <ChatQuery source={source} />
      <ChatQuery source={source} />
      <ChatQuery source={source} />
      <ChatQuery source={source} />
    </div>
  );
};
export default ChatScreenBody;
