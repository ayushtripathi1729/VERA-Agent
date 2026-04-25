"use client";

import { useState } from "react";

type Props = {
  input: string;
  setInput: (val: string) => void;
  execute: () => void;
  loading: boolean;
};

export default function InputPanel({
  input,
  setInput,
  execute,
  loading,
}: Props) {
  const [listening, setListening] = useState(false);

  // 🎙 Voice Input
  const startVoice = () => {
    try {
      const SpeechRecognition =
        (window as any).webkitSpeechRecognition ||
        (window as any).SpeechRecognition;

      if (!SpeechRecognition) {
        alert("Voice recognition not supported in this browser");
        return;
      }

      const recognition = new SpeechRecognition();
      recognition.lang = "en-US";

      setListening(true);

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setListening(false);
      };

      recognition.onerror = () => {
        setListening(false);
      };

      recognition.onend = () => {
        setListening(false);
      };

      recognition.start();
    } catch {
      setListening(false);
    }
  };

  // ⌨ Enter to execute
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!loading && input.trim()) {
        execute();
      }
    }
  };

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 glow-card">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-green-400 text-sm font-semibold tracking-wide">
          INPUT TERMINAL
        </h2>

        <span className="text-xs text-gray-400">
          {loading ? "PROCESSING..." : listening ? "LISTENING..." : "READY"}
        </span>
      </div>

      {/* TEXTAREA */}
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Enter instruction... (Press Enter to execute)"
        className="w-full min-h-[120px] resize-none p-3 rounded-md bg-black text-green-300 border border-slate-600 focus:outline-none focus:ring-1 focus:ring-green-500"
      />

      {/* ACTION BUTTON */}
      <button
        onClick={execute}
        disabled={loading || !input.trim()}
        className="mt-3 w-full bg-green-500 hover:bg-green-600 disabled:bg-gray-600 text-black font-bold py-2 rounded transition"
      >
        ▶ EXECUTE
      </button>

      {/* VOICE BUTTON */}
      <button
        onClick={startVoice}
        disabled={loading}
        className="mt-2 w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-600 text-white py-2 rounded transition"
      >
        🎙 {listening ? "Listening..." : "Speak"}
      </button>

      {/* EXAMPLES */}
      <div className="mt-3 flex flex-wrap gap-2">
        {[
          "Check if 97 is prime",
          "Find modular inverse of 7 mod 26",
          "Explain RSA encryption",
        ].map((example, i) => (
          <button
            key={i}
            onClick={() => setInput(example)}
            className="text-xs px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 transition"
          >
            {example}
          </button>
        ))}
      </div>

    </div>
  );
}
