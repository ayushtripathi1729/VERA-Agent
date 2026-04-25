"use client";

import React from "react";

type Props = {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: "primary" | "secondary" | "danger";
  className?: string;
};

/**
 * Reusable Button Component
 * Variants: primary | secondary | danger
 */
export default function Button({
  children,
  onClick,
  disabled = false,
  variant = "secondary",
  className = "",
}: Props) {
  const base =
    "px-3 py-1 rounded text-sm transition font-medium";

  const variants = {
    primary: "bg-green-500 hover:bg-green-600 text-black",
    secondary: "bg-slate-700 hover:bg-slate-600 text-white",
    danger: "bg-red-500 hover:bg-red-600 text-white",
  };

  const disabledStyle = "bg-gray-600 cursor-not-allowed";

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${
        disabled ? disabledStyle : variants[variant]
      } ${className}`}
    >
      {children}
    </button>
  );
}
