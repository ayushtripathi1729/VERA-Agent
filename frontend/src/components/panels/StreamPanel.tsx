"use client";

import { useEffect, useRef } from "react";
import Loader from "../ui/Loader";

type Props = {
  steps: string[];
  loading: boolean;
};

/**
 * Classify step type for coloring
 */
function getStepType(step: string) {
  const s = step.toLowerCase();

  if (s.includes("plan") || s.includes("decompos") || s.includes("understand")) {
    return "planner";
  }

  if (s.includes("tool") || s.includes("execut") || s.includes("compute")) {
    return "tool";
  }

  if (s.includes("synth") || s.includes("final") || s.includes("result")) {
    return "output";
  }

  return "system";
}

export default function StreamPanel({ steps, loading }: Props) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  // 🔽 Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [steps]);

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 h-[500px] flex flex-col glow-card">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-blue-400 text-sm font-semibold tracking-wide">
          EXECUTION STREAM
        </h2>

        <span className="text-xs text-gray-400">
          {loading ? "RUNNING..." : "IDLE"}
        </span>
      </div>

      {/* STREAM */}
      <div className="flex-1 overflow-y-auto text-sm font-mono space-y-2 pr-1">

        {steps.length === 0 && (
          <p className="text-gray-500">No execution yet...</p>
        )}

        {steps.map((step, index) => {
          const type = getStepType(step);

          const color =
            type === "planner"
              ? "text-purple-400"
              : type === "tool"
              ? "text-yellow-400"
              : type === "output"
              ? "text-green-400"
              : "text-gray-400";

          return (
            <div key={index} className={`${color} animate-fadeIn`}>
              [{new Date().toLocaleTimeString()}] {step}
            </div>
          );
        })}

        {/* 🔥 Loader */}
        {loading && <Loader />}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
