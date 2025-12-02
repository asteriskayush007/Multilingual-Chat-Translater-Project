// src/components/ChatBox.jsx
import React, { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import html2canvas from "html2canvas";

export default function ChatBox({ user }) {
  const [text, setText] = useState("");
  const [messages, setMessages] = useState([]);
  const [myLang, setMyLang] = useState(user === "A" ? "en" : "hi");
  const [translateOption, setTranslateOption] = useState(true);

  const ws = useRef(null);
  const chatRef = useRef(null);
  const containerRef = useRef(null);

  // ⭐ SAFE WEBSOCKET INIT
  useEffect(() => {
    if (ws.current) {
      try { ws.current.close(); } catch (e) {}
    }

    const socket = new WebSocket(`wss://multilingual-chat-translater-project.onrender.com/ws/${user}`);
    ws.current = socket;

    socket.onopen = () => {
      socket.send(
        JSON.stringify({
          type: "set_lang",
          lang: myLang
        })
      );
    };

    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === "lang_ack") return;
      setMessages((prev) => [...prev, msg]);
    };

    socket.onerror = (err) => console.log("WS Error:", err);

    socket.onclose = () => console.log("WS closed");

    return () => {
      try { socket.close(); } catch {}
    };
  }, [user, myLang]);

  // Scroll bottom
  useEffect(() => {
    if (chatRef.current)
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
  }, [messages]);

  // ⭐ SAFE SEND (no red screen)
  const sendMessage = () => {
    if (!text.trim()) return;
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      console.log("⚠ WS not open yet");
      return;
    }

    ws.current.send(
      JSON.stringify({
        type: "message",
        text,
        translate: translateOption
      })
    );

    setText("");
  };

  // Enter to send
  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Download chat as image
  const downloadChat = async () => {
    const canvas = await html2canvas(containerRef.current, {
      backgroundColor: null,
      scale: 2
    });
    const link = document.createElement("a");
    link.download = `chat_${user}.png`;
    link.href = canvas.toDataURL();
    link.click();
  };

  return (
    <div ref={containerRef} className="flex flex-col h-screen bg-gray-900 text-white p-4">

      {/* Header */}
      <div className="flex justify-between items-center mb-3">
        <h2>Logged in as: {user}</h2>
        <button
          onClick={downloadChat}
          className="px-3 py-1 bg-green-600 rounded"
        >
          📥 Download Chat
        </button>
      </div>

      {/* Lang + Toggle */}
      <div className="flex gap-2 mb-3 items-center">
        <select
          className="p-2 rounded text-black"
          value={myLang}
          onChange={(e) => setMyLang(e.target.value)}
        >
          <option value="en">English</option>
          <option value="hi">Hindi</option>
          <option value="fr">French</option>
          <option value="bn">Bengali</option>
          <option value="mr">Marathi</option>
        </select>

        <label className="flex items-center gap-1 text-black">
          <input
            type="checkbox"
            checked={translateOption}
            onChange={() => setTranslateOption(!translateOption)}
          />
          Translate
        </label>
      </div>

      {/* Chat messages */}
      <div ref={chatRef} className="flex-1 overflow-auto bg-gray-800 p-4 rounded mb-3">
        {messages.length === 0 && <p className="text-gray-400">Start chatting…</p>}

        {messages.map((msg, i) => {
          const isMe = msg.sender === user;
          const textToShow = isMe ? msg.original : msg.translated;

          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex mb-2 ${isMe ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`px-3 py-2 max-w-xs rounded-lg ${
                  isMe ? "bg-blue-600 rounded-br-none" : "bg-gray-600 rounded-bl-none"
                }`}
              >
                {textToShow}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <textarea
          rows={2}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKey}
          className="flex-1 p-2 rounded text-black"
          placeholder="Type a message..."
        />
        <button
          onClick={sendMessage}
          className="px-4 py-2 bg-blue-600 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}
