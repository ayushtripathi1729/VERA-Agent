/**
 * Utility Functions for V.E.R.A Frontend
 */

/**
 * Returns current time in HH:MM:SS format
 */
export function getCurrentTime(): string {
  return new Date().toLocaleTimeString();
}

/**
 * Truncates long text safely
 */
export function truncateText(text: string, maxLength: number = 100): string {
  if (!text) return "";
  return text.length > maxLength
    ? text.slice(0, maxLength) + "..."
    : text;
}

/**
 * Safely copy text to clipboard
 */
export async function copyToClipboard(text: string) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    return false;
  }
}

/**
 * Download text as file
 */
export function downloadTextFile(filename: string, content: string) {
  const blob = new Blob([content], { type: "text/plain" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();

  URL.revokeObjectURL(url);
}

/**
 * Simple delay helper (useful for animations/testing)
 */
export function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
