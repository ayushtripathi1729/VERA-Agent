"use client";

type Props = {
  raw: string;
  onRetry: () => void;
};

export default function DevConsole({ raw, onRetry }: Props) {
  // 📋 Copy raw output
  const handleCopy = () => {
    if (!raw) return;
    navigator.clipboard.writeText(raw);
  };

  return (
    <div className="bg-black/60 border border-slate-700 rounded-xl p-3 text-xs glow-card">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-2">
        <span className="text-gray-400 tracking-wide">
          DEV CONSOLE
        </span>

        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded"
          >
            Copy
          </button>

          <button
            onClick={onRetry}
            className="px-2 py-1 bg-green-600 hover:bg-green-500 rounded"
          >
            Retry
          </button>
        </div>
      </div>

      {/* CONTENT */}
      <pre className="whitespace-pre-wrap text-green-300 max-h-[180px] overflow-y-auto">
        {raw || "No data yet..."}
      </pre>

    </div>
  );
}
