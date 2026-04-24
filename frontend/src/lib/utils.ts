import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * CN (Class Name) Merger
 * Combines tailwind classes and handles conditional logic without style conflicts.
 * Essential for the glassmorphism and glow effects in our HUD.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Neural Data Formatter
 * Sanitizes and truncates strings for the terminal view.
 */
export function formatNeuralText(text: string, maxLength: number = 500): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + "... [DATA_TRUNCATED]";
}

/**
 * System Timestamp Generator
 * Returns a high-precision timestamp for the terminal logs.
 */
export function getSystemTime(): string {
  return new Date().toLocaleTimeString('en-GB', {
    hour12: false,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
  });
}

/**
 * Delay Utility
 * Used to simulate "Thinking Time" for the AI Agent in the UI.
 */
export const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Error Parser
 * Safely extracts error messages from failed API calls for the Terminal.
 */
export function parseApiError(error: any): string {
  if (error.response?.data?.detail) return error.response.data.detail;
  if (error.message) return error.message;
  return "UNKNOWN_NEURAL_DISCONNECT";
}
