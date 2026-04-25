"use client";

/**
 * Loader
 * ------
 * Displays V.E.R.A thinking state with animated dots
 */
export default function Loader() {
  return (
    <div className="flex items-center gap-2 text-yellow-400 mt-1">

      {/* Brain icon */}
      <span className="text-sm">🧠</span>

      {/* Text */}
      <span className="text-sm">Thinking</span>

      {/* Animated dots */}
      <span className="flex gap-1 ml-1">
        <span className="w-1 h-1 bg-yellow-400 rounded-full animate-dot" />
        <span className="w-1 h-1 bg-yellow-400 rounded-full animate-dot [animation-delay:0.2s]" />
        <span className="w-1 h-1 bg-yellow-400 rounded-full animate-dot [animation-delay:0.4s]" />
      </span>

    </div>
  );
}
