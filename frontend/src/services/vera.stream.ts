/**
 * V.E.R.A Streaming Service
 * Handles SSE (if available) + fallback to normal API
 */

import { runVera } from "./vera.service";

const BASE_URL = "https://vera-backend-djwd.onrender.com";

export type StreamHandlers = {
  onStep: (step: string) => void;
  onGoal?: (goal: string) => void;
  onFinal: (output: string) => void;
  onError: (err: string) => void;
};

/**
 * Main streaming function
 */
export function streamVera(
  instruction: string,
  handlers: StreamHandlers
) {
  let closed = false;

  try {
    // 🔥 Attempt SSE connection (future-ready)
    const url = `${BASE_URL}/stream?instruction=${encodeURIComponent(
      instruction
    )}`;

    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      if (closed) return;

      try {
        const data = JSON.parse(event.data);

        if (data.type === "step") {
          handlers.onStep(data.payload);
        }

        if (data.type === "goal") {
          handlers.onGoal?.(data.payload);
        }

        if (data.type === "final") {
          handlers.onFinal(data.payload);
          eventSource.close();
          closed = true;
        }
      } catch {
        // fallback: plain text step
        handlers.onStep(event.data);
      }
    };

    eventSource.onerror = () => {
      // 🔁 fallback to API if SSE fails
      eventSource.close();
      closed = true;

      fallbackExecution(instruction, handlers);
    };

    return () => {
      eventSource.close();
      closed = true;
    };
  } catch {
    // 🔁 fallback immediately if SSE not supported
    fallbackExecution(instruction, handlers);
  }
}

/**
 * Fallback execution using standard API
 */
async function fallbackExecution(
  instruction: string,
  handlers: StreamHandlers
) {
  try {
    handlers.onStep("🧠 Planning...");
    handlers.onStep("⚙️ Executing...");

    const res = await runVera(instruction);

    if (res.goal) {
      handlers.onGoal?.(res.goal);
    }

    handlers.onFinal(res.logs || "No response");
  } catch (err: any) {
    handlers.onError("Fallback execution failed");
  }
}
