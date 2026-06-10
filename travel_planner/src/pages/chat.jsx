import React, { useState } from "react";
import { sendMessage } from "../api";

export default function Chat() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [chatId, setChatId] = useState(null);

  const token = localStorage.getItem("token");

  const handleSend = async () => {
    const res = await sendMessage(message, chatId, token);

    setChatId(res.chat_id);

    setChat((prev) => [
      ...prev,
      { role: "user", text: message },
      { role: "bot", text: res.response },
    ]);

    setMessage("");
  };

  return (
    <div>
      <h2>Travel Chat</h2>

      <div style={{ height: 400, overflow: "auto", border: "1px solid gray" }}>
        {chat.map((c, i) => (
          <div key={i}>
            <b>{c.role}:</b> {c.text}
          </div>
        ))}
      </div>

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask travel plan..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}