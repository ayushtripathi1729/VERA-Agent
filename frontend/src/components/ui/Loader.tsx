"use client";

export default function Loader() {
  return (
    <div className="flex items-center gap-2 text-yellow-400 animate-pulse">
      <span className="text-lg">🧠</span>
      <span>Thinking...</span>

      {/* dots animation */}
      <span className="flex gap-1 ml-1">
        <span className="w-1 h-1 bg-yellow-400 rounded-full animate-bounce"></span>
        <span className="w-1 h-1 bg-yellow-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
        <span className="w-1 h-1 bg-yellow-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
      </span>
    </div>
  );
}
