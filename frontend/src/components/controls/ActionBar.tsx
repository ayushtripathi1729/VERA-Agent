"use client";

type Props = {
  setInput: (val: string) => void;
  execute: () => void;
  loading: boolean;
};

const EXAMPLES = [
  "Check if 97 is prime",
  "Find modular inverse of 7 mod 26",
  "Explain RSA encryption",
  "Audit the security of an API",
  "Latest AI research trends",
];

export default function ActionBar({ setInput, execute, loading }: Props) {
  const handleClick = (text: string) => {
    setInput(text);

    // small delay so input updates visually before execution
    setTimeout(() => {
      if (!loading) execute();
    }, 150);
  };

  return (
    <div className="bg-slate-900/60 border border-slate-700 rounded-xl p-3 glow-card">

      {/* HEADER */}
      <h3 className="text-xs text-gray-400 mb-2 tracking-wide">
        QUICK ACTIONS
      </h3>

      {/* BUTTONS */}
      <div className="flex flex-wrap gap-2">
        {EXAMPLES.map((example, index) => (
          <button
            key={index}
            onClick={() => handleClick(example)}
            disabled={loading}
            className="text-xs px-3 py-1 rounded bg-slate-700 hover:bg-slate-600 disabled:bg-gray-700 disabled:cursor-not-allowed transition"
          >
            {example}
          </button>
        ))}
      </div>

    </div>
  );
}
