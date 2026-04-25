// src/services/vera.service.ts

export type VeraResponse = {
  status: string;
  goal: string;
  logs: string;
  raw: any;
};

const BASE_URL = "https://vera-backend-djwd.onrender.com";

export async function runVera(instruction: string): Promise<VeraResponse> {
  try {
    const response = await fetch(`${BASE_URL}/run`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ instruction }),
    });

    if (!response.ok) {
      throw new Error("Backend error");
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error("V.E.R.A API ERROR:", error);

    return {
      status: "error",
      goal: "",
      logs: "❌ Unable to connect to backend.",
      raw: null,
    };
  }
}
