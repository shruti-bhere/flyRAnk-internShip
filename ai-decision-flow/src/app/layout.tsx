import type { Metadata } from "next";
import "@xyflow/react/dist/style.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Decision Flow",
  description: "Visual AI decision workflows using React Flow and Inngest",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-white antialiased m-0 p-0 overflow-hidden">
        {children}
      </body>
    </html>
  );
}