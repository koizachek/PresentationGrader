import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Presentation Grader with Voice Transcription",
  description: "Bewertung vertonter Präsentationen",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de">
      <body>{children}</body>
    </html>
  );
}
