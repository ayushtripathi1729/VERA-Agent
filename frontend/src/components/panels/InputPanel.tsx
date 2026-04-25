"use client";

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

  // 🔥 Enter to execute (Shift+Enter for newline)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!loading && input.trim()) {
        execute();
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
