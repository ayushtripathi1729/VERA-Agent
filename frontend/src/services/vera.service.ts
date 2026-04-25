/**
 * V.E.R.A API Service (Fallback / Direct Calls)
 */

const BASE_URL = "https://vera-backend-djwd.onrender.com";

/**
 * Standard execution request (non-streaming fallback)
 */
export async function runVera(instruction: string) {
  try {
    const res = await fetch(`${BASE_URL}/run`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ instruction }),
    });

    if (!res.ok) {
      throw new Error("Server error");
    }

    const data = await res.json();

    return {
      goal: data.goal || "",
      logs: data.logs || "",
      raw: data.raw || {},
    };
  } catch (error: any) {
    return {
      goal: "",
      logs: `❌ API ERROR: ${error.message}`,
      raw: {},
    };
  }
}

/**
 * Health check (useful for debugging backend status)
 */
export async function checkHealth() {
  try {
    const res = await fetch(`${BASE_URL}/`);

    if (!res.ok) {
      throw new Error("Backend not reachable");
    }

    return await res.json();
  } catch {
    return {
      status: "DOWN",
      message: "Unable to connect to backend",
    };
  }
}
