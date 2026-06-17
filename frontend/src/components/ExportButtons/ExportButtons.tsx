"use client";

import { FiCopy, FiDownload, FiFileText } from "react-icons/fi";

import { promptStore } from "../../store/promptStore";

function downloadBlob(data: string, filename: string, type: string) {
  const blob = new Blob([data], { type });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  link.parentNode?.removeChild(link);
  window.URL.revokeObjectURL(url);
}

export default function ExportButtons() {
  const prompts = promptStore((state) => state.prompts);

  const handleCopy = async () => {
    if (!prompts.length) {
      return;
    }
    await navigator.clipboard.writeText(JSON.stringify(prompts, null, 2));
  };

  const actions = [
    {
      label: "Download JSON",
      icon: FiDownload,
      handler: () =>
        downloadBlob(JSON.stringify(prompts, null, 2), "prompts.json", "application/json")
    },
    {
      label: "Download CSV",
      icon: FiFileText,
      handler: () =>
        downloadBlob(
          "platform,content\n" +
            prompts.map((prompt) => `${prompt.platform},${JSON.stringify(prompt.prompt)}`).join("\n"),
          "prompts.csv",
          "text/csv"
        )
    },
    {
      label: "Copy JSON",
      icon: FiCopy,
      handler: () => void handleCopy()
    }
  ];

  return (
    <div className="rounded-3xl border border-slate-200/70 bg-white/90 p-5 shadow-lg dark:border-slate-800/70 dark:bg-slate-900/70">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Export prompt data</h2>
        <span className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
          {prompts.length ? "Ready" : "Awaiting analysis"}
        </span>
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        {actions.map(({ label, handler, icon: Icon }) => (
          <button
            key={label}
            className="flex items-center justify-center gap-2 rounded-xl border border-slate-200/70 bg-slate-100/60 px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-brand hover:bg-white focus:outline-none focus:ring-2 focus:ring-brand/60 disabled:cursor-not-allowed disabled:border-slate-200 disabled:bg-slate-100 dark:border-slate-800/70 dark:bg-slate-900/60 dark:text-slate-200 dark:hover:border-brand-light dark:hover:bg-slate-900"
            disabled={!prompts.length}
            type="button"
            onClick={handler}
          >
            <Icon className="text-base" />
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}
