"use client";

import { useExecution } from "@/hooks/useExecution";

import InputPanel from "../panels/InputPanel";
import StreamPanel from "../panels/StreamPanel";
import OutputPanel from "../panels/OutputPanel";

export default function VeraDashboard() {
  // 🧠 Core Hook
  const {
    input,
    setInput,
    loading,
    steps,
    output,
    goal,
    execute,
  } = useExecution();

  return (
    <div className="min-h-screen text-white px-6 py-4">

      {/* 🧠 HEADER */}
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-green-400">
          V.E.R.A. Neural Console
        </h1>

        <span className="text-sm text-gray-400">
          STATUS: {loading ? "PROCESSING..." : "IDLE"}
        </span>
      </div>

      {/* 🧩 MAIN GRID */}
      <div className="grid grid-cols-3 gap-4">

        {/* LEFT */}
        <InputPanel
          input={input}
          setInput={setInput}
          execute={execute}
          loading={loading}
        />

        {/* CENTER */}
        <StreamPanel
          steps={steps}
          loading={loading}
        />

        {/* RIGHT */}
        <OutputPanel
          output={output}
          goal={goal}
        />

      </div>
    </div>
  );
}
