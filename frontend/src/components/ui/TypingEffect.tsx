"use client";

import { useEffect, useState } from "react";

type Props = {
  text: string;
};

/**
 * TypingEffect
 * -------------
 * Simulates AI typing output with adaptive speed + blinking cursor
 */
export default function TypingEffect({ text }: Props) {
  const [display, setDisplay] = useState("");

  useEffect(() => {
    let i = 0;
    setDisplay("");

    // Adaptive speed: longer text = faster typing
    const speed = Math.max(5, 25 - text.length / 40);

    const interval = setInterval(() => {
      setDisplay((prev) => prev + text.charAt(i));
      i++;

      if (i >= text.length) {
        clearInterval(interval);
      }
    }, speed);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <pre className="whitespace-pre-wrap">
      {display}
      <span className="cursor-blink">|</span>
    </pre>
  );
}
