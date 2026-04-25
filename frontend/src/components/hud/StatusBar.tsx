"use client";

import { useEffect, useState } from "react";

type Props = {
  loading: boolean;
  latency: number;
};

export default function StatusBar({ loading, latency }: Props) {
  const [time, setTime] = useState("");

  // ⏱ Live clock
  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-slate-900/60 border border-slate-700 rounded-lg px-4 py-2 flex justify-between items-center text-xs text-gray-400 backdrop-blur glow-card">

      {/* LEFT SIDE */}
      <div className="flex gap-4 flex-wrap">
        <span>🧠 MODEL: Llama3-70B</span>

        <span>
          ⚡ LATENCY: {latency ? `${latency}ms` : "--"}
        </span>

        <span className={loading ? "text-yellow-400" : "text-green-400"}>
          {loading ? "🟡 PROCESSING" : "🟢 READY"}
        </span>
      </div>

      {/* RIGHT SIDE */}
      <div>
        ⏱ {time}
      </div>

    </div>
  );
}
