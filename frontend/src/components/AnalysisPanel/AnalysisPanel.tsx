"use client";

import { FiAperture, FiHash, FiSliders } from "react-icons/fi";

import { usePromptGeneration } from "../../hooks/usePromptGeneration";
import { analysisStore } from "../../store/analysisStore";

const placeholderMetrics = [
  {
    label: "Face mode",
    description: "Tune embeddings & expressions",
    icon: FiAperture
  },
  {
    label: "Context mode",
    description: "Capture environment styling",
    icon: FiSliders
  },
  {
    label: "Confidence",
    description: "Model certainty per strategy",
    icon: FiHash
  }
];

export default function AnalysisPanel() {
  const analysis = analysisStore((state) => state.analysis);
  const { handleGenerate, isGenerating } = usePromptGeneration();

  if (!analysis) {
    return (
      <div className="rounded-3xl border border-slate-200/70 bg-white/80 p-6 text-slate-600 shadow-md dark:border-slate-800/80 dark:bg-slate-900/70 dark:text-slate-400">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Awaiting analysis</h2>
        <p className="mt-2 text-sm">
          Upload an image to view facial embeddings, scene descriptors, and multi-model confidence
          breakdowns. Results populate instantly once processing completes.
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          {placeholderMetrics.map((item) => (
            <div
              key={item.label}
              className="flex flex-col gap-2 rounded-2xl border border-dashed border-slate-300/70 p-4 text-sm dark:border-slate-700/70"
            >
              <item.icon className="text-lg text-slate-400 dark:text-slate-500" />
              <span className="font-semibold text-slate-700 dark:text-slate-200">{item.label}</span>
              <span className="text-xs text-slate-500 dark:text-slate-400">{item.description}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  const face = analysis.face;
  const context = analysis.context;
  const confidenceEntries = Object.entries(analysis.confidence ?? {});

  return (
    <div className="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-lg dark:border-slate-800/80 dark:bg-slate-900/70">
      <div className="flex flex-col gap-2 border-b border-slate-200/70 pb-4 dark:border-slate-800/80">
        <h2 className="text-xl font-semibold text-slate-900 dark:text-white">Analysis output</h2>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Structured traits extracted from the uploaded reference. Use the prompt generator below to fan
          out into platform-specific payloads.
        </p>
      </div>

      <div className="mt-5 grid gap-4 lg:grid-cols-2">
        <section className="rounded-2xl border border-slate-200/80 bg-slate-100/60 p-4 dark:border-slate-800/80 dark:bg-slate-900/70">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Face fidelity</h3>
            <span className="rounded-full bg-brand/15 px-3 py-0.5 text-xs font-medium text-brand dark:bg-brand/25 dark:text-brand-light">
              {face?.embedding_vector?.length ?? 0} dims
            </span>
          </div>
          {face ? (
            <dl className="mt-3 space-y-2 text-sm text-slate-700 dark:text-slate-200">
              <div className="flex items-start justify-between gap-4">
                <dt className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Embedding ID
                </dt>
                <dd className="max-w-[60%] text-right text-xs font-mono">{face.embedding_id}</dd>
              </div>
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Emotions
                </dt>
                <dd>{face.emotions?.join(", ") || "n/a"}</dd>
              </div>
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Accessories
                </dt>
                <dd>{face.accessories?.join(", ") || "n/a"}</dd>
              </div>
            </dl>
          ) : (
            <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
              Face analysis disabled. Enable the toggle to populate embeddings.
            </p>
          )}
        </section>

        <section className="rounded-2xl border border-slate-200/80 bg-slate-100/60 p-4 dark:border-slate-800/80 dark:bg-slate-900/70">
          <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Scene context</h3>
          {context ? (
            <dl className="mt-3 space-y-2 text-sm text-slate-700 dark:text-slate-200">
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">Scene</dt>
                <dd>{context.scene?.join(", ") || "n/a"}</dd>
              </div>
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Lighting
                </dt>
                <dd>{context.lighting || "n/a"}</dd>
              </div>
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Objects
                </dt>
                <dd>{context.detected_objects?.join(", ") || "n/a"}</dd>
              </div>
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Style tags
                </dt>
                <dd>{context.style_tags?.join(", ") || "n/a"}</dd>
              </div>
            </dl>
          ) : (
            <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
              Context analysis disabled. Enable the toggle to generate scenic metadata.
            </p>
          )}
        </section>
      </div>

      {confidenceEntries.length > 0 && (
        <div className="mt-4 rounded-2xl border border-slate-200/80 bg-white/70 p-4 dark:border-slate-800/80 dark:bg-slate-900/60">
          <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Model confidence
          </h3>
          <ul className="mt-2 grid gap-2 text-sm text-slate-600 dark:text-slate-300 sm:grid-cols-2">
            {confidenceEntries.map(([model, score]) => (
              <li key={model} className="flex items-center justify-between rounded-xl border border-slate-200/70 px-3 py-2 dark:border-slate-800/70">
                <span className="font-medium capitalize text-slate-700 dark:text-slate-200">{model}</span>
                <span className="rounded-full bg-slate-200 px-2 py-0.5 text-xs font-semibold text-slate-700 dark:bg-slate-800 dark:text-slate-200">
                  {(score * 100).toFixed(0)}%
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <button
        className="mt-6 w-full rounded-xl bg-brand px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-brand/20 transition hover:bg-brand-dark focus:outline-none focus:ring-2 focus:ring-brand/60 disabled:cursor-not-allowed disabled:bg-slate-400 disabled:text-slate-100 dark:disabled:bg-slate-700"
        disabled={isGenerating}
        onClick={() => void handleGenerate()}
        type="button"
      >
        {isGenerating ? "Generating platform prompts..." : "Generate platform prompts"}
      </button>
    </div>
  );
}
