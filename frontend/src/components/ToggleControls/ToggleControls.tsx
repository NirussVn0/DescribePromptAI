"use client";

import { type ComponentType } from "react";
import { FiGlobe, FiUser } from "react-icons/fi";
import toast from "react-hot-toast";

import { analysisStore } from "../../store/analysisStore";
import { getErrorMessage } from "../../utils/errors";

const modeConfig: Record<
  "face" | "context",
  { label: string; description: string; icon: ComponentType<{ className?: string }> }
> = {
  face: {
    label: "Face fidelity",
    description: "Identity, expression, and embedding",
    icon: FiUser
  },
  context: {
    label: "Scene context",
    description: "Environment, lighting, and composition",
    icon: FiGlobe
  }
};

export default function ToggleControls() {
  const modes = analysisStore((state) => state.modes);
  const runAnalysis = analysisStore((state) => state.runAnalysis);
  const toggleMode = analysisStore((state) => state.toggleMode);
  const imageId = analysisStore((state) => state.imageId);

  const handleToggle = async (key: "face" | "context") => {
    toggleMode(key);
    if (!imageId) {
      return;
    }
    try {
      await runAnalysis(imageId);
    } catch (error) {
      toast.error(getErrorMessage(error, "Failed to refresh analysis."));
    }
  };

  return (
    <div className="rounded-3xl border border-slate-200/70 bg-white/80 p-5 shadow-lg dark:border-slate-800/80 dark:bg-slate-900/70">
      <div className="flex flex-col gap-1 pb-3">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Analysis focus</h3>
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Toggle between facial precision and broader scene insights. Switching replays the last analysis
          when an image is active.
        </p>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        {(Object.keys(modeConfig) as Array<"face" | "context">).map((key) => {
          const active = modes.includes(key);
          const { label, description, icon: Icon } = modeConfig[key];
          return (
            <button
              key={key}
              className={`flex h-full flex-col items-start gap-2 rounded-2xl border px-4 py-3 text-left transition focus:outline-none focus:ring-2 focus:ring-brand/60 ${
                active
                  ? "border-brand/50 bg-brand/10 text-brand dark:border-brand-light/50 dark:bg-brand/20 dark:text-brand-light"
                  : "border-slate-200 bg-slate-100/50 text-slate-600 hover:border-slate-300 hover:bg-white dark:border-slate-800 dark:bg-slate-900/60 dark:text-slate-300"
              }`}
              onClick={() => void handleToggle(key)}
              type="button"
            >
              <div className="flex items-center gap-2">
                <Icon className="text-lg" />
                <span className="text-sm font-semibold">{label}</span>
              </div>
              <span className="text-xs text-slate-500 dark:text-slate-400">{description}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
