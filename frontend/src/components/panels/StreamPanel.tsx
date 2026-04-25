"use client";

import { useEffect, useRef } from "react";
import Loader from "../ui/Loader";

type Props = {
  steps: string[];
  loading: boolean;
};

export default function StreamPanel({ steps, loading }: Props) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  // 🔥 Auto-scroll to latest step
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [steps]);

  return (
    <div className="bg-slate-800/60 backdrop-blur-lg border border-slate-700 rounded-xl p-4 h-[500px] flex flex-col shadow-lg">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-blue-400 font-semibold">EXECUTION STREAM</h2>
        <span className="text-xs text-gray-400">
          {loading ? "RUNNING..." : "IDLE"}
        </span>
      </div>

      {/* STREAM AREA */}
      <div className="flex-1 overflow-y-auto text-sm font-mono space-y-2 pr-1">

        {steps.length === 0 && (
          <p className="text-gray-500">No execution yet...</p>
        )}

        {steps.map((step, index) => (
          <div
            key={index}
            className="text-green-300 animate-fadeIn"
          >
            [{new Date().toLocaleTimeString()}] {step}
          </div>
        ))}

        {/* 🔥 Loader */}
        {loading && <Loader />}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
