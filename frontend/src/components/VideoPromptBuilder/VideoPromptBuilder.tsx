"use client";

import { useEffect } from "react";
import { FiFilm, FiPlay } from "react-icons/fi";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import toast from "react-hot-toast";

import { useVideoExtension } from "../../hooks/useVideoExtension";
import { getErrorMessage } from "../../utils/errors";

const videoPromptSchema = z.object({
  motion: z.string().min(10, "Describe the motion in at least 10 characters."),
  duration: z
    .coerce.number({
      invalid_type_error: "Duration must be a number."
    })
    .int("Duration must be a whole number.")
    .min(1, "Duration must be at least 1 second.")
    .max(120, "Duration cannot exceed 120 seconds.")
    .default(12)
});

type VideoPromptFormValues = z.infer<typeof videoPromptSchema>;

export default function VideoPromptBuilder() {
  const { imageId, extendPrompt, isExtending, videoPrompt, resetPrompt } = useVideoExtension();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting }
  } = useForm<VideoPromptFormValues>({
    resolver: zodResolver(videoPromptSchema),
    defaultValues: {
      motion: "",
      duration: 12
    }
  });

  useEffect(() => {
    if (!imageId) {
      reset({ motion: "", duration: 12 });
      resetPrompt();
    }
  }, [imageId, reset, resetPrompt]);

  const onSubmit = async (values: VideoPromptFormValues) => {
    try {
      await extendPrompt({
        motion: values.motion,
        durationSeconds: values.duration
      });
      toast.success("Video prompt extended successfully.");
    } catch (error) {
      toast.error(getErrorMessage(error, "Failed to extend video prompt."));
    }
  };

  return (
    <div className="rounded-3xl border border-slate-200/70 bg-gradient-to-br from-white via-white to-slate-100/70 p-6 shadow-lg dark:border-slate-800/70 dark:from-slate-900 dark:via-slate-900 dark:to-slate-950/70">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-full bg-brand/15 text-brand dark:bg-brand/25 dark:text-brand-light">
            <FiFilm />
          </span>
          <div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Video extension builder</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Blend scene analysis with motion direction to form platform-ready video cues.
            </p>
          </div>
        </div>
      </div>

      <form className="mt-4 flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200" htmlFor="motion">
            Motion & Actions
          </label>
          <textarea
            className="w-full rounded-md border border-slate-300 bg-white/70 p-3 text-sm text-slate-900 focus:border-brand focus:outline-none dark:border-slate-700 dark:bg-slate-950/50 dark:text-white"
            id="motion"
            placeholder="Describe desired motion, camera moves, or pacing"
            rows={4}
            {...register("motion")}
          />
          {errors.motion && <p className="mt-1 text-xs text-red-400">{errors.motion.message}</p>}
        </div>
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-200" htmlFor="duration">
            Duration (seconds)
          </label>
          <input
            className="w-full rounded-md border border-slate-300 bg-white/70 p-3 text-sm text-slate-900 focus:border-brand focus:outline-none dark:border-slate-700 dark:bg-slate-950/50 dark:text-white"
            id="duration"
            min={1}
            max={120}
            type="number"
            {...register("duration")}
          />
          {errors.duration && <p className="mt-1 text-xs text-red-400">{errors.duration.message}</p>}
        </div>
        <button
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-brand px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-brand/20 transition hover:bg-brand-dark focus:outline-none focus:ring-2 focus:ring-brand/60 disabled:cursor-not-allowed disabled:bg-slate-400 dark:disabled:bg-slate-700"
          disabled={!imageId || isExtending || isSubmitting}
          type="submit"
        >
          <FiPlay className="text-lg" />
          {isExtending || isSubmitting ? "Generating..." : "Generate video prompt"}
        </button>
        {!imageId && (
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Upload and analyze an image to enable video prompt generation.
          </p>
        )}
      </form>
      {videoPrompt && (
        <div className="mt-4 rounded-2xl border border-slate-200/70 bg-slate-100/70 p-4 dark:border-slate-800/70 dark:bg-slate-900/70">
          <div className="mb-2 flex items-center justify-between text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
            <span>Video prompt payload</span>
            <span>{videoPrompt?.technical?.duration_seconds ?? ""}s</span>
          </div>
          <pre className="max-h-48 overflow-y-auto rounded-lg bg-white/80 p-3 text-xs text-slate-800 dark:bg-slate-950/70 dark:text-slate-200">
            {JSON.stringify(videoPrompt, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
