"use client";

type Props = {
  title?: string;
  children: React.ReactNode;
  height?: string; // optional custom height
};

export default function Terminal({
  title = "TERMINAL",
  children,
  height = "h-[300px]",
}: Props) {
  return (
    <div
      className={`bg-black/80 border border-slate-700 rounded-xl flex flex-col overflow-hidden glow-card`}
    >
      {/* HEADER */}
      <div className="flex items-center justify-between px-3 py-2 bg-slate-900 border-b border-slate-700">
        <span className="text-xs text-gray-400 tracking-wide">
          {title}
        </span>

        {/* fake terminal buttons */}
        <div className="flex gap-1">
          <span className="w-2 h-2 rounded-full bg-red-500" />
          <span className="w-2 h-2 rounded-full bg-yellow-400" />
          <span className="w-2 h-2 rounded-full bg-green-500" />
        </div>
      </div>

      {/* BODY */}
      <div
        className={`p-3 text-green-300 text-sm font-mono overflow-y-auto ${height}`}
      >
        {children}
      </div>
    </div>
  );
}
