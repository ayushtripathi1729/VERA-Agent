"use client";

import { useState, useRef } from "react";
import { streamVera } from "../services/vera.stream";

export function useExecution() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [steps, setSteps] = useState<string[]>([]);
  const [output, setOutput] = useState("");
  const [goal, setGoal] = useState("");
  const [latency, setLatency] = useState(0);

  // 🔒 prevent overlapping executions
  const activeRun = useRef(false);

  const execute = () => {
    if (!input.trim() || activeRun.current) return;

    activeRun.current = true;

    setLoading(true);
    setSteps([]);
    setOutput("");
    setGoal("");
    setLatency(0);

    const startTime = performance.now();

    try {
      streamVera(input, {
        onStep: (step) => {
          setSteps((prev) => [...prev, step]);
        },

        onGoal: (g) => {
          setGoal(g);
        },

        onFinal: (finalOutput) => {
          const endTime = performance.now();
          setLatency(Math.floor(endTime - startTime));

          setOutput(finalOutput);
          setLoading(false);
          activeRun.current = false;
        },

        onError: (err) => {
          setSteps((prev) => [...prev, "❌ " + err]);
          setLoading(false);
          activeRun.current = false;
        },
      });
    } catch (err) {
      setSteps((prev) => [...prev, "❌ Execution failed"]);
      setLoading(false);
      activeRun.current = false;
    }
  };

  const reset = () => {
    setInput("");
    setSteps([]);
    setOutput("");
    setGoal("");
    setLatency(0);
    setLoading(false);
    activeRun.current = false;
  };

  return {
    input,
    setInput,
    loading,
    steps,
    output,
    goal,
    latency,
    execute,
    reset,
  };
}
