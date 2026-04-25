"use client";

import { useEffect, useState } from "react";

type Props = {
  loading: boolean;
};

export default function StatusBar({ loading }: Props) {
  const [time, setTime] = useState("");
  const [latency, setLatency] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      setTime(now.toLocaleTimeString());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  // fake latency simulation
  useEffect(() => {
    if (loading) {
      setLatency(Math.floor(Math.random() * 400) + 200);
    }
  }, [loading]);

  return (
    <div className="bg-slate-900/70 border border-slate-700 rounded-lg px-4 py-2 flex justify-between items-center text-xs text-gray-400 backdrop-blur">

      <div className="flex gap-4">
        <span>🧠 MODEL: Llama3-70B</span>
        <span>⚡ LATENCY: {loading ? `${latency}ms` : "--"}</span>
        <span>🟢 STATUS: {loading ? "PROCESSING" : "READY"}</span>
      </div>

      <div>
        ⏱ {time}
      </div>
    </div>
  );
}
