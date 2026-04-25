"use client";

import TypingEffect from "../ui/TypingEffect";

type Props = {
  output: string;
  goal: string;
};

export default function OutputPanel({ output, goal }: Props) {

  // 📋 Copy to clipboard
  const handleCopy = () => {
    if (!output) return;
    navigator.clipboard.writeText(output);
  };

  // ⬇ Download as file
  const handleDownload = () => {
    if (!output) return;

    const blob = new Blob([output], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "vera_output.txt";
    a.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-slate-800/60 backdrop-blur-lg border border-slate-700 rounded-xl p-4 h-[500px] flex flex-col shadow-lg">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-purple-400 font-semibold">OUTPUT</h2>

        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="text-xs px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded"
          >
            Copy
          </button>

          <button
            onClick={handleDownload}
            className="text-xs px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded"
          >
            Download
          </button>
        </div>
      </div>

      {/* CONTENT */}
      <div className="flex-1 overflow-y-auto text-sm space-y-3 pr-1">

        {!output && (
          <p className="text-gray-500">No output yet...</p>
        )}

        {/* 🎯 GOAL */}
        {goal && (
          <div>
            <h3 className="text-blue-400 font-semibold mb-1">🎯 Objective</h3>
            <p className="text-gray-300 whitespace-pre-wrap">{goal}</p>
          </div>
        )}

        {/* ✅ RESULT */}
        {output && (
          <div>
            <h3 className="text-green-400 font-semibold mb-1">✅ Result</h3>

            <div className="bg-black p-3 rounded border border-slate-600 text-green-300">
              <TypingEffect text={output} />
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
