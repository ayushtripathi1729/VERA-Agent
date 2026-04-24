import type { Config } from "tailwindcss";

const config: Config = {
  // 1. Ensure Tailwind scans all your new components and app files
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      // 2. Custom "Cyber-Oasis" Color Palette
      colors: {
        cyber: {
          bg: "#020617",       // Deep Space Blue
          neon: "#06b6d4",     // Cyan Glow
          terminal: "#22c55e", // Classic Matrix Green
          danger: "#ef4444",   // System Alert Red
          warning: "#eab308",  // Execution Yellow
          border: "#164e63",   // Muted Cyan for Glass Panels
        },
      },
      // 3. Extended Typography for that Terminal feel
      fontFamily: {
        sans: ["var(--font-inter)"],
        mono: ["var(--font-jetbrains)"],
      },
      // 4. Custom Animations for the HUD elements
      animation: {
        "pulse-fast": "pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "scanline": "scanline-move 8s linear infinite",
        "float": "float 3s ease-in-out infinite",
      },
      keyframes: {
        "scanline-move": {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(1000%)" },
        },
        "float": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-5px)" },
        },
      },
      // 5. Enhanced Blur for high-end Glassmorphism
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
};

export default config;
