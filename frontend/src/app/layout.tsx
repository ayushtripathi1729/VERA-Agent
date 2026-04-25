import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "V.E.R.A Neural Console",
  description: "Versatile Executive & Reasoning Agent (V.E.R.A)",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>

        {/* 🌐 MAIN APP WRAPPER */}
        <div className="min-h-screen w-full">

          {/* ⚡ BACKGROUND EFFECT LAYER */}
          <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_top,#0f172a,#020617)]" />

          {/* 🧠 APP CONTENT */}
          <main className="relative z-10">
            {children}
          </main>

        </div>

      </body>
    </html>
  );
}
