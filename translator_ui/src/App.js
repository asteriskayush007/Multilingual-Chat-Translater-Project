import React, { useState } from "react";
import ChatBox from "./components/ChatBox";

function App() {
  const [user, setUser] = useState(null);

  if (!user) {
    // simple login screen
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
        <h1 className="text-2xl mb-4">Login as A or B</h1>
        <div className="flex gap-4">
          <button
            onClick={() => setUser("A")}
            className="px-4 py-2 bg-blue-600 rounded"
          >
            Login as A
          </button>
          <button
            onClick={() => setUser("B")}
            className="px-4 py-2 bg-green-600 rounded"
          >
            Login as B
          </button>
        </div>
      </div>
    );
  }

  return <ChatBox user={user} />;
}

export default App;
