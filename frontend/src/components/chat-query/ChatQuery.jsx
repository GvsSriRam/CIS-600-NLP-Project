import React from "react";
import "./ChatQuery.scss";

const ChatQuery = ({ source }) => {
  return (
    <div className="chat-query-container">
      <div className="chat-query">
        <div className="chat-question-container">
          <img className="chat-profile-pic" src={source} alt="logo" />
          <p className="chat-question">
            We've combined the power of the Following feed with the For you feed
            so there’s one place to discover content on GitHub. There’s improved
            filtering so you can customize your feed exactly how you like it,
            and a shiny new visual design. ✨
          </p>
        </div>
        <div className="chat-answer">
          <p>
            This code only provides the skeleton for the app. You would need to
            add state management for handling user interactions, and potentially
            a routing library like react-router if you have multiple pages.
            Also, if your application involves chatbot functionality, you would
            need to integrate a chatbot service, either by using third-party
            APIs or building your own service, and handle the message sending
            and receiving logic within your React components.
          </p>
        </div>
        <p className="chat-query-time">now</p>
      </div>
      {/* <p className="chat-query-time">now</p> */}
    </div>
  );
};
export default ChatQuery;
