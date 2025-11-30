import React from "react";

export default function Sidebar({ dark, setDark }) {
  return (
    <aside className={`w-72 p-6 ${dark ? "bg-gray-900 text-gray-100" : "bg-white text-gray-900"} shadow-lg`}>
      <h1 className="text-2xl font-bold mb-4">🌐 LinguaLive</h1>

      <button
        onClick={() => setDark(!dark)}
        className="mb-4 px-4 py-2 rounded-lg bg-blue-500 text-white"
      >
        {dark ? "Light Mode" : "Dark Mode"}
      </button>

      <div className="text-sm">
        <p className="font-medium">Features</p>
        <ul className="mt-3 space-y-2">
          <li>• Live Translation</li>
          <li>• Latency Meter</li>
          <li>• Auto-detect</li>
          <li>• Model Fallback</li>
          <li>• Download Chat</li>
        </ul>
      </div>
    </aside>
  );
}
