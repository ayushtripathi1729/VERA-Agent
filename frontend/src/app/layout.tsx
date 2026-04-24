import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

// Inter for clean UI elements
const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-inter",
});

// JetBrains Mono for the authentic "Terminal" feel
const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "V.E.R.A. | Neural Execution Core",
  description: "Autonomous Agentic Architecture for Research and Security Audit",
  icons: {
    icon: "/favicon.ico", // Ensure you have an icon in /public
  },
};

export const viewport: Viewport = {
  themeColor: "#020617",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark selection:bg-cyan-500/30">
      <body
        className={`${inter.variable} ${jetbrains.variable} font-sans antialiased bg-[#020617] text-cyan-50 min-h-screen`}
      >
        {/* CRT Vignette Layer - Fixed at the top of the stack */}
        <div className="vignette pointer-events-none fixed inset-0 z-[100]" />

        {/* Ambient Background Glows */}
        <div className="fixed top-[-10%] left-[-10%] w-[50%] h-[50%] bg-cyan-500/5 blur-[120px] rounded-full pointer-events-none z-0" />
        <div className="fixed bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-600/5 blur-[120px] rounded-full pointer-events-none z-0" />

        {/* Main Application Container */}
        <div className="relative z-10 flex flex-col min-h-screen">
          {children}
        </div>

        {/* System Scanline (Overlaying the whole page for subtle CRT feel) */}
        <div className="fixed inset-0 pointer-events-none opacity-[0.03] z-[90] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_2px,3px_100%]" />
      </body>
    </html>
  );
}
