"use client";

type Props = {
  steps: string[];
};

/**
 * Classifies each step into an agent lane
 */
function classifyStep(step: string) {
  const s = step.toLowerCase();

  if (s.includes("plan") || s.includes("decompos") || s.includes("understand")) {
    return "planner";
  }

  if (s.includes("tool") || s.includes("execut") || s.includes("compute")) {
    return "tool";
  }

  if (s.includes("final") || s.includes("synth") || s.includes("result")) {
    return "output";
  }

  return "system";
}

export default function AgentBoard({ steps }: Props) {
  const lanes = {
    planner: [] as string[],
    tool: [] as string[],
    output: [] as string[],
    system: [] as string[],
  };

  // Distribute steps into lanes
  steps.forEach((step) => {
    const type = classifyStep(step);
    lanes[type].push(step);
  });

  const Lane = ({
    title,
    items,
    color,
  }: {
    title: string;
    items: string[];
    color: string;
  }) => (
    <div className="bg-slate-900/60 border border-slate-700 rounded-xl p-3 flex flex-col glow-card">

      {/* HEADER */}
      <h3 className={`text-xs mb-2 tracking-wide ${color}`}>
        {title}
      </h3>

      {/* CONTENT */}
      <div className="text-xs font-mono space-y-1 overflow-y-auto max-h-[200px] pr-1">
        {items.length === 0 && (
          <p className="text-gray-500">No activity</p>
        )}

        {items.map((item, index) => (
          <div key={index} className="animate-fadeIn">
            • {item}
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="grid grid-cols-4 gap-3">

      <Lane
        title="PLANNER"
        items={lanes.planner}
        color="text-purple-400"
      />

      <Lane
        title="TOOLS"
        items={lanes.tool}
        color="text-yellow-400"
      />

      <Lane
        title="OUTPUT"
        items={lanes.output}
        color="text-green-400"
      />

      <Lane
        title="SYSTEM"
        items={lanes.system}
        color="text-gray-400"
      />

    </div>
  );
}
