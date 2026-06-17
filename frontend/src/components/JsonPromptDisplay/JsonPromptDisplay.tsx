"use client";

import { FiCode } from "react-icons/fi";
import { useTheme } from "next-themes";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark, duotoneLight } from "react-syntax-highlighter/dist/esm/styles/prism";

import { promptStore } from "../../store/promptStore";

export default function JsonPromptDisplay() {
  const prompts = promptStore((state) => state.prompts);
  const { resolvedTheme } = useTheme();
  const theme = resolvedTheme === "light" ? duotoneLight : atomDark;

  return (
    <div className="rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-lg dark:border-slate-800/80 dark:bg-slate-900/70">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-full bg-brand/15 text-brand dark:bg-brand/25 dark:text-brand-light">
            <FiCode />
          </span>
          <div>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-white">Prompt preview</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Normalized JSON output for each selected generation platform.
            </p>
          </div>
        </div>
        <span className="rounded-full bg-slate-200 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-slate-700 dark:bg-slate-800 dark:text-slate-200">
          {prompts.length} platform{prompts.length === 1 ? "" : "s"}
        </span>
      </div>
      <div className="mt-4 rounded-2xl border border-slate-200/70 bg-slate-100/60 p-3 dark:border-slate-800/80 dark:bg-slate-900/70">
        {prompts.length ? (
          <SyntaxHighlighter
            className="max-h-72 overflow-y-auto rounded-lg text-xs"
            language="json"
            showLineNumbers
            style={theme}
            wrapLines
          >
            {JSON.stringify(prompts, null, 2)}
          </SyntaxHighlighter>
        ) : (
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Generate prompts to preview platform payloads, metadata, and face embedding references.
          </p>
        )}
      </div>
    </div>
  );
}
