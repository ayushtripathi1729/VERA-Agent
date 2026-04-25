"use client";

type Props = {
  input: string;
};

export default function ImagePanel({ input }: Props) {
  const getImage = () => {
    const text = input.toLowerCase();

    if (text.includes("prime") || text.includes("math")) {
      return "/images/math-visual.png";
    }

    if (text.includes("crypto") || text.includes("rsa")) {
      return "/images/crypto-diagram.png";
    }

    if (text.includes("ai") || text.includes("neural")) {
      return "/images/neural-network.png";
    }

    return "/images/ai-brain.svg";
  };

  return (
    <div className="bg-slate-800/60 backdrop-blur-lg border border-slate-700 rounded-xl p-4 h-[250px] shadow-lg">

      {/* HEADER */}
      <h2 className="text-pink-400 font-semibold mb-2">
        VISUAL CONTEXT
      </h2>

      {/* IMAGE */}
      <div className="w-full h-full flex items-center justify-center">
        <img
          src={getImage()}
          alt="visual"
          className="max-h-full object-contain opacity-90"
        />
      </div>

    </div>
  );
}
