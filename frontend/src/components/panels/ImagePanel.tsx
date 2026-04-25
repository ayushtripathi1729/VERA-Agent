"use client";

type Props = {
  input: string;
};

/**
 * Maps user input to a relevant visual
 */
function getImageSource(input: string): string {
  const text = input.toLowerCase();

  if (text.includes("prime") || text.includes("math") || text.includes("number")) {
    return "/images/math-visual.png";
  }

  if (text.includes("rsa") || text.includes("crypto") || text.includes("encryption")) {
    return "/images/crypto-diagram.png";
  }

  if (text.includes("ai") || text.includes("neural") || text.includes("model")) {
    return "/images/neural-network.png";
  }

  if (text.includes("security") || text.includes("api") || text.includes("audit")) {
    return "/images/security.png";
  }

  return "/images/ai-brain.svg";
}

export default function ImagePanel({ input }: Props) {
  const imageSrc = getImageSource(input);

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 glow-card">

      {/* HEADER */}
      <h2 className="text-pink-400 text-sm font-semibold mb-2 tracking-wide">
        VISUAL CONTEXT
      </h2>

      {/* IMAGE */}
      <div className="w-full flex items-center justify-center">
        <img
          src={imageSrc}
          alt="visual context"
          className="max-h-[180px] object-contain opacity-90"
        />
      </div>

    </div>
  );
}
