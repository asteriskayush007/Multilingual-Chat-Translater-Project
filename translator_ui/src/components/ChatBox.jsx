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

  // Connect websocket safely
  useEffect(() => {
    if (ws.current) {
      try { ws.current.close(); } catch {}
    }

    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/${user}`);
    ws.current = socket;

    socket.onopen = () => {
      socket.send(JSON.stringify({ type: "set_lang", lang: myLang }));
    };

    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === "lang_ack") return;
      setMessages(prev => [...prev, msg]);
    };

    return () => {
      try { socket.close(); } catch {}
    };
  }, [user, myLang]);

  // Auto scroll
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  // Send message
  const sendMessage = () => {
    if (!text.trim()) return;
    if (!ws.current || ws.current.readyState !== 1) return;

    ws.current.send(JSON.stringify({
      type: "message",
      text,
      translate: translateOption,
    }));

    setText("");
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Download chat screenshot
  const downloadChat = async () => {
    const canvas = await html2canvas(containerRef.current, {
      backgroundColor: "#111827",
      scale: 2,
    });
    const link = document.createElement("a");
    link.download = `chat_${user}.png`;
    link.href = canvas.toDataURL("image/png");
    link.click();
  };

  return (
    <div
      ref={containerRef}
      className="flex flex-col h-screen bg-gradient-to-br from-gray-900 to-black text-white p-4"
    >

      {/* HEADER */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex justify-between items-center mb-4"
      >
        <h2 className="text-xl font-semibold">👤 Logged in as: {user}</h2>

        <button
          onClick={downloadChat}
          className="px-4 py-2 bg-green-600 hover:bg-green-500 transition rounded-lg shadow-lg"
        >
          📥 Download Chat
        </button>
      </motion.div>

      {/* LANGUAGE + TOGGLE */}
      <div className="flex gap-3 mb-4 items-center">
        <select
          value={myLang}
          onChange={(e) => setMyLang(e.target.value)}
          className="p-2 rounded bg-gray-100 text-black shadow"
        >
          <option value="en">English</option>
          <option value="hi">Hindi</option>
          <option value="fr">French</option>
          <option value="bn">Bengali</option>
          <option value="mr">Marathi</option>
        </select>

        <label className="flex items-center gap-2 text-gray-300">
          <input
            type="checkbox"
            checked={translateOption}
            onChange={() => setTranslateOption(!translateOption)}
          />
          Translate
        </label>
      </div>

      {/* CHAT WINDOW */}
      <div
        ref={chatRef}
        className="flex-1 overflow-auto rounded-lg p-4 bg-gray-800 bg-opacity-40 backdrop-blur-lg shadow-inner"
      >
        {messages.length === 0 && (
          <p className="text-gray-400 text-center mt-10">Start chatting…</p>
        )}

        {messages.map((msg, i) => {
          const isMe = msg.sender === user;
          const textToShow = isMe ? msg.original : msg.translated;

          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: isMe ? 50 : -50 }}
              animate={{ opacity: 1, x: 0 }}
              className={`mb-3 flex ${isMe ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`
                  max-w-xs px-4 py-2 rounded-xl shadow-md 
                  ${isMe
                    ? "bg-blue-600 text-white rounded-br-none"
                    : "bg-gray-700 text-white rounded-bl-none"}
                `}
              >
                <div>{textToShow}</div>

                {/* Latency Display */}
                {msg.latency && (
                  <div className="text-[10px] opacity-60 mt-1">
                    ⏱ {msg.latency} ms
                  </div>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* INPUT BOX */}
      <div className="mt-3 flex gap-3 items-center">
        <textarea
          rows={2}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKey}
          className="flex-1 p-3 rounded-lg text-black resize-none shadow-lg"
          placeholder="Type your message..."
        />

        <button
          onClick={sendMessage}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-500 shadow-lg rounded-xl transition text-white font-semibold"
        >
          Send
        </button>
      </div>
    </div>
  );
}
