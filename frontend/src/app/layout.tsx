import type { Metadata } from "next";
import { Toaster } from "react-hot-toast";
import type { ReactNode } from "react";

import { AppThemeProvider } from "../components/Theme/AppThemeProvider";
import "./globals.css";

export const metadata: Metadata = {
  title: "DescribePromptAI",
  description: "Vision-to-video prompt generation workspace"
};

export default function RootLayout({
  children
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        suppressHydrationWarning
        className="min-h-screen bg-slate-50 text-slate-900 antialiased transition-colors duration-300 dark:bg-slate-950 dark:text-slate-100"
      >
        <AppThemeProvider>
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 3500,
              className: "border border-slate-200 bg-slate-100 text-slate-900 shadow-lg dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
            }}
          />
        </AppThemeProvider>
      </body>
    </html>
  );
}
