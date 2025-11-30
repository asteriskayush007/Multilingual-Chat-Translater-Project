import { useState } from "react";

export default function Translator() {
  const [text, setText] = useState("");
  const [output, setOutput] = useState("");

  async function handleTranslate() {
    const res = await fetch("http://localhost:8000/translate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ text, target: "hi" })
    });

    const data = await res.json();
    setOutput(data.output);
  }

  return (
    <div>
      <h2>Translator UI</h2>

      <textarea value={text} onChange={(e)=>setText(e.target.value)} />
      <button onClick={handleTranslate}>Translate</button>

      <h3>Output:</h3>
      <p>{output}</p>
    </div>
  );
}
