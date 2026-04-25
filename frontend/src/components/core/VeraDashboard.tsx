"use client";

import { useState, useEffect } from "react";

import { useExecution } from "@/hooks/useExecution";

import InputPanel from "../panels/InputPanel";
import StreamPanel from "../panels/StreamPanel";
import OutputPanel from "../panels/OutputPanel";
import ImagePanel from "../panels/ImagePanel";
import AgentBoard from "../panels/AgentBoard";

import ActionBar from "../controls/ActionBar";

import StatusBar from "../hud/StatusBar";
import DevConsole from "../hud/DevConsole";

export default function VeraDashboard() {
  // 🧠 Execution Hook
  const {
    input,
    setInput,
    loading,
    steps,
    output,
    goal,
    execute,
    reset,
    latency,
  } = useExecution();

  // ⚡ Boot screen effect
  const [booting, setBooting] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setBooting(false), 1200);
    return () => clearTimeout(timer);
  }, []);

  if (booting) {
    return (
      <div className="h-screen flex items-center justify-center text-green-400 text-xl animate-pulse">
        🧠 Initializing V.E.R.A...
      </div>
    );
  }

  return (
    <div className="p-4 text-white">

      {/* 🧠 HEADER */}
      <div className="mb-3">
        <h1 className="text-3xl font-bold text-green-400 tracking-wide">
          V.E.R.A Neural Console
        </h1>
      </div>

      {/* 📊 STATUS */}
      <StatusBar loading={loading} latency={latency} />

      {/* 🎛 CONTROLS */}
      <div className="flex gap-2 mt-3">
        <button
          onClick={execute}
          className="px-3 py-1 bg-green-500 text-black rounded"
        >
          ▶ Run
        </button>

        <button
          onClick={reset}
          className="px-3 py-1 bg-red-500 text-white rounded"
        >
          Reset
        </button>
      </div>

      {/* 🧩 MAIN GRID */}
      <div className="grid grid-cols-4 gap-4 mt-4">

        {/* LEFT PANEL */}
        <div className="col-span-1 space-y-4">
          <InputPanel
            input={input}
            setInput={setInput}
            execute={execute}
            loading={loading}
          />

          <ActionBar
            setInput={setInput}
            execute={execute}
            loading={loading}
          />

          <ImagePanel input={input} />
        </div>

        {/* CENTER PANEL */}
        <div className="col-span-2 space-y-4">
          <StreamPanel steps={steps} loading={loading} />
          <AgentBoard steps={steps} />
        </div>

        {/* RIGHT PANEL */}
        <div className="col-span-1 space-y-4">
          <OutputPanel output={output} goal={goal} />

          <DevConsole
            raw={output}
            onRetry={execute}
          />
        </div>

      </div>
    </div>
  );
}
