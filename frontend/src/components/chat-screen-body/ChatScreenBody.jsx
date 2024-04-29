import React from "react";
import "./ChatScreenBody.scss";
import ChatQuery from "./../chat-query/ChatQuery.jsx";
const ChatScreenBody = ({ chatLog, source }) => {
  return (
    <div className="chat-screen-body">
      {chatLog.map((chat, index) => (
        <ChatQuery chat={chat} source={source} key={index} />
      ))}
      {/* <ChatQuery source={source} />
      <ChatQuery source={source} />
      {/* <ChatQuery source={source} />
      <ChatQuery source={source} />
      <ChatQuery source={source} /> */}
    </div>
  );
};
export default ChatScreenBody;
