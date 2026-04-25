"use client";

import { useState } from "react";

// Temporary placeholders (we will build these next)
const Placeholder = ({ title }: { title: string }) => (
  <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 h-[300px] flex items-center justify-center text-gray-400">
    {title}
  </div>
);

export default function VeraDashboard() {
  // 🧠 Core State
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [steps, setSteps] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

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

        {/* LEFT PANEL */}
        <div className="flex flex-col gap-4">
          <Placeholder title="Input Panel (next)" />
          <Placeholder title="Control Panel (next)" />
        </div>

        {/* CENTER PANEL */}
        <div>
          <Placeholder title="Execution Stream (next)" />
        </div>

        {/* RIGHT PANEL */}
        <div>
          <Placeholder title="Output Panel (next)" />
        </div>

      </div>
    </div>
  );
}
