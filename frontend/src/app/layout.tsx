import "./globals.css";

export const metadata = {
  title: "V.E.R.A Neural Console",
  description: "Versatile Executive & Reasoning Agent",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
