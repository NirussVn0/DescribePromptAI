"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export function ThemeToggle() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  const mode = (theme ?? resolvedTheme ?? "dark") === "dark" ? "dark" : "light";
  const toggle = () => {
    setTheme(mode === "dark" ? "light" : "dark");
  };

  return (
    <button
      aria-label="Toggle theme"
      className="flex items-center gap-2 rounded-full border border-slate-400/30 bg-slate-200/70 px-4 py-1 text-sm font-medium text-slate-800 transition hover:border-slate-500/60 focus:outline-none focus:ring-2 focus:ring-brand focus:ring-offset-2 dark:border-slate-700/60 dark:bg-slate-900/60 dark:text-slate-200 dark:hover:border-slate-500"
      onClick={toggle}
      type="button"
    >
      <span className="hidden sm:inline">{mode === "dark" ? "Dark" : "Light"} mode</span>
      <span aria-hidden className="text-lg sm:text-base">
        {mode === "dark" ? "🌙" : "☀️"}
      </span>
    </button>
  );
}
