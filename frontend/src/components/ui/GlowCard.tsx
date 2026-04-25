"use client";

import React from "react";

type Props = {
  children: React.ReactNode;
  className?: string;
};

/**
 * GlowCard
 * --------
 * Reusable wrapper for panels with consistent glow + styling.
 * Optional className allows extension.
 */
export default function GlowCard({ children, className = "" }: Props) {
  return (
    <div
      className={`bg-slate-800/60 border border-slate-700 rounded-xl p-4 shadow-lg backdrop-blur glow-card ${className}`}
    >
      {children}
    </div>
  );
}
