"use client";

import { useState } from "react";
import { runVera, VeraResponse } from "@/services/vera.service";

export function useExecution() {
  // 🧠 STATE
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [steps, setSteps] = useState<string[]>([]);
  const [output, setOutput] = useState("");
  const [goal, setGoal] = useState("");

  // 🚀 MAIN EXECUTION FUNCTION
  const execute = async () => {
    if (!input.trim()) return;

    setLoading(true);

    // 🔥 Initial fake stream
    setSteps([
      "🧠 Initializing V.E.R.A...",
      "⚙️ Parsing instruction...",
    ]);

    try {
      const res: VeraResponse = await runVera(input);

      // 🧠 Update goal
      setGoal(res.goal || "");

      // ⚡ Simulate intelligent step streaming
      const simulatedSteps = [
        "🧠 Planning execution...",
        "🔍 Analyzing problem...",
        "🛠 Selecting tools...",
        "⚙️ Executing steps...",
        "✅ Finalizing output...",
      ];

      for (let i = 0; i < simulatedSteps.length; i++) {
        await new Promise((r) => setTimeout(r, 400));
        setSteps((prev) => [...prev, simulatedSteps[i]]);
      }

      // 📊 Set final output
      setOutput(res.logs || "No output received.");

    } catch (err) {
      setOutput("❌ Execution failed. Please check backend.");
      setSteps((prev) => [...prev, "❌ Error occurred"]);
    }

    setLoading(false);
  };

  // 🔄 RESET FUNCTION
  const reset = () => {
    setInput("");
    setSteps([]);
    setOutput("");
    setGoal("");
    setLoading(false);
  };

  return {
    input,
    setInput,
    loading,
    steps,
    output,
    goal,
    execute,
    reset,
  };
}
