import {
  FiCpu,
  FiFilm,
  FiLayers,
  FiStar,
  FiUploadCloud,
  FiZap,
} from "react-icons/fi";

import AnalysisPanel from "../components/AnalysisPanel/AnalysisPanel";
import ExportButtons from "../components/ExportButtons/ExportButtons";
import ImageUpload from "../components/ImageUpload/ImageUpload";
import JsonPromptDisplay from "../components/JsonPromptDisplay/JsonPromptDisplay";
import ToggleControls from "../components/ToggleControls/ToggleControls";
import { ThemeToggle } from "../components/Theme/ThemeToggle";
import VideoPromptBuilder from "../components/VideoPromptBuilder/VideoPromptBuilder";

const highlights = [
  {
    icon: FiCpu,
    title: "Multimodal Intelligence",
    description:
      "Run Claude Vision + InsightFace analysis in one streamlined pass.",
  },
  {
    icon: FiFilm,
    title: "Studio-Ready Prompts",
    description:
      "Generate tuned payloads for Sora, Runway, Pika, and Luma instantly.",
  },
  {
    icon: FiLayers,
    title: "Re-usable Context",
    description:
      "Cache embeddings and scenes with Redis + Postgres persistence.",
  },
];

const quickActions = [
  {
    icon: FiUploadCloud,
    label: "1. Upload a reference image",
    detail: "Drag & drop or browse. We keep the original safe in S3 or memory.",
  },
  {
    icon: FiStar,
    label: "2. Toggle analysis emphasis",
    detail:
      "Switch between face precision and environment comprehension on demand.",
  },
  {
    icon: FiZap,
    label: "3. Export platform prompts",
    detail:
      "Copy, download, or extend into video storyboards with a single click.",
  },
];

export default function HomePage() {
  return (
    <div className="relative min-h-screen bg-slate-50/60 pb-16 dark:bg-slate-950">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-72 bg-gradient-to-b from-brand/30 via-transparent to-transparent blur-3xl opacity-60 dark:from-brand/40" />

      <main className="relative mx-auto flex w-full max-w-6xl flex-col gap-10 px-4 pb-12 pt-14 sm:px-8">
        <header className="flex flex-col gap-6 rounded-3xl border border-slate-200/70 bg-white/80 p-8 shadow-xl dark:border-slate-800/80 dark:bg-slate-900/70">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-brand/30 bg-brand/10 px-4 py-1 text-sm font-medium text-brand dark:border-brand-light/40 dark:bg-brand/20 dark:text-brand-light">
                DescribePromptAI
              </div>
              <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900 dark:text-white">
                Turn reference imagery into cinematic video prompts.
              </h1>
              <p className="mt-3 max-w-2xl text-base text-slate-600 dark:text-slate-300">
                Upload an image, run multimodal analysis, and receive
                platform-tuned prompts with preserved identity and motion cues.
                Built for creative automation teams and prompt engineers.
              </p>
            </div>
            <ThemeToggle />
          </div>
          <dl className="grid gap-4 pt-4 sm:grid-cols-2 lg:grid-cols-3">
            {highlights.map((item) => (
              <div
                key={item.title}
                className="group flex items-start gap-4 rounded-2xl border border-slate-200/80 bg-slate-100/60 p-4 transition hover:border-brand/50 hover:bg-white dark:border-slate-800/80 dark:bg-slate-900/80 dark:hover:border-brand/60"
              >
                <item.icon className="mt-1 text-2xl text-brand dark:text-brand-light" />
                <div>
                  <dt className="text-sm font-semibold text-slate-900 dark:text-white">
                    {item.title}
                  </dt>
                  <dd className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                    {item.description}
                  </dd>
                </div>
              </div>
            ))}
          </dl>
        </header>

        <section className="grid grid-cols-1 gap-8 lg:grid-cols-[1.1fr_1fr]">
          <div className="flex flex-col gap-6">
            <ImageUpload />
            <ToggleControls />
            <AnalysisPanel />
          </div>
          <div className="flex flex-col gap-6">
            <VideoPromptBuilder />
            <JsonPromptDisplay />
            <ExportButtons />
          </div>
        </section>

        <section className="rounded-3xl border border-slate-200/70 bg-white/80 p-8 shadow-lg dark:border-slate-800/80 dark:bg-slate-900/70">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">
            Workflow at a glance
          </h2>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            Keep this checklist handy while you iterate on prompt variations.
            Everything updates live as you upload, analyze, and export.
          </p>
          <ol className="mt-6 grid gap-4 md:grid-cols-3">
            {quickActions.map((step, index) => (
              <li
                key={step.label}
                className="flex flex-col gap-3 rounded-2xl border border-slate-200/80 bg-slate-100/60 p-4 dark:border-slate-800/70 dark:bg-slate-900/70"
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand/15 text-brand dark:bg-brand/30 dark:text-brand-light">
                    <step.icon className="text-xl" />
                  </span>
                  <span className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                    Step {index + 1}
                  </span>
                </div>
                <p className="text-base font-medium text-slate-900 dark:text-white">
                  {step.label}
                </p>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  {step.detail}
                </p>
              </li>
            ))}
          </ol>
        </section>
      </main>
    </div>
  );
}
