"use client";

import { useExecution } from "@/hooks/useExecution";

/**
 * ExecutionEngine
 * ----------------
 * A wrapper component that provides execution logic (hook)
 * to any child component using render props pattern.
 *
 * This keeps logic separated from UI and allows scaling later
 * (multi-agent, different execution modes, etc.)
 */

type Props = {
  children: (execution: ReturnType<typeof useExecution>) => React.ReactNode;
};

export default function ExecutionEngine({ children }: Props) {
  const execution = useExecution();

  return <>{children(execution)}</>;
}
