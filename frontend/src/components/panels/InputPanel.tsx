"use client";

import { useRef } from "react";

type Props = {
  input: string;
  setInput: (val: string) => void;
  loading: boolean;
  onRun: () => void;
};

export default function InputPanel({
  input,
  setInput,
  loading,
  onRun,
}: Props) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // 🔥 Auto resize textarea
  const handleChange = (value: string) => {
    setInput(value);

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        textareaRef.current.scrollHeight + "px";
    }
  };

  // ⚡ Enter to execute
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!loading && input.trim()) {
        onRun();
      }
    }
  };

  return (
    <div className="bg-slate-800/60 backdrop-blur-lg border border-slate-700 rounded-xl p-4 shadow-lg">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-green-400 font-semibold">INPUT TERMINAL</h2>
        <span className="text-xs text-gray-400">
          {loading ? "Processing..." : "Ready"}
        </span>
      </div>

      {/* TEXTAREA */}
      <textarea
        ref={textareaRef}
        value={input}
        onChange={(e) => handleChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Enter your instruction... (Press Enter to execute)"
        className="w-full min-h-[120px] max-h-[300px] resize-none p-3 rounded-md bg-black text-green-300 border border-slate-600 focus:outline-none focus:ring-1 focus:ring-green-500 transition-all"
      />

      {/* FOOTER */}
      <div className="mt-2 flex justify-between text-xs text-gray-500">
        <span>↵ Enter to run</span>
        <span>Shift + Enter for new line</span>
      </div>

      {/* EXAMPLE PROMPTS */}
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
